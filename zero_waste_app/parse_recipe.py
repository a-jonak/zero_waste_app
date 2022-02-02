from bs4 import BeautifulSoup
import requests
import re

from .parse_fractions import parse_problematic_numbers


def open_page(url):
    return BeautifulSoup(requests.get(url).content, 'html.parser')


def get_specific_div(page_content, div_class):
    return page_content.find('div', {'class': div_class})


def get_specific_div_by_id(page, id):
    return page.find('div', {'id': id})


def normalize_ingredients(ingredients):
    return [ingredient.text.replace('\t', '').replace('\n', '').replace('\xa0', '') for ingredient in ingredients.find_all('li')]


def parse_recipe_instruction(instructions):
    return '\n'.join([line for line in instructions.split('\n') if line.strip()])


class KuchniaLidla:
    def __init__(self, page_content) -> None:
        self._page_content = page_content

    def get_recipe_name(self):
        return get_specific_div(self._page_content, 'lead').find('h1').text

    def get_recipe_ingredients(self):
        ingredients = normalize_ingredients(get_specific_div(self._page_content, 'skladniki'))
        return self.prepare_ingredients_to_database(ingredients)

    def get_recipe_instructions(self):
        instructions = get_specific_div_by_id(self._page_content, 'opis').text
        return parse_recipe_instruction(instructions)

    def parse_ingredient(self, ingredient):
        try:
            product_and_amount = ingredient.split('-')
            if len(product_and_amount) < 2:
                product_and_amount = ingredient.split('–')
            amount = product_and_amount[1][1:].split(' ')
            return product_and_amount[0][:-1], amount[0], amount[1]
        except:
            return [ingredient]

    def prepare_ingredients_to_database(self, ingredients):
        d = []
        for ingredient in ingredients:
            parsed_ingredient = self.parse_ingredient(ingredient)
            if len(parsed_ingredient) > 1:
                product, amount, unit = parsed_ingredient
                d.append('nazwa: {}, ilość: {}, jednostka: {}'.format(product, parse_problematic_numbers(amount), unit))
            else:
                d.append('nazwa: {}, ilość: 1, jednostka: szt.'.format(parsed_ingredient[0], amount, unit))
        return d


def get_recipe_informations(page_url, units):
    page_content = open_page(page_url)
    recipe = KuchniaLidla(page_content)
    return recipe.get_recipe_name(), '\n'.join(recipe.get_recipe_ingredients()), recipe.get_recipe_instructions()
