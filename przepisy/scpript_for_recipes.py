from bs4 import BeautifulSoup
from collections import defaultdict
import requests


def get_ingredients_from_kwestia_smaku(recipe):
    # for ingredient in content.find_all('li'):
    #     print(ingredient.text)
    content = get_specific_div(recipe, 'group-skladniki')
    return [ingredient.text.replace('\t', '').replace('\n', '') for ingredient in content.find_all('li')]

def get_ingredients_from_kuchnia_lidla(recipe):
    content = get_specific_div(recipe, 'skladniki')
    return [ingredient.text.replace('\t', '').replace('\n', '') for ingredient in content.find_all('li')]

def get_specific_div(page, div_class):
    # for line in page.find_all('div'):
    #     if line.get('class') and div_class in line.get('class'):
    #         return line
    return page.find('div', {'class': div_class})

def get_specific_div_by_id(page, id):
    return page.find('div', {'id': id})

def get_recipe_name(page):
    return page.find('h1', {'class': 'przepis'}).text

def get_instructions_from_kuchnia_lidla(page):
    div = get_specific_div_by_id(page, 'opis')
    return div.text

def parse_recipe_instruction(instruction):
    return '\n'.join([line for line in instruction.split('\n') if line.strip()])

def prepare_ingredients_list_for_database(ingredients):
    d = {}
    for ingredient in ingredients:
        parsed_ingredient = parse_ingredient(ingredient)
        if len(parsed_ingredient) > 1:
            product, amount, unit = parsed_ingredient
            d[product] = {'amount': amount, 'unit': unit}
        else:
            d[parsed_ingredient[0]] = {'amount': '1', 'unit': 'szt.'}
    return d

def parse_ingredient(ingredient):
    try:
        product_and_amount = ingredient.split('-')
        if len(product_and_amount) < 2:
            product_and_amount = ingredient.split('–')
        amount = product_and_amount[1][1:].split(' ')
        return product_and_amount[0][:-1], amount[0], amount[1]
    except:
        return [ingredient]


def get_links(line):
    links = []
    prefix = 'https://www.kwestiasmaku.com'
    for link in line.find_all('a'):
        if prefix + link['href'] not in links and 'przepis' in link['href']:
            links.append(prefix + link['href'])
    return links

def get_links_from_kuchnia_lidla(page):
    return ['https://kuchnialidla.pl' + link['href'] for link in page.find_all('a', {'class': 'description'})]

def get_next_page(page):
    return 'https://www.kwestiasmaku.com' + page.find('div', {'class': 'text-center'}).find('li', {'class': 'next'}).find('a')['href']


def open_page(page):
    return BeautifulSoup(requests.get(page).content, 'html.parser')


def search_pages(start, depth, pages):
    soup = open_page(start)
    if depth < 0:
        return pages
    else:
        pages.append(start)
        return search_pages(get_next_page(soup), depth-1, pages)

# URL = 'https://www.kwestiasmaku.com/przepisy/posilki'
# URL1 = 'https://www.kwestiasmaku.com/przepis/makaron-z-grzybami-i-boczkiem'
# URL2 = 'https://www.kwestiasmaku.com/przepis/placki-jogurtowe-z-bananem'



# for link in get_links(get_specific_div(open_page(URL), 'views-bootstrap-grid-plugin-style')):
#     recipe_name = get_recipe_name(open_page(link))
#     ingredients = get_ingredients(open_page(link))
#     if len(ingredients) < 10:
#         print(recipe_name, ingredients)

# print(get_links(get_specific_div(open_page(URL), 'views-bootstrap-grid-plugin-style')))
# print(get_ingredients(get_specific_div(soup, 'group-skladniki')))
# print(get_next_page(soup))
# print(search_pages(URL, 3, []))

def get_recipe_information(page_with_recipe):
    recipe_name = get_specific_div(page_with_recipe, 'lead').find('h1').text
    ingredients = get_ingredients_from_kuchnia_lidla(page_with_recipe)
    ingredients_list = prepare_ingredients_list_for_database(ingredients)
    # instructions = get_specific_div_by_id(page_with_recipe, 'opis').find('p').text
    instructions = parse_recipe_instruction(get_instructions_from_kuchnia_lidla(page_with_recipe))
    return recipe_name, ingredients_list, instructions

# page = open_page('https://kuchnialidla.pl/przepisy/weganskie')
# for link in get_links_from_kuchnia_lidla(page):
#     page_with_recipe = open_page(link)
#     recipe_name = get_specific_div(page_with_recipe, 'lead').find('h1').text
#     ingredients = get_ingredients_from_kuchnia_lidla(page_with_recipe)
#     ingredients_list = prepare_ingredients_list_for_database(ingredients)
#     # instructions = get_specific_div_by_id(page_with_recipe, 'opis').find('p').text
#     instructions = parse_recipe_instruction(get_instructions_from_kuchnia_lidla(page_with_recipe))
#     print(recipe_name, ingredients_list, instructions)
#     print('\n')

URL1 = 'https://kuchnialidla.pl/ciasto-na-pizze-1'
URL2 = 'https://kuchnialidla.pl/weganski-lunchbox-kanapki-z-salatka-z-ciecierzycy'

# print(parse_recipe_instruction(get_instructions_from_kuchnia_lidla(open_page(URL1))))