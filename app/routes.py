from flask import render_template, redirect, url_for, jsonify, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from .models import User, Artist, Artwork, ArtworksUser, UsersAsArtist, db  # Ensure all necessary models are defined
from . import bcrypt  # Import bcrypt configured in your __init__.py

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html', user=current_user)

    # Routes for artworks by user artists
    @app.route('/user-artworks')
    @login_required
    def user_artworks():
        artworks = ArtworksUser.query.all()
        return render_template('user_artworks.html', artworks=artworks)

    @app.route('/user-artwork/<int:artwork_id>')
    @login_required
    def user_artwork_detail(artwork_id):
        artwork = ArtworksUser.query.get_or_404(artwork_id)
        return render_template('user_artwork_detail.html', artwork=artwork)

    @app.route('/user-artist/<int:artist_id>')
    @login_required
    def user_artist_detail(artist_id):
        artist = UsersAsArtist.query.get_or_404(artist_id)
        artworks = artist.artworks_users.all()
        return render_template('user_artist_detail.html', artist=artist, artworks=artworks)

    # Routes for historic artworks
    @app.route('/historic-artworks')
    @login_required
    def historic_artworks():
        artworks = Artwork.query.all()
        return render_template('historic_artworks.html', artworks=artworks)

    @app.route('/historic-artwork/<int:artwork_id>')
    @login_required
    def historic_artwork_detail(artwork_id):
        artwork = Artwork.query.get_or_404(artwork_id)
        return render_template('historic_artwork_detail.html', artwork=artwork)

    @app.route('/historic-artist/<int:artist_id>')
    @login_required
    def historic_artist_detail(artist_id):
        artist = Artist.query.get_or_404(artist_id)
        artworks = artist.artworks.all()
        return render_template('historic_artist_detail.html', artist=artist, artworks=artworks)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            print("Username:", username)
            print("Password:", password)
            user = User.query.filter_by(username=username).first()
            if user:
                print("User found in database")
            else:
                print("User not found in database")

            if user and bcrypt.check_password_hash(user.password, password):
                print("Password correct, logging in")
                login_user(user)
                return redirect(url_for('historic_artworks'))
            else:
                print("Invalid login attempt")
                flash('Invalid username or password.', 'error')
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
        return redirect(url_for('home'))

    @app.route('/account')
    @login_required
    def account():
        return render_template('account.html', user=current_user)

    @app.route('/account/become-artist', methods=['GET', 'POST'])
    @login_required
    def become_artist():
        if request.method == 'POST':
            artist_name = request.form.get('artist_name')
            genre = request.form.get('genre')
            nationality = request.form.get('nationality')
            bio = request.form.get('bio')

            # Check if the user is already registered as an artist
            existing_artist = UsersAsArtist.query.filter_by(id_user=current_user.id).first()
            if existing_artist:
                flash('You are already registered as an artist.', 'info')
                return redirect(url_for('artist_detail', artist_id=existing_artist.id_user))

            # Create a new artist profile linked to the current user
            new_artist = UsersAsArtist(
                id_user=current_user.id,
                artist_name=artist_name,
                genre=genre,
                nationality=nationality,
                bio=bio
            )
            db.session.add(new_artist)
            db.session.commit()
            flash('You have successfully registered as an artist!', 'success')
            return redirect(url_for('artist_detail', artist_id=new_artist.id_user))
        
        return render_template('artist_registration.html')

