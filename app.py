from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Search for recipes matching ANY ingredient    

def search_recipes_any_ingredients(ingredients):
    ingredient_list = [i.strip() for i in ingredients.split(',') if i.strip()]
    all_recipes = []
    seen_ids = set()

    for ing in ingredient_list:
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ing}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['meals']:
                for meal in data['meals']:
                    if meal['idMeal'] not in seen_ids:
                        all_recipes.append(meal)
                        seen_ids.add(meal['idMeal'])

    return all_recipes

def fetch_meal_details(meal_id):
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    response = requests.get(url)
    data = response.json()
    return data['meals'][0] if data['meals'] else {}

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        if ingredients:
            recipes = search_recipes_any_ingredients(ingredients)
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<meal_id>')
def recipe_detail(meal_id):
    recipe = fetch_meal_details(meal_id)
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
