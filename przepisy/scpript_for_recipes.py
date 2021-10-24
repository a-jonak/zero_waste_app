from bs4 import BeautifulSoup
import requests


def get_ingredients(recipe):
    # for ingredient in content.find_all('li'):
    #     print(ingredient.text)
    content = get_specific_div(recipe, 'group-skladniki')
    return [ingredient.text.replace('\t', '').replace('\n', '') for ingredient in content.find_all('li')]

def get_specific_div(page, div_class):
    # for line in page.find_all('div'):
    #     if line.get('class') and div_class in line.get('class'):
    #         return line
    return page.find('div', {'class': div_class})

def get_links(line):
    links = []
    prefix = 'https://www.kwestiasmaku.com'
    for link in line.find_all('a'):
        if prefix + link['href'] not in links and 'przepis' in link['href']:
            links.append(prefix + link['href'])
    return links

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

URL = 'https://www.kwestiasmaku.com/przepisy/posilki'
URL1 = 'https://www.kwestiasmaku.com/przepis/makaron-z-grzybami-i-boczkiem'
URL2 = 'https://www.kwestiasmaku.com/przepis/placki-jogurtowe-z-bananem'

for link in get_links(get_specific_div(open_page(URL), 'views-bootstrap-grid-plugin-style')):
    print(get_ingredients(open_page(link)))

# print(get_links(get_specific_div(open_page(URL), 'views-bootstrap-grid-plugin-style')))
# print(get_ingredients(get_specific_div(soup, 'group-skladniki')))
# print(get_next_page(soup))
# print(search_pages(URL, 3, []))