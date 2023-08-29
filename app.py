from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager
from models import db
from resources import Login, Register, Anime, Category
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Configuraciones

load_dotenv()

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ.get('DBUSER')}:{os.environ.get('DBPASS')}@{os.environ.get('DBHOST')}:{os.environ.get('DBPORT')}/{os.environ.get('DBNAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializaciones
db.init_app(app)
jwt = JWTManager(app)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')
    
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Anime, '/anime', '/anime/<int:id>')
api.add_resource(Category, '/category', '/category/<int:id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
