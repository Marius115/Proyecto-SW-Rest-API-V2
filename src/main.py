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
from models import db, User,Character,Planet,Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

#Endpoint para el o los usuarios
@app.route('/user', methods=['GET'])
def user_list():

	user = User.query.all()
	all_users = list(map(
        lambda user: user.serialize(),user))
        
	return jsonify(all_users), 200

# Endpoints de todos los characters y del character individual

@app.route('/character', methods=['GET'])
def character_list():
   
    character = Character.query.all()
    all_characters = list(map(
        lambda character: character.serialize(),character)) 
    
    return jsonify(all_characters), 200
    

@app.route('/character/<int:character_id>', methods=['PUT', 'GET'])
def get_single_character(character_id):
    body = request.get_json() 
    if request.method == 'PUT':
        single_character = Character.query.get(character_id)
        single_character.name = body.name
        db.session.commit()
    if request.method == 'GET':
        single_character = Character.query.get(character_id)
        return jsonify(single_character.serialize()), 200


 # Endpoints de todos los planets y de planet individual
@app.route('/planet', methods=['GET'])
def planet_list():
   
    planet = Planet.query.all()
    all_planets = list(map(
        lambda planet: planet.serialize(),planet)) 
    
    return jsonify(all_planets), 200

@app.route('/planet/<int:planet_id>', methods=['PUT', 'GET'])
def get_single_planet(planet_id):
    body = request.get_json() #{ 'username': 'new_username'}
    if request.method == 'PUT':
        single_planet = Planet.query.get(planet_id)
        single_planet.name = body.name
        db.session.commit()
    if request.method == 'GET':
        single_planet = Planet.query.get(planet_id)
        return jsonify(single_planet.serialize()), 200

#Endpoint de favorites:
@app.route('/user/favorite', methods=['GET'])
def handle_favorite():

    favorite = Favorite.query.all()
    all_favorites = list(map(
        lambda favorite: favorite.serialize(),favorite))
    return jsonify(all_favorites), 200


@app.route('/favorite/planet/<int:planet_id>',methods=['POST'])
def add_planet_favorite(planet_id):

	body = request.get_json()
	new_favorite = Favorite(
		user_id=body["user_id"],
		planet_id=body["planet_id"],
		)
	db.session.add(new_favorite)
	db.session.commit()
	return jsonify(new_favorite.serialize()), 200


@app.route('/favorite/character/<int:character_id>',methods=['POST'])
def add_character_favorite(character_id):

	body = request.get_json()
	new_favorite = Favorite(
		user_id=body["user_id"],
		character_id=body["character_id"],
		)
	db.session.add(new_favorite)
	db.session.commit()
	return jsonify(new_favorite.serialize()), 200


@app.route('/user/<int:user_id>/favorite', methods=['GET'])
def handle_user_fav(user_id):

    favorites = Favorite.query.filter_by(user_id=user_id)
    return jsonify([fav.serialize() for fav in favorites]), 200






# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
