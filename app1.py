from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
import redis
from flask_jwt_extended import decode_token

cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
blacklist = set()

app = Flask(__name__)
app.secret_key = 'secret-key-112326'

app.config['JWT_SECRET_KEY'] = 'JWT-auth-token-256' 
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('usersdb')
records = db.users

@app.route('/')
def home():

    token = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        token = request.args.get("token")

    if not token:
        return redirect(url_for('login'))

    try:
        decoded_token = decode_token(token)
        username = decoded_token['sub']
        stored_token = cache.get(f"token:{username}")
        if stored_token != token:
            return jsonify({'status': 'error', 'message': 'Token is invalid or expired'}), 401
    except Exception as e:
        print("JWT Error:", e)
        return redirect(url_for('login'))
    
    user = cache.hgetall(f"user:{username}") 

    if not user:
        db_user = records.find_one({"username": username})
        if db_user:
            user = {
                'username': db_user['username'],
                'name': db_user['name'],
                'age': db_user['age'],
                'email': db_user['email'],
                'dob': db_user['dob'],
                'contact': db_user['contact']
            }
        else:
            return redirect(url_for('login'))

    return render_template('home.html', **user)


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
                access_token = create_access_token(identity=username)
                cache.set(f"token:{username}", access_token)
                return jsonify({'status': 'success', 'access_token': access_token})
            
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

    if request.method == 'POST':

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'status': 'error', 'message': 'Missing token'}), 401

        token = auth_header.split(" ")[1]

        try:
            decoded_token = decode_token(token)
            username = decoded_token['sub']

            stored_token = cache.get(f"token:{username}")
            if stored_token != token:
                return jsonify({'status': 'error', 'message': 'Token is invalid or expired'}), 401
            
        except Exception as e:
            print("JWT Error:", e)
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        
        if request.is_json:
            data = request.get_json()
            name = data.get('name', '')
            age = data.get('age', '')
            dob = data.get('dob', '')
            email = data.get('email', '')
            contact = data.get('contact', '')

            if name == "":
                return jsonify({'status': 'error', 'message': 'Name cannot be empty'}), 400
            elif not age.isdigit() or int(age) < 0:
                return jsonify({'status': 'error', 'message': 'Age must be a positive integer'}), 400
            elif '@' not in email or '.' not in email:
                return jsonify({'status': 'error', 'message': 'Invalid email format'}), 400
            elif not contact.isdigit() or len(contact) != 10:
                return jsonify({'status': 'error', 'message': 'Contact must be a 10-digit number'}), 400
            
            print("Update starts")
            
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
                'contact': contact
            })

            print("Update Ends")

            return jsonify({'status': 'success', 'message': 'Profile updated successfully'})

        return jsonify({'status': 'error', 'message': 'Invalid request'}), 400
    
    
    return render_template('update.html')



@app.route('/delete', methods=['POST'])
def delete_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'status': 'error', 'message': 'Missing token'}), 401

    token = auth_header.split(" ")[1]

    try:
        decoded_token = decode_token(token)
        username = decoded_token['sub']

        stored_token = cache.get(f"token:{username}")
        if stored_token != token:
            return jsonify({'status': 'error', 'message': 'Token is invalid or expired'}), 401
        
    except Exception as e:
        print("JWT Error:", e)
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

    result = records.delete_one({'username': username})

    if result.deleted_count > 0:
        cache.delete(f"user:{username}")
        cache.delete(f"token:{username}")
        return jsonify({'status': 'success', 'message': 'Profile deleted successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404




@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']  
    blacklist.add(jti)
    cache.delete(f"token:{get_jwt_identity()}")
    return jsonify({'status': 'success', 'message': 'Logged out successfully'})

if __name__ == "__main__":
    app.run(debug=True)
