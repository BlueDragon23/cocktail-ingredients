"""
Scrape wikipedia for the ingredients of the IBA official cocktails
Start from the list of cocktails, and work out from there
"""
from bs4 import BeautifulSoup
import requests
from typing import List

def get_primary_links() -> List[str]:
    iba_official_cocktail_page = "https://en.m.wikipedia.org/wiki/List_of_IBA_official_cocktails"

    request_result = requests.get(iba_official_cocktail_page)
    if request_result.status_code != 200:
        raise Exception(f'Received error {request_result.status_code} from root page')

    root_page = BeautifulSoup(request_result.content)
    list_section = root_page.find(True, class_='mf-section-1')
    lists = list_section.findAll('ul')
    return [link['href'] for links in lists for link in links.findAll('a')]


def get_ingredients(link: str) -> (str, List[str]):
        page = requests.get(f"https://en.m.wikipedia.org/{link}")
        if page.status_code != 200:
            raise Exception(f'Received error {request_result.status_code} from root page')
        parsed_page = BeautifulSoup(page.content)
        page_title = parsed_page.find(True, id="section_0").get_text()
        print(page_title)
        infobox = [infobox for infobox in parsed_page.find_all(True, class_='infobox') if infobox.select('a[title="List of IBA official cocktails"]')][0]
        drink_name = infobox.caption.get_text()
        rows = infobox.find_all('tr')
        # Find the row that defines the ingredients, skipping the header row as it has the same link
        ingredients_list = [row.find('a', title='List of IBA official cocktails').parent.next_sibling for row in rows[1:] if row.find('a', title='List of IBA official cocktails') is not None]
        if len(ingredients_list) != 1:
            raise Exception(f'Failed to find ingredients list for drink {drink_name}')
        ingredients_td = ingredients_list[0]
        ingredients = [li.get_text() for li in ingredients_td.find_all('li')]
        return (drink_name, ingredients)


def run():
    links = get_primary_links()
    ingredients_mapping = {}
    for link in links:
        (drink_name, ingredients) = get_ingredients(link)
        ingredients_mapping[drink_name] = ingredients
    return ingredients_mapping


if __name__ == "__main__":
    print(run())