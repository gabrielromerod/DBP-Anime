from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# JWT config
app.config['JWT_SECRET_KEY'] = 'sfwjnONFQION3128Y3T471'

# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gabo:papa1234@localhost:5432/anime'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to silence a warning

db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

class UserModel(db.Model):    
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)  # Ensuring usernames are unique
    password_hash = Column(String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def register(self):
        # you might need to adjust this later for db.session
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):
        # you might need to adjust this later for db.session
        db.session.add(self)
        db.session.commit()

class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)

    animes = relationship('AnimeModel', secondary='anime_categories', back_populates='categories')

anime_categories = Table('anime_categories', db.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('anime_id', Integer, ForeignKey('anime.id'))
)

class AnimeModel(db.Model):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False, unique=True)
    rating = Column(Float, nullable=False)
    reviews = Column(Integer)
    seasons = Column(Integer, nullable=False)
    type = Column(String(80), nullable=False)
    poster = Column(String(255))

    # Many-to-Many relationship with Category
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
            'poster': self.poster
        }
    
    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):
        # you might need to adjust this later for db.session
        db.session.add(self)
        db.session.commit()

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank.')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank.')

    def post(self):
        data = Login.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401
    
class Register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='This field cannot be blank.')
    parser.add_argument('password', type=str, required=True, help='This field cannot be blank.')

    def post(self):
        data = Register.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201
    
    def get(self):
        return {"For register a user POST to /register with username and password": "POST /register"}, 200

class User(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        return user.json(), 200
    
class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be blank.')

    @jwt_required
    def get(self, category_id):
        category = CategoryModel.find_by_id(category_id)
        if category:
            return category.json(), 200
        return {'message': 'Category not found'}, 404

    @jwt_required
    def post(self, category_id):
        data = Category.parser.parse_args()

        if CategoryModel.find_by_name(data['name']):
            return {'message': 'A category with that name already exists'}, 400

        category = CategoryModel(data['name'])
        category.save_to_db()

        return category.json(), 201

    @jwt_required
    def delete(self, category_id):
        category = CategoryModel.find_by_id(category_id)
        if category:
            category.delete_from_db()
            return {'message': 'Category deleted'}, 200
        return {'message': 'Category not found'}, 404
    
class CategoryList(Resource):
    @jwt_required
    def get(self):
        return {'categories': [category.json() for category in CategoryModel.query.all()]}, 200
    
class Anime(Resource):
    @jwt_required
    def get(self, anime_id):
        anime = AnimeModel.find_by_id(anime_id)
        if anime:
            return anime.json(), 200
        return {'message': 'Anime not found'}, 404
    
    @jwt_required
    def post(self, anime_id):
        data = Anime.parser.parse_args()

        if AnimeModel.find_by_title(data['title']):
            return {'message': 'An anime with that title already exists'}, 400

        anime = AnimeModel(data['title'], data['rating'], data['reviews'], data['seasons'], data['type'], data['poster'])
        anime.save_to_db()

        return anime.json(), 201
    
    @jwt_required
    def delete(self, anime_id):
        anime = AnimeModel.find_by_id(anime_id)
        if anime:
            anime.delete_from_db()
            return {'message': 'Anime deleted'}, 200
        return {'message': 'Anime not found'}, 404
    
    @jwt_required
    def put(self, anime_id):
        data = Anime.parser.parse_args()

        anime = AnimeModel.find_by_id(anime_id)

        if anime:
            anime.title = data['title']
            anime.rating = data['rating']
            anime.reviews = data['reviews']
            anime.seasons = data['seasons']
            anime.type = data['type']
            anime.poster = data['poster']
        else:
            anime = AnimeModel(data['title'], data['rating'], data['reviews'], data['seasons'], data['type'], data['poster'])

        anime.save_to_db()

        return anime.json(), 200
    
    @jwt_required
    def patch(self, anime_id):
        data = Anime.parser.parse_args()

        anime = AnimeModel.find_by_id(anime_id)

        if anime:
            anime.title = data['title'] if data['title'] else anime.title
            anime.rating = data['rating'] if data['rating'] else anime.rating
            anime.reviews = data['reviews'] if data['reviews'] else anime.reviews
            anime.seasons = data['seasons'] if data['seasons'] else anime.seasons
            anime.type = data['type'] if data['type'] else anime.type
            anime.poster = data['poster'] if data['poster'] else anime.poster
        else:
            anime = AnimeModel(data['title'], data['rating'], data['reviews'], data['seasons'], data['type'], data['poster'])

        anime.save_to_db()

        return anime.json(), 200
    
class AnimeList(Resource):
    @jwt_required
    def get(self):
        return {'animes': [anime.json() for anime in AnimeModel.query.all()]}, 200
    

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(User, '/user')
api.add_resource(Category, '/category/<int:category_id>')
api.add_resource(CategoryList, '/categories')
api.add_resource(Anime, '/anime/<int:anime_id>')
api.add_resource(AnimeList, '/animes')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
