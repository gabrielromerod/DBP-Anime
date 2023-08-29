from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager
from models import db
from resources import Login, Register, Anime, Category
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuraciones
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback_default_secret_key')

# Configuración de la base de datos
conn_str = os.environ.get('AZURE_POSTGRESQL_CONNECTIONSTRING')
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{conn_str_params['user']}:{conn_str_params['password']}@{conn_str_params['host']}/{conn_str_params['dbname']}"
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

