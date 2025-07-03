from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL 
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret-key-112326'


con = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'mabelmanuel',
    database = 'usersdb'
)   

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html',username = session['username'], password = session['password'], 
                               name = session['name'], age = session['age'], email = session['email'], dob = session['dob'], contact = session['contact'])
    else:
        return render_template('home.html')
    
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':

        if request.is_json:
            
            data = request.get_json()

            username = data['username']
            pwd = data['password']

            cur = con.cursor()
            cur.execute(f"SELECT username, password, name, age, email, DATE_FORMAT(dob, '%d-%m-%Y'), contact FROM users WHERE username = '{username}';")
            user = cur.fetchone()
            cur.close()

            if user and pwd == user[1]:
                session['username'] = user[0]
                session['password'] = user[1]
                session['name'] = user[2]
                session['age'] = user[3]
                session['email'] = user[4]
                session['dob'] = user[5]
                session['contact'] = user[6]

                print("Logged in:", username)
                
                return jsonify({'status': 'success', 'message': 'Login successful'})
            else:
                return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
            
        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

    return render_template('login.html') 



@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        pwd = request.form['password']
        age = request.form['age']
        email = request.form['email']
        dob = request.form['dob']
        contact = request.form['contact']

        cur = con.cursor()
        cur.execute(f"""insert into users (username, password, age, dob, contact, email, name) 
                    values ('{username}','{pwd}','{age}','{dob}','{contact}','{email}','{name}');""")
        con.commit()
        cur.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

#read, update, delete operations

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

            if name == "" :
                return jsonify({'status': 'error', 'message': 'Name cannot be empty'}), 400
            elif age.isdigit() == False or int(age) < 0:
                return jsonify({'status': 'error', 'message': 'Age must be a positive integer'}), 400
            elif '@' not in email or '.' not in email:
                return jsonify({'status': 'error', 'message': 'Invalid email format'}), 400
            elif contact.isdigit() == False or len(contact) != 10:
                return jsonify({'status': 'error', 'message': 'Contact must be a 10-digit number'}), 400
            else:
                cur = con.cursor()
                cur.execute(f""" UPDATE users SET name = '{name}', age = '{age}', dob = '{dob}', email = '{email}', contact = '{contact}'
                            WHERE username = '{username}';""")
                con.commit()
                cur.close()

                session['name'] = name
                session['age'] = age
                session['dob'] = dob
                session['email'] = email
                session['contact'] = contact

                return jsonify({'status': 'success', 'message': 'Profile updated successfully'})
        
        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400
    
    return render_template('update.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

        

if __name__ == "__main__":
    app.run(debug = True)