from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/')
def index():
    return "Welcome to the Flask App!"

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.name for user in users]})

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.json['name']
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!'}), 201

if __name__ == '__main__':
    db.create_all()  # This creates all tables based on the models defined
    app.run(debug=True)






#Manage userpassword
import bcrypt

def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def check_password(hashed_password, user_password):
    # Check if the provided password matches the stored hashed password
    return bcrypt.checkpw(user_password.encode(), hashed_password)

# Example usage
password = "my_secret_password"
hashed = hash_password(password)
print("Hashed:", hashed)

# Check the password
is_correct = check_password(hashed, "my_secret_password")
print("Password correct:", is_correct)