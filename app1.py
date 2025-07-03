from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymongo

import redis

cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


app = Flask(__name__)
app.secret_key = 'secret-key-112326'

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('usersdb')
records = db.users

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'], password=session['password'],
                               name=session['name'], age=session['age'], email=session['email'],
                               dob=session['dob'], contact=session['contact'])
    else:
        return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data['username']
            pwd = data['password']

            cached_user = cache.hgetall(f"user:{username}")

            if cached_user:
                user = cached_user
            
            else:
                user = records.find_one({"username": username})
                if user:
                    cache.hmset(f"user:{username}",{
                        'username': user['username'],
                        'password': user['password'],
                        'name': user['name'],
                        'age': user['age'],
                        'email': user['email'],
                        'dob': user['dob'],
                        'contact': user['contact']
                })

            if user and pwd == user['password']:
                session['username'] = user['username']
                session['password'] = pwd
                session['name'] = user['name']
                session['age'] = user['age']
                session['email'] = user['email']
                session['dob'] = user['dob']
                session['contact'] = user['contact']
                return jsonify({'status': 'success', 'message': 'Login successful'})
            else:
                return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        pwd = request.form['password']
        age = request.form['age']
        email = request.form['email']
        dob = request.form['dob']
        contact = request.form['contact']
        

        records.insert_one({
            "username": username,
            "password": pwd,
            "name": name,
            "age": age,
            "email": email,
            "dob": dob,
            "contact": contact
        })

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data['name']
            age = data['age']
            dob = data['dob']
            email = data['email']
            contact = data['contact']

            if name == "":
                return jsonify({'status': 'error', 'message': 'Name cannot be empty'}), 400
            elif not age.isdigit() or int(age) < 0:
                return jsonify({'status': 'error', 'message': 'Age must be a positive integer'}), 400
            elif '@' not in email or '.' not in email:
                return jsonify({'status': 'error', 'message': 'Invalid email format'}), 400
            elif not contact.isdigit() or len(contact) != 10:
                return jsonify({'status': 'error', 'message': 'Contact must be a 10-digit number'}), 400
            else:
                records.update_one({"username": username}, {"$set": {
                    "name": name,
                    "age": age,
                    "dob": dob,
                    "email": email,
                    "contact": contact
                }})

                cache.hmset(f"user:{username}", {
                    'username': username,
                    'name': name,
                    'age': age,
                    'dob': dob,
                    'email': email,
                    'contact': contact,
                    'password': session['password']  # Reuse existing
                })

                session['name'] = name
                session['age'] = age
                session['dob'] = dob
                session['email'] = email
                session['contact'] = contact

                return jsonify({'status': 'success', 'message': 'Profile updated successfully'})

        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

    return render_template('update.html')

@app.route('/delete', methods=['POST'])
def delete_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    result = records.delete_one({'username': username})

    if result.deleted_count > 0:

        session.clear()
        cache.delete(f"user:{username}")
        return redirect(url_for('home'))
    
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
