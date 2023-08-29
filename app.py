from flask import Flask, jsonify, render_template
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)

# JWT config
app.config['JWT_SECRET_KEY'] = 'sfwjnONFQION3128Y3T471'

# SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gabo:papa1234@localhost:5432/anime'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to silence a warning

db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

class BaseModel(db.Model):
    __abstract__ = True  # Esta es una clase base y no debe ser mapeada a una tabla en la DB.

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class UserModel(BaseModel):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)  # Usernames are unique
    password_hash = Column(String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json(self):
        return {'id': self.id, 'username': self.username}  # We don't return the password

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

anime_categories = Table('anime_categories', db.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('anime_id', Integer, ForeignKey('anime.id'))
)

class AnimeModel(BaseModel):
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

    def __repr__(self):
        return f"<Anime(title='{self.title}')>"


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

    

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
