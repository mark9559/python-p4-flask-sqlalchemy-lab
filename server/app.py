#!/usr/bin/env python3
# app.py

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get_or_404(id)  # Fetch the animal by ID or return 404 if not found
    zookeeper = animal.zookeeper  # Get the zookeeper associated with this animal
    enclosure = animal.enclosure  # Get the enclosure associated with this animal

    # Create a response containing the details to display
    response = f"""
        <h1>{animal.name} Details</h1>
        <ul>
            <li>Name: {animal.name}</li>
            <li>Species: {animal.species}</li>
            <li>Zookeeper: {zookeeper.name}</li>
            <li>Enclosure: {enclosure.environment} ({'Open' if enclosure.open_to_visitors else 'Closed'} to Visitors)</li>
        </ul>
    """
    return make_response(response)


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id)  # Fetch the zookeeper by ID or return 404 if not found
    animals = zookeeper.animals  # Get the animals associated with this zookeeper

    # Create a response containing the details to display
    response = f"""
        <h1>{zookeeper.name} Details</h1>
        <ul>
            <li>Name: {zookeeper.name}</li>
            <li>Birthday: {zookeeper.birthday}</li>
            <li>Animals under care:</li>
            <ul>
    """
    for animal in animals:
        response += f"<li>{animal.name} - {animal.species}</li>"
    response += """
            </ul>
        </ul>
    """
    return make_response(response)



@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get_or_404(id)
    animals = enclosure.animals

    response = f"""
        <h1>Enclosure Details</h1>
        <ul>
            <li>Environment: {enclosure.environment}</li>
            <li>Open to Visitors: {'Yes' if enclosure.open_to_visitors else 'No'}</li>
            <li>Animals in the enclosure:</li>
            <ul>
    """
    for animal in animals:
        response += f"<li>{animal.name} - {animal.species}</li>"
    response += """
            </ul>
        </ul>
    """
    return make_response(response)




if __name__ == '__main__':
    app.run(port=5555, debug=True)
