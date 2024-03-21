# recipes-crud

This app should be able to store recipes, to read recipes that you just added, edit and delete them.

This app is written in Flask.

`pip install flask`

and it uses SQLAlchemy as ORM.

`pip install flask_sqlalchemy`

# TODO:
- Add delete endpoint
- Add parameters validation (create and update endpoints)
  - recipe name, description, preparation
  - ingredients name and quantity
- Add search endpoint (search recipe by name)
- Add get pagination (example: count: 20) -> "get recipes, 20 per get"
- Fix return messages to return
  - succes: `{'message': 'success message}`
  - error: `{'error': 'error message'}`
- Add `requirements.txt`
- Update `README.md`
- Recipes should be unique. Check before adding a new recipe if it already exists
- Create `/recipes/export` function, which will export all the recipes in a desired format
- Create parameters for export function like:
  - recipe name. (example: `pasta`)
  - recipe preparation (example: under 30 mins)
  - recipe ingredients (example: not more than 5 ingredients)
  - recipe difficulty (example: easy, medium, hard)
  - export time (example: `.csv, .json, .xml, .txt`)
- Create new Recipe attributes (like `difficulty` and `servings`)
- BONUS (run black code formatter)
- BONUS (create some unit tests) - read about unit tests
