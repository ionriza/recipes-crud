from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    preparation_time = db.Column(db.Integer, nullable=False)
    ingredients = db.relationship("IngredientQuantity", backref="user", lazy=True)

    def __repr__(self):
        return self.name


class IngredientQuantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)

    def __repr__(self):
        return f"{self.quantity} {self.name}"
