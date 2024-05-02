from . import db
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, nullable=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    likes = relationship('Like', backref='user')
    users_as_artists = relationship('UsersAsArtist', backref='user', uselist=False)

    @property
    def is_authenticated(self):
        return True # Assuming all instances represent authenticated users once created

    @property
    def is_active(self):
        return True # This could be a real column in the database if you want to deactivate users

    @property
    def is_anonymous(self):
        return False # Normally False for authenticated users

    def get_id(self):
        return str(self.id) # Return the user ID as a unicode string; Flask-Login requires this to be a string

class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    death_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(255))
    nationality = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    wikipedia_link = db.Column(db.String(255), nullable=False)
    number_paintings = db.Column(db.Integer, default=0)
    artworks = relationship('Artwork', backref='artist')

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    __table_args__ = (
        db.ForeignKeyConstraint(['painting_name', 'artist_id'], ['artworks.painting_name', 'artworks.artist_id']),
    )

class Artwork(db.Model):
    __tablename__ = 'artworks'
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key=True)
    likes = relationship('Like', backref='artwork')

class UsersAsArtist(db.Model):
    __tablename__ = 'users_as_artist'
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    artist_name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255))
    nationality = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    artworks_user = relationship('ArtworksUser', backref='users_as_artist')

class ArtworksUser(db.Model):
    __tablename__ = 'artworks_user'
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_user_id = db.Column(db.Integer, db.ForeignKey('users_as_artist.id_user'), primary_key=True)
    likes_artists_users = relationship('LikesArtistsUser', backref='artworks_user')

class LikesArtistsUser(db.Model):
    __tablename__ = 'likes_artists_user'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_user_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    __table_args__ = (
        db.ForeignKeyConstraint(['painting_name', 'artist_user_id'], ['artworks_user.painting_name', 'artworks_user.artist_user_id']),
    )
