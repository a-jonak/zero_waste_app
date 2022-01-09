import psycopg2
from collections import Counter

user_id = 1
conn = psycopg2.connect('dbname=recipes user=zwa password=thesis')
cur = conn.cursor()
select_user_products = "SELECT * FROM zero_waste_app_userproduct WHERE user_id=%s;"
# select_recipe_product = "SELECT recipe_id FROM zero_waste_app_recipeingredient WHERE ingredient_id IN (%s)"
cur.execute(select_user_products, (user_id,))
user_products = cur.fetchall()
products_id = [product[1] for product in user_products]
select_recipe_product = "SELECT recipe_id FROM zero_waste_app_recipeingredient WHERE ingredient_id IN ({})".format(', '.join(map(str, products_id)))
cur.execute(select_recipe_product)
recipes = [obj[0] for obj in cur.fetchall()]

print(Counter(recipes))
# print(', '.join(products_id))
