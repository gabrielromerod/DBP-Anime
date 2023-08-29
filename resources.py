from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, create_access_token
from models import UserModel, CategoryModel, AnimeModel

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

class Anime(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', type=str, required=True, help='This field cannot be blank.')
    post_parser.add_argument('rating', type=float, required=True, help='This field cannot be blank.')
    post_parser.add_argument('reviews', type=int, required=True, help='This field cannot be blank.')
    post_parser.add_argument('seasons', type=int, required=True, help='This field cannot be blank.')
    post_parser.add_argument('type', type=str, required=True, help='This field cannot be blank.')
    post_parser.add_argument('poster', type=str, required=True, help='This field cannot be blank.')
    post_parser.add_argument('categories', type=str, action='append', required=True, help='At least one category is required.')

    patch_parser = reqparse.RequestParser()
    patch_parser.add_argument('title', type=str, required=False)
    patch_parser.add_argument('rating', type=float, required=False)
    patch_parser.add_argument('reviews', type=int, required=False)
    patch_parser.add_argument('seasons', type=int, required=False)
    patch_parser.add_argument('type', type=str, required=False)
    patch_parser.add_argument('poster', type=str, required=False)
    patch_parser.add_argument('categories', type=str, action='append', required=False)

    @jwt_required()
    def get(self, id=None):
        if id:
            anime = AnimeModel.find_by_id(id)
            if anime:
                return anime.json(), 200
            return {'message': 'Anime not found'}, 404
        return {'animes': [anime.json() for anime in AnimeModel.query.all()]}, 200
    
    @jwt_required()
    def post(self):
        data = Anime.post_parser.parse_args()

        if AnimeModel.find_by_title(data['title']):
            return {'message': 'An anime with that title already exists'}, 400
        
        category_names = data['categories']
        category_objects = []

        for name in category_names:
            category = CategoryModel.query.filter_by(name=name).first()
            if category:
                category_objects.append(category)
            else:
                return {'message': f'Category {name} not found'}, 404

        del data['categories']

        anime = AnimeModel(**data)
        anime.categories.extend(category_objects)
        anime.save_to_db()

        return anime.json(), 201

    @jwt_required()
    def patch(self, id):
        data = Anime.patch_parser.parse_args()

        anime = AnimeModel.find_by_id(id)
        if anime is None:
            return {'message': 'Anime not found'}, 404

        if data['title']:
            anime.title = data['title']
        if data['rating'] is not None:
            anime.rating = data['rating']
        if data['reviews'] is not None:
            anime.reviews = data['reviews']
        if data['seasons'] is not None:
            anime.seasons = data['seasons']
        if data['type']:
            anime.type = data['type']
        if data['poster']:
            anime.poster = data['poster']

        if data['categories']:
            anime.categories.clear()
            category_objects = []
            for name in data['categories']:
                category = CategoryModel.query.filter_by(name=name).first()
                if category:
                    category_objects.append(category)
                else:
                    return {'message': f'Category {name} not found'}, 404
            anime.categories.extend(category_objects)

        anime.save_to_db()
        return anime.json(), 200

    @jwt_required()
    def delete(self, id):
        anime = AnimeModel.find_by_id(id)
        if anime:
            anime.delete_from_db()
            return {'message': 'Anime deleted'}, 200
        return {'message': 'Anime not found'}, 404
    
    @jwt_required()
    def put(self, id):
        data = Anime.post_parser.parse_args()

        anime = AnimeModel.find_by_id(id)

        if anime is None:
            return {'message': 'Anime not found'}, 404
        
        category_names = data['categories']

        category_objects = []

        for name in category_names:
            category = CategoryModel.query.filter_by(name=name).first()
            if category:
                category_objects.append(category)
            else:
                return {'message': f'Category {name} not found'}, 404
            
        anime.title = data['title']
        anime.rating = data['rating']
        anime.reviews = data['reviews']
        anime.seasons = data['seasons']
        anime.type = data['type']
        anime.poster = data['poster']
        anime.categories.clear()
        anime.categories.extend(category_objects)
        anime.save_to_db()
        return anime.json(), 200

class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='This field cannot be blank.')

    @jwt_required()
    def get(self, id=None):
        if id:
            category = CategoryModel.find_by_id(id)
            if category:
                return category.json(), 200
            return {'message': 'Category not found'}, 404
        return {'categories': [category.json() for category in CategoryModel.query.all()]}, 200

    @jwt_required()
    def post(self):
        data = Category.parser.parse_args()

        if CategoryModel.find_by_name(data['name']):
            return {'message': 'A category with that name already exists'}, 400

        category = CategoryModel(**data)
        category.save_to_db()

        return category.json(), 201

    @jwt_required()
    def delete(self, id):
        category = CategoryModel.find_by_id(id)
        if category:
            category.delete_from_db()
            return {'message': 'Category deleted'}, 200
        return {'message': 'Category not found'}, 404

    @jwt_required()
    def put(self, id):
        data = Category.parser.parse_args()

        category = CategoryModel.find_by_id(id)

        if category is None:
            return {'message': 'Category not found'}, 404

        category.name = data['name']
        category.save_to_db()
        return category.json(), 200
    
    @jwt_required()
    def patch(self, id):
        data = Category.parser.parse_args()

        category = CategoryModel.find_by_id(id)
        if category is None:
            return {'message': 'Category not found'}, 404

        if data['name']:
            category.name = data['name']

        category.save_to_db()
        return category.json(), 200