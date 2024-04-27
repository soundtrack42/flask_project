from flask import render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user, login_user, logout_user
from .models import User, Artist, Artwork, db  # Ensure all necessary models are defined
from . import bcrypt  # Import bcrypt configured in your __init__.py

def init_routes(app):

    @app.route('/')
    def home():
        return render_template('home.html', user=current_user)

    @app.route('/all_artworks')
    @login_required
    def all_artworks():
        artworks = Artwork.query.all()  # Assuming Artwork model has needed fields
        return render_template('all_artworks.html', artworks=artworks)

    @app.route('/historic_artworks')
    @login_required
    def historic_artworks():
        artworks = Artwork.query.filter(Artwork.is_historic == True).all()
        return render_template('historic_artworks.html', artworks=artworks)

    @app.route('/artwork/<int:artwork_id>')
    @login_required
    def artwork_detail(artwork_id):
        artwork = Artwork.query.get_or_404(artwork_id)
        return render_template('artwork_detail.html', artwork=artwork)

    @app.route('/artist/<int:artist_id>')
    @login_required
    def artist_detail(artist_id):
        artist = Artist.query.get_or_404(artist_id)
        artworks = artist.artworks.all()  # Assuming a relationship defined in models
        return render_template('artist_detail.html', artist=artist, artworks=artworks)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                error = "Invalid username or password."
                return render_template('login.html', error=error)
        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            bio = request.form.get('bio', None)
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, password=hashed_password, bio=bio)
                db.session.add(new_user)
                db.session.commit()
                flash('User successfully registered. You can now log in.')
                return redirect(url_for('login'))
        return render_template('signup.html')

    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/account')
    @login_required
    def account():
        return render_template('account.html', user=current_user)

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify({'users': [user.username for user in users]})

    @app.route('/add_user', methods=['POST'])
    def add_user():
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            bio = data.get('bio', None)
            if not username or not password:
                return jsonify({'message': 'Username and password are required'}), 400
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password, bio=bio)
            db.session.add(new_user)
            try:
                db.session.commit()
                return jsonify({'message': 'User added successfully'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500
        return jsonify({'message': 'Request must be JSON'}), 400
