from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from os import environ
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///default.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Needed for session management

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define a model
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    death_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(255))
    nationality = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    wikipedia_link = db.Column(db.String(255), nullable=False)
    number_paintings = db.Column(db.Integer, default=0)
    draws = relationship('Draw', backref='artist', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    likes = relationship('Like', backref='user', lazy=True)
    users_as_artists = relationship('UsersAsArtist', backref='user', uselist=False)

class Draw(db.Model):
    painting_name = db.Column(db.String(255), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    likes = relationship('Like', backref='draw', lazy='dynamic')

class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('draw.artist_id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class UsersAsArtist(db.Model):
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    artist_name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255))
    nationality = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    draws_users = relationship('DrawsUser', backref='users_as_artist', lazy=True)

class DrawsUser(db.Model):
    painting_name = db.Column(db.String(255), nullable=False)
    artist_user_id = db.Column(db.Integer, db.ForeignKey('users_as_artist.id_user'), primary_key=True)
    likes_artists_users = relationship('LikesArtistsUser', backref='draws_user', lazy='dynamic')

class LikesArtistsUser(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_user_id = db.Column(db.Integer, db.ForeignKey('draws_user.artist_user_id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


#routes
@app.route('/')
def index():
    return "Welcome to the Flask App!"

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.name for user in users]})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        bio = data.get('bio', None)  # Optional bio field

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password, bio=bio)

        db.session.add(new_user)
        try:
            db.session.commit()
            return jsonify({'message': 'User added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Request must be JSON'}), 400


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    return jsonify({'message': 'Request must be JSON'}), 400


@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()  # This creates all tables based on the models defined
    app.run(debug=True)

