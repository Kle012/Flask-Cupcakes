from app import app
from models import db, Cupcake


with app.app_context():
    db.drop_all()
    db.create_all()

app_context = app.app_context()
app_context.push()


c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)

c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)

db.session.add(c1)
db.session.add(c2)
db.session.commit()