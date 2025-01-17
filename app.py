# Import flask
from flask import Flask, jsonify, request
from models import db, Recipe, IngredientQuantity

# Initialize a Flask object
app = Flask(__name__)

# Configure the database location
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipes.db"

# We initialize the database connection
db.init_app(app)


def convert_recipe_to_dict(recipe):
    return {
        "id": recipe.id,
        "name": recipe.name,
        "description": recipe.description,
        "preparation": f"{recipe.preparation_time} min",
        "ingredients": [
            f"{ingredient.quantity} {ingredient.name}"
            for ingredient in recipe.ingredients
        ],
    }


@app.route("/recipes")
def get_recipes():
    return_recipies = []
    recipes = Recipe.query.all()
    for recipe in recipes:
        recipe_dict = convert_recipe_to_dict(recipe)
        return_recipies.append(recipe_dict)
    return jsonify(return_recipies)


@app.route("/recipes/<int:id>")
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return_recipe = convert_recipe_to_dict(recipe)
    return jsonify(return_recipe)


@app.route("/recipes", methods=["POST"])
def create_recipe():
    # HTTP Body data (as JSON)
    data = request.get_json()
    # Unpacking data from JSON
    recipe_name = data.get("name")
    recipe_description = data.get("description")
    recipe_preparation = data.get("preparation")
    ingredients = data.get("ingredients")

    # Creating IngredientQuantity objects
    ingredients_list = []
    for ingredient in ingredients:
        ingredient_name = ingredient.get("name")
        ingredient_quantity = ingredient.get("quantity")
        ingredient_obj = IngredientQuantity(
            name=ingredient_name, quantity=ingredient_quantity
        )
        ingredients_list.append(ingredient_obj)

    recipe_obj = Recipe(
        name=recipe_name,
        description=recipe_description,
        preparation_time=recipe_preparation,
        ingredients=ingredients_list,
    )
    db.session.add(recipe_obj)
    db.session.add_all(ingredients_list)

    db.session.commit()

    return jsonify("Recipe created"), 201


@app.route("/recipes/<int:id>", methods=["PUT"])
def update_recipe(id):
    # Get recipe from database
    recipe = Recipe.query.get_or_404(id)
    # HTTP Body data (as JSON)
    data = request.get_json()
    # Unpacking data from JSON
    recipe_name = data.get("name")
    recipe_description = data.get("description")
    recipe_preparation = data.get("preparation")

    if not recipe_preparation:
        return jsonify({"error": "Please specify preparation time"}), 400
    ingredients = data.get("ingredients")

    # Creating IngredientQuantity objects
    ingredients_list = []
    for ingredient in ingredients:
        ingredient_name = ingredient.get("name")
        ingredient_quantity = ingredient.get("quantity")
        ingredient_obj = IngredientQuantity(
            name=ingredient_name, quantity=ingredient_quantity
        )
        ingredients_list.append(ingredient_obj)

    recipe.name = recipe_name
    recipe.description = recipe_description
    recipe.preparation_time = recipe_preparation
    # Delete ingredients then add the new ones
    for recipe_ingredient in recipe.ingredients:
        db.session.delete(recipe_ingredient)
    recipe.ingredients = ingredients_list

    db.session.add_all(ingredients_list)
    db.session.commit()

    return jsonify("Recipe updated")


if __name__ == "__main__":
    app.run()
