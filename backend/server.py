from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:umdMinnehack2021@34.203.31.126:5432/minnehack"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "wow"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    packaging = db.Column(db.String)
    
    def __init__(self, name, packaging):
        self.name = name
        self.packaging = packaging

    def __repr__(self):
        return f"<Product {self.name}>"