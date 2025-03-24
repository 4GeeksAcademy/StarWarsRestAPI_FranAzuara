"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorito
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_user():
    user= User.query.all()

    all_user= list(map(lambda x: x.serialize(),user))

    return jsonify(all_user), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planets= Planet.query.all()

    all_planets= list(map(lambda x: x.serialize(),planets))

    return jsonify(all_planets), 200


@app.route('/planet/<planet_id>', methods=['GET'])
def get_single_planet(id):
    single_planet= Planet.query.all(id)

    return jsonify(single_planet), 200



@app.route('/people', methods=['GET'])
def get_people():
    people= People.query.all()

    all_people= list(map(lambda x: x.serialize(),people))

    return jsonify(all_people), 200



@app.route('/people/<people_id>', methods=['GET'])
def get_single_people(id):
    single_person= People.query.all(id)

    return jsonify(single_person), 200


@app.route('/users/favorito', methods=['GET'])
def get_favoritos():

    data = request.get_json()
    favoritos = Favorito.query.all()
    favoritos_serialized = [favorito.serialize() for favorito in favoritos]
    return jsonify(favoritos_serialized), 200 

@app.route('/favorito/planet/<planet_id>', methods=['POST'])
def add_planet_favorito():
    data = request.get_json()
    planet_id = data.get("planet_id")

    exist = Favorito.query.filter_by(user_id = data["user_id"], planet_id=planet_id).first()
    if exist:
        return jsonify({"error": "El planeta ya está en favoritos"}), 400

    new_favorito = Favorito(
        planet_id=planet_id,
        user_id= data["user_id"]
    )
    db.session.add(new_favorito)
    db.session.commit()
    return jsonify({"msg": "Favorito añadido"}), 201

@app.route('/favorito/planet/<planet_id>', methods=['DELETE'])
def delete_planet_favorito(planet_id):
    data = request.get_json()
    favorito = Favorito.query.filter_by(user_id = data["user_id"], planet_id = planet_id).first()
    db.session.delete(favorito)
    db.session.commit()
    
    return jsonify({"message": "Favorito eliminado"}), 200



@app.route('/favorito/people/<people_id>', methods=['POST'])
def add_people_favorito():
    data = request.get_json()
    people_id = data.get("people_id")

    exist = Favorito.query.filter_by(user_id = data["user_id"], people_id=people_id).first()
    if exist:
        return jsonify({"error": "El personaje ya está en favoritos"}), 400

    new_favorito = Favorito(
        people_id=people_id,
        user_id= data["user_id"]
    )
    db.session.add(new_favorito)
    db.session.commit()
    return jsonify({"msg": "Favorito añadido"}), 201

@app.route('/favorito/people/<people_id>', methods=['DELETE'])
def delete_people_favorito(people_id):
    data = request.get_json()
    favorito = Favorito.query.filter_by(user_id = data["user_id"], people_id = people_id).first()
    db.session.delete(favorito)
    db.session.commit()
    
    return jsonify({"message": "Favorito eliminado"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
