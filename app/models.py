from . import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    likes = relationship('Like', backref='user')
    users_as_artists = relationship('UsersAsArtist', backref='user', uselist=False)

class Artist(db.Model):
    __tablename__ = 'artist'
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

class Like(db.Model):
    __tablename__ = 'like'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    painting_name = db.Column(db.String(255), db.ForeignKey('artwork.painting_name'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artwork.artist_id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Artwork(db.Model):
    __tablename__ = 'artwork'
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    likes = relationship('Like', backref='artwork', lazy='dynamic', foreign_keys=[Like.painting_name, Like.artist_id], primaryjoin="and_(Artwork.painting_name==Like.painting_name, Artwork.artist_id==Like.artist_id)")

class UsersAsArtist(db.Model):
    __tablename__ = 'users_as_artist'
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    artist_name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255))
    nationality = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    artworks_users = relationship('ArtworksUser', backref='users_as_artist', lazy=True)

class ArtworksUser(db.Model):
    __tablename__ = 'artworks_user'
    painting_name = db.Column(db.String(255), primary_key=True)
    artist_user_id = db.Column(db.Integer, db.ForeignKey('users_as_artist.id_user'), primary_key=True)
    likes_artists_users = relationship('LikesArtistsUser', backref='artworks_user', lazy='dynamic', foreign_keys="[LikesArtistsUser.painting_name, LikesArtistsUser.artist_user_id]", primaryjoin="and_(ArtworksUser.painting_name==LikesArtistsUser.painting_name, ArtworksUser.artist_user_id==LikesArtistsUser.artist_user_id)")

class LikesArtistsUser(db.Model):
    __tablename__ = 'likes_artists_user'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    painting_name = db.Column(db.String(255), db.ForeignKey('artworks_user.painting_name'), primary_key=True)
    artist_user_id = db.Column(db.Integer, db.ForeignKey('artworks_user.artist_user_id'))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
