from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class UserModel(BaseModel):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {'id': self.id, 'username': self.username}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def __repr__(self):
        return f"<User(username='{self.username}')>"

class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)

    animes = relationship('AnimeModel', secondary='anime_categories', back_populates='categories')

    def __repr__(self):
        return f"<Category(name='{self.name}')>"
    
    def json(self):
        return {'id': self.id, 'name': self.name}
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

anime_categories = Table('anime_categories', db.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('anime_id', Integer, ForeignKey('anime.id'))
)

class AnimeModel(BaseModel):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False, unique=True)
    rating = Column(Float, nullable=False)
    reviews = Column(Integer, nullable=False)
    seasons = Column(Integer, nullable=False)
    type = Column(String(80), nullable=False)
    poster = Column(String(255), nullable=False)

    categories = relationship('CategoryModel', secondary=anime_categories, back_populates='animes')

    def __init__(self, title, rating, reviews, seasons, type, poster):
        self.title = title
        self.rating = rating
        self.reviews = reviews
        self.seasons = seasons
        self.type = type
        self.poster = poster

    def json(self):
        return {
            'id': self.id, 
            'title': self.title, 
            'rating': self.rating, 
            'reviews': self.reviews, 
            'seasons': self.seasons, 
            'type': self.type, 
            'poster': self.poster,
            'categories': [category.json() for category in self.categories]
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def __repr__(self):
        return f"<Anime(title='{self.title}')>"