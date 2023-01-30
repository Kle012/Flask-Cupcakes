"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def homepage():
    """Show empty cupcakes list and a new cupcake form."""
    cupcakes = Cupcake.query.all()
    return render_template('homepage.html', cupcakes = cupcakes)

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """
    Get data about all cupcakes.
    Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
    """
    cupcakes = [c.serialized() for c in Cupcake.query.all()]
    return jsonify (cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def list_single_dessert(id):
    """
    Get data about a single cupcake.
    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    """
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify (cupcake=cupcake.serialized())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request.
    Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}.
    """
    data = request.json

    new_cupcake = Cupcake (
        flavor=data["flavor"], 
        size=data["size"], 
        rating=data["rating"], 
        image=data.get("image", None)
    )
    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify (cupcake=new_cupcake.serialized()), 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update a cupcake. This should raise a 404 if the cupcake cannot be found.
    Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.
    """
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    db.session.commit()
    return jsonify (cupcake = cupcake.serialized())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete cupcake. This should raise a 404 if the cupcake cannot be found.
    Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.
    """
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message = 'Deleted')
