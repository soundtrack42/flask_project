from . import db
from sqlalchemy.orm import relationship

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
    artworks = relationship('Artwork', backref='artist', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    likes = relationship('Like', backref='user', lazy=True)
    users_as_artists = relationship('UsersAsArtist', backref='user', uselist=False)

class Artwork(db.Model):
    painting_name = db.Column(db.String(255), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    likes = relationship('Like', backref='Artwork', lazy='dynamic')

class Like(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artwork.artist_id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class UsersAsArtist(db.Model):
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    artist_name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255))
    nationality = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    artworks_users = relationship('ArtworksUser', backref='users_as_artist', lazy=True)

class ArtworksUser(db.Model):
    painting_name = db.Column(db.String(255), nullable=False)
    artist_user_id = db.Column(db.Integer, db.ForeignKey('users_as_artist.id_user'), primary_key=True)
    likes_artists_users = relationship('LikesArtistsUser', backref='Artworks_user', lazy='dynamic')

class LikesArtistsUser(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_user_id = db.Column(db.Integer, db.ForeignKey('Artworks_user.artist_user_id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())