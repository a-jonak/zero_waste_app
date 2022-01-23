from bs4 import BeautifulSoup
import requests
import re


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


class KwestiaSmaku:
    def __init__(self, page_content, units) -> None:
        self._page_content = page_content
        self._units = units

    def get_recipe_name(self):
        return self._page_content.find('h1', {'class': 'przepis'}).text

    def get_recipe_ingredients(self):
        regex = re.compile('.*skladniki.*')
        ingredients = normalize_ingredients(get_specific_div(self._page_content, regex))
        return self.prepare_ingredients_to_database(ingredients)

    def get_recipe_instructions(self):
        regex = re.compile('.*przygotowanie.*')
        instructions = get_specific_div(self._page_content, regex).text
        return parse_recipe_instruction(instructions)

    def parse_ingredient(self, ingredient):
        parsed_ingredient = []
        amount_and_product = ingredient.split(' ')
        try:
            if '/' in amount_and_product[0]:
                amount = int(amount_and_product[0][0]) / int(amount_and_product[0][2])
            else:
                amount = int(amount_and_product[0])
            parsed_ingredient.append(amount)
            if amount_and_product[1] in self._units:
                parsed_ingredient.append(amount_and_product[1])
                parsed_ingredient.append(amount_and_product[2:])
            else:
                parsed_ingredient.append('szt.')
                parsed_ingredient.append(amount_and_product[1:])
        except:
            parsed_ingredient = ['1', 'szt.', amount_and_product]
        return parsed_ingredient

    def prepare_ingredients_to_database(self, ingredients):
        d = []
        for ingredient in ingredients:
            amount, unit, ingredient_name_list = self.parse_ingredient(ingredient)
            ingredient_name = ' '.join(ingredient_name_list)
            d.append('nazwa: {}, ilość: {}, jednostka: {}'.format(ingredient_name, amount, unit))
        return d


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
                d.append('nazwa: {}, ilość: {}, jednostka: {}'.format(product, amount, unit))
            else:
                d.append('nazwa: {}, ilość: 1, jednostka: szt.'.format(parsed_ingredient[0], amount, unit))
        return d


def get_recipe_informations(page_url, units):
    page_content = open_page(page_url)
    if 'kwestiasmaku' in page_url:
        recipe = KwestiaSmaku(page_content, units)
    elif 'kuchnialidla' in page_url:
        recipe = KuchniaLidla(page_content)
    return recipe.get_recipe_name(), '\n'.join(recipe.get_recipe_ingredients()), recipe.get_recipe_instructions()
