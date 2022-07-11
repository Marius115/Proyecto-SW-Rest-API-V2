from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "email": self.email,
            "password": self.password
        }

#Character
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    gender = db.Column(db.String(150))
    birth_year = db.Column(db.String(150))
    height = db.Column(db.String(150))

    def __repr__(self):
        return '<Character %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender":self.gender,
            "birth_year":self.birth_year,
            "height":self.height
        }

#Planet
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    terrain = db.Column(db.String(150), nullable=False)
    climate = db.Column(db.String(150), nullable=False)
    population = db.Column(db.String(150))

    def __repr__(self):
        return '<Planet %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "climate": self.climate,
            "population": self.population
        }

#Favorite
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }