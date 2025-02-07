from models import db, Planet
from app import app

with app.app_context():
    planet_1= Planet(name="Tatooine")
    planet_2= Planet(name="Naboo")

    db.session.add(planet_1)
    db.session.add(planet_2)

    db.session.commit()