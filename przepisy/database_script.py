import psycopg2

from scpript_for_recipes import get_recipe_information, open_page
from parse_fractions import parse_problematic_numbers


recipe = {
    'name': '',
    'ingredients': [],
    'instructions': ''
}

# POSSIBLE_UNITS = ['g', 'łyżeczki', 'łyszeczka', 'łyżka', 'łyżki', 'szklanka', 'szklanki', ]
# SPICES = ['sól', 'pieprz', 'bazylia', '']

# def get_ingredients_and_quantity(ingredients_list):
#     for elem in ingredients_list:
#         ingredient_information = elem.split()
#         amount = convert_to_int(ingredient_information[0])
#         unit = ingredient_information[1] if ingredient_information[1] in POSSIBLE_UNITS else ''
#         ingredient_name = ingredient_information[2:]
#         print(amount, unit, ingredient_name)


# def convert_to_int(s):
#     try:
#         return int(s)
#     except:
#         return ''


# get_ingredients_and_quantity(ing)
name, ingredients, instructions = get_recipe_information(open_page('https://kuchnialidla.pl/tortille-z-lososiem-wedzonym'))
# ingredients.pop('bułka tarta')
ingredients.pop('sól')
ingredients.pop('pieprz')
# ingredients.pop('sok z cytryny')
# ingredients.pop('sok wyciśnięty z ½ cytryny')
# ingredients.pop('świeże zioła (np. natka pietruszki, szczypiorek, rukiew wodna)')
# ingredients.pop('oliwa z oliwek')
ingredients['sól'] = {'amount': '1', 'unit': 'szczypta'}
ingredients['pieprz'] = {'amount': '1', 'unit': 'szczypta'}
# ingredients['ziemniaki'] = {'amount': '1', 'unit': 'kg'}
# ingredients['oliwa z oliwek'] = {'amount': '1', 'unit': 'łyżka'}
for ing in ingredients:
    # print(ing)
    ingredients[ing]['amount'] = parse_problematic_numbers(ingredients[ing]['amount'])
print(ingredients)


def add_to_database(recipe_name, ingredients_list, recipe_instructions):
    conn = psycopg2.connect('dbname=recipes user=zwa password=thesis')
    cur = conn.cursor()
    select_recipe = "SELECT * FROM zero_waste_app_recipe WHERE name=%s;"
    cur.execute(select_recipe, (recipe_name,))
    recipe_id = cur.fetchone()
    if not recipe_id:
        insert_recipe = 'INSERT INTO zero_waste_app_recipe(name, instructions) VALUES(%s, %s) RETURNING id;'
        cur.execute(insert_recipe, (recipe_name, recipe_instructions))
        recipe_id = cur.fetchone()
    # recipe_id = cur.fetchone()[0]
    for ingredient in ingredients_list:
        select_ingredient = "SELECT * FROM zero_waste_app_product WHERE name=%s;"
        cur.execute(select_ingredient, (ingredient,))
        product = cur.fetchone()
        if not product:
            insert_product = 'INSERT INTO zero_waste_app_product(name) VALUES(%s) RETURNING id;'
            cur.execute(insert_product, (ingredient,))
            product = cur.fetchone()
        insert_recipeingredient = 'INSERT INTO zero_waste_app_recipeingredient(amount, ingredient_id, recipe_id, unit) VALUES(%s, %s, %s, %s) RETURNING id;'
        # select_recipeingredient = 'SELECT * FROM zero_waste_app_recipeingredient WHERE ingredient_id=%s and recipe_id=%s;'
        # cur.execute(select_recipeingredient, (product[0], recipe_id[0]))
        # if not cur.fetchone:
        cur.execute(insert_recipeingredient, (ingredients_list[ingredient]['amount'], product[0], recipe_id[0], ingredients_list[ingredient]['unit']))
    conn.commit()
    cur.close()
    conn.close()


add_to_database(name, ingredients, instructions)

## https://kuchnialidla.pl/przepisy/szybkie/8#lista
## https://kuchnialidla.pl/przepisy/latwy/17#lista
