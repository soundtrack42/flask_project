from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from .models import User, Artist, Artwork, ArtworksUser, UsersAsArtist, db
from . import bcrypt
from werkzeug.utils import secure_filename
import os

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html', user=current_user)

    @app.route('/user-artworks')
    @login_required
    def user_artworks():
        # Fetch artworks created by the current logged-in user as an artist
        artworks = db.session.query(ArtworksUser).join(UsersAsArtist).all()
        
        # Adjust artist names for filesystem paths
        for artwork in artworks:
            if artwork.users_as_artist:
                # Temporarily adjust the artist's name for filesystem paths
                artwork.users_as_artist.artist_name = artwork.users_as_artist.artist_name.replace(" ", "_")
        return render_template('user_artworks.html', artworks=artworks)

    @app.route('/user-artist/<int:artist_user_id>')
    @login_required
    def user_artist_detail(artist_user_id):
        # Fetch an artist profile and their artworks, ensuring it belongs to the current user
        artist = UsersAsArtist.query.get_or_404(artist_user_id)
        return render_template('user_artist_detail.html', artist=artist)

    @app.route('/user-artwork/<int:artist_user_id>/<string:painting_name>')
    @login_required
    def user_artwork(artist_user_id, painting_name):
        # Fetch the specific user artwork
        artwork = ArtworksUser.query.filter_by(artist_user_id=artist_user_id, painting_name=painting_name).first()
        if not artwork:
            abort(404)  # If no artwork is found, return a 404 error

        # Check if the artwork has an associated artist and replace spaces in full name
        if artwork.users_as_artist:
            file_system_name = artwork.users_as_artist.artist_name.replace(" ", "_")
        else:
            file_system_name = None  # Handle cases where there may not be an associated artist

        return render_template('user_artwork.html', artwork=artwork, file_system_name=file_system_name)

    @app.route('/historic-artworks')
    @login_required
    def historic_artworks():
        # Join Artwork with Artist to fetch necessary data
        artworks = db.session.query(Artwork).join(Artist).all()

        for artwork in artworks:
            if artwork.artist:
                # Replace spaces with underscores in the artist's full name for file system compatibility
                artwork.artist.full_name = artwork.artist.full_name.replace(" ", "_")
        return render_template('historic_artworks.html', artworks=artworks)

    @app.route('/historic-artist/<int:artist_id>')
    @login_required
    def historic_artist_detail(artist_id):
        # Fetch an historic artist and their artworks by artist_id
        artist = Artist.query.get_or_404(artist_id)
        return render_template('historic_artist_detail.html', artist=artist)

    @app.route('/historic-artwork/<int:artist_id>/<string:painting_name>')
    @login_required
    def historic_artwork(artist_id, painting_name):
        # Fetch the specific artwork
        artwork = Artwork.query.filter_by(artist_id=artist_id, painting_name=painting_name).first()
        if not artwork:
            abort(404)  # If no artwork is found, return a 404 error

        # Check if the artwork has an associated artist and replace spaces in full name
        if artwork.artist:
            file_system_name = artwork.artist.full_name.replace(" ", "_")
        else:
            file_system_name = None  # Handle cases where there may not be an associated artist

        return render_template('historic_artwork.html', artwork=artwork, file_system_name=file_system_name)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('historic_artworks'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next') or url_for('historic_artworks')
                return redirect(next_page)
            else:
                flash('Login failed. Check your username and password.', 'error')
        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for('historic_artworks'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
            else:
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
        return render_template('signup.html')

    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/account')
    @login_required
    def account():
        return render_template('account.html', user=current_user)

    @app.route('/upload-artwork/<int:artist_user_id>', methods=['GET', 'POST'])
    @login_required
    def upload_artwork(artist_user_id):
        artist = UsersAsArtist.query.get_or_404(artist_user_id)
        if artist.id_user != current_user.id:
            flash('You are not authorized to upload artwork for this artist.', 'error')
            return redirect(url_for('user_artworks'))

        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                artist_name = artist.artist_name.replace(" ", "_")
                directory = os.path.join(app.root_path, 'static', 'user_images', artist_name)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file_path = os.path.join(directory, filename)
                file.save(file_path)

                # Create a new artwork record in the database
                new_artwork = ArtworksUser(painting_name=filename, artist_user_id=artist_user_id)
                db.session.add(new_artwork)
                db.session.commit()

                flash('Artwork uploaded successfully!', 'success')
                return redirect(url_for('user_artworks'))
        return render_template('upload_artwork.html', artist=artist)

    @app.route('/account/become-artist', methods=['GET', 'POST'])
    @login_required
    def become_artist():
        if request.method == 'POST':
            artist_name = request.form['artist_name']
            genre = request.form['genre']
            nationality = request.form['nationality']
            bio = request.form.get('bio', None)

            existing_artist = UsersAsArtist.query.filter_by(id_user=current_user.id).first()
            if existing_artist:
                flash('You are already registered as an artist.', 'info')
                # Redirect to the specific user artist detail page using the artist's user ID
                return redirect(url_for('user_artist_detail', artist_user_id=existing_artist.id_user))

            new_artist = UsersAsArtist(id_user=current_user.id, artist_name=artist_name, genre=genre, nationality=nationality, bio=bio)
            db.session.add(new_artist)
            db.session.commit()

            # Create directory for the artist in the static folder
            directory_path = os.path.join(app.root_path, 'static', 'user_images', secure_filename(artist_name.replace(" ", "_")))
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            
            flash('Artist profile created successfully!', 'success')
            return redirect(url_for('user_artist_detail', artist_user_id=new_artist.id_user))

        return render_template('artist_registration.html')
