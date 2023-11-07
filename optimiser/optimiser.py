from collections import Counter
from itertools import combinations
import re
from typing import Dict, List, Optional

cocktail_ingredients = {
    "Alexander": ["3 cl cognac", "3 cl brown crème de cacao", "3 cl light cream"],
    "Americano": ["3 cl Campari", "3 cl red vermouth", "A splash of soda water"],
    "Angel Face": ["3 cl gin", "3 cl Apricot brandy", "3 cl Calvados"],
    "Aviation": [
        "45 ml gin",
        "15 ml lemon juice",
        "15 ml maraschino liqueur",
        "1 barspoon crème de violette",
    ],
    "Between the Sheets": [
        "3 cl white rum",
        "3 cl cognac",
        "3 cl triple sec",
        "2 cl fresh lemon juice",
    ],
    "Boulevardier": [
        "30 ml (1 part) or 45 ml (1.5 parts) bourbon",
        "30 ml (1 part) sweet red vermouth",
        "30 ml (1 part) campari",
    ],
    "Brandy Crusta": [
        "52.5 ml brandy",
        "7.5 ml Maraschino Luxardo",
        "1 Bar Spoon curacao",
        "15 ml Fresh lemon juice",
        "1 barspoon simple syrup",
        "2 dashes aromatic bitters",
    ],
    "Casino": [
        "4 cl gin (Old Tom)",
        "1 cl Maraschino",
        "1 cl fresh lemon juice",
        "2 dashes orange bitters",
    ],
    "Clover Club Cocktail": [
        "4.5cl Gin",
        "1.5cl lemon juice",
        "1.5cl raspberry syrup",
        "1 egg white",
    ],
    "Daiquiri": ["6 cl white rum", "2 cl lime juice", "2 bar spoons superfine sugar"],
    "Dry Martini": ["6 cl (6 parts) gin", "1 cl (1 parts) dry vermouth"],
    "Gin Fizz": [
        "4.5 cl Gin",
        "3 cl fresh lemon juice",
        "1 cl simple syrup",
        "8 cl soda water",
    ],
    "Hanky Panky": [
        "45 ml London Dry Gin",
        "45 ml Sweet Red Vermouth",
        "7.5 ml Fernet Branca",
    ],
    "John Collins": [
        "4.5 cl (3 parts) gin",
        "3 cl (2 parts) freshly squeezed lemon juice",
        "1.5 cl (1 part) sugar syrup",
        "6 cl (4 parts) carbonated water",
    ],
    "The Last Word": [
        "One part gin",
        "One part lime juice",
        "One part green Chartreuse",
        "One part maraschino liqueur",
    ],
    "Manhattan": [
        "5 cL Rye whiskey",
        "2 cL Sweet red vermouth",
        "Dash Angostura bitters",
    ],
    "Martinez": [
        "45 ml London Dry Gin",
        "45 ml Sweet Red Vermouth",
        "1 Bar Spoon Maraschino Liqueur",
        "2 Dashes Orange Bitters",
    ],
    "Mary Pickford": [
        "6 cl white rum",
        "6 cl fresh pineapple juice",
        "1 cl Grenadine",
        "1 cl Maraschino",
    ],
    "Monkey Gland": [
        "5cl gin",
        "3cl orange juice",
        "2 drops absinthe",
        "2 drops grenadine",
    ],
    "Negroni": ["3 cl gin", "3 cl sweet red vermouth", "3 cl Campari"],
    "Old Fashioned": [
        "4.5 cl Bourbon or Rye whiskey",
        "2 dashes Angostura bitters",
        "1 sugar cube",
        "Few dashes plain water",
    ],
    "Paradise": [
        "3.5 cl (7 parts) gin",
        "2 cl (4 parts) apricot brandy",
        "1.5 cl (3 parts) orange juice",
    ],
    "Planter's punch": [
        "4.5cl Dark rum",
        "3.5 cl fresh orange juice",
        "3.5 cl fresh pineapple juice",
        "2 cl fresh lemon juice",
        "1 cl Grenadine syrup",
        "1 cl simple syrup",
        "3 or 4 dashes Angostura bitters",
    ],
    "Porto Flip": [
        "1.5 cl (3 parts) brandy",
        "4.5 cl (9 parts) port",
        "1 cl (2 parts) egg yolk",
    ],
    "Rusty Nail": ["4.5 cl Scotch Whisky", "2.5 cl Drambuie"],
    "Sazerac": [
        "5 cl cognac",
        "1 cl absinthe",
        "One sugar cube",
        "Two dashes Peychaud's Bitters",
    ],
    "Sidecar": ["5 cl cognac", "2 cl triple sec", "2 cl lemon juice"],
    "Stinger": ["5 cL cognac", "2 cL white crème de menthe"],
    "Tuxedo": [
        "3 cl gin (Old Tom)",
        "3 cl dry Vermouth",
        "1/2 barspoon Maraschino",
        "1/4 barspoon Absinthe",
        "3 dashes orange bitters",
    ],
    "Vieux Carré": [
        "3 cl rye whiskey",
        "3 cl cognac",
        "3 cl sweet Vermouth",
        "1 barspoon Bénédictine",
        "2 dashes Peychaud's bitters",
    ],
    "Whiskey Sour": [
        "4.5 cl (3 parts) bourbon whiskey",
        "3 cl (2 parts) fresh lemon juice",
        "1.5 cl (1 part) simple syrup",
    ],
    "White Lady": ["4 cl gin", "3 cl  Triple Sec", "2 cl lemon juice"],
    "Bellini": ["10 cl (2 parts) Prosecco", "5 cl (1 part) fresh peach purée"],
    "Black Russian": ["4 cl Vodka", "2 cl Coffee liqueur"],
    "Bloody Mary": [
        "4.5 cl/1 jigger (3 parts) vodka",
        "9 cl/3 oz (6 parts) Tomato juice",
        "1.5 cl/1 tbsp (1 part) Lemon juice",
        "2 to 3 dashes of Worcestershire Sauce",
        "Tabasco sauce",
        "Celery salt",
        "Black pepper",
    ],
    "Caipirinha": [
        "5 cl cachaça",
        "Half a lime cut into 4 wedges",
        "2 teaspoons sugar",
    ],
    "Champagne Cocktail": [
        "9cl Champagne",
        "1cl cognac",
        "2 dashes Angostura bitters",
        "1 sugar cube",
    ],
    "Corpse Reviver №2": [
        "3/4 ounce gin",
        "3/4 ounce lemon juice",
        "3/4 ounce Cointreau (curaçao)",
        "3/4 ounce Kina Lillet, Amber Vermouth or Cocchi Americano",
        "1 dash absinthe",
    ],
    "Cosmopolitan": [
        "4 cl Vodka Citron",
        "1.5 cl Cointreau",
        "1.5 cl Fresh lime juice",
        "3 cl Cranberry juice",
    ],
    "Rum and Coke (Cuba libre)": [
        "12 cl Cola",
        "5 cl white rum",
        "1 cl Fresh lime juice",
    ],
    "French 75": [
        "3 cl gin",
        "2 dashes simple syrup",
        "1.5 cl lemon juice",
        "6 cl Champagne",
    ],
    "French Connection": ["3.5cl Cognac", "3.5cl Amaretto liqueur"],
    "Golden Dream": [
        "2 cl (2 parts) Galliano",
        "2 cl (2 parts) Triple Sec",
        "2 cl (2 parts) Fresh orange juice",
        "1 cl (1 part) Fresh cream",
    ],
    "Grasshopper": [
        "3 cl Crème de menthe (green)",
        "3 cl Crème de cacao (white)",
        "3 cl cream",
    ],
    "Hemingway Special": [
        "6 cL (12 parts) Rum",
        "4 cl (8 parts) grapefruit juice",
        "1.5 cL (3 parts) Maraschino liqueur",
        "1.5 cl (3 parts) fresh lime juice",
    ],
    "Horse's Neck": [
        "4 cL (1 part) Brandy",
        "12 cL (3 parts) Ginger ale",
        "Dash of Angostura bitter (optional)",
    ],
    "Irish Coffee": [
        "4 cl (2 parts) Irish whiskey",
        "8 cl (4 parts) hot coffee",
        "3 cl (1½ parts) fresh cream",
        "1 tsp brown sugar",
    ],
    "Kir": ["9 cl (9 parts) white wine", "1 cl (1 part) crème de cassis"],
    "Long Island Iced Tea": [
        "1.5 cl  Tequila",
        "1.5 cl  Vodka",
        "1.5 cl  White rum",
        "1.5 cl  Triple sec",
        "1.5 cl  Gin",
        "2.5 cl  Lemon juice",
        "3.0 cl  simple syrup",
        "Top with Cola",
    ],
    "Mai Tai": [
        "3 cl amber Jamaican rum",
        "3 cl Martinique molasses rum",
        "1.5 cl orange curaçao",
        "1.5 cl orgeat syrup",
        "3 cl fresh lime juice",
        ".75 cl simple syrup",
    ],
    "Margarita": [
        "5 cL (10 parts) Tequila",
        "2 cL (4 parts) Triple sec",
        "1.5 cL (3 parts) Lime juice",
    ],
    "Mimosa": ["7.5 cl champagne", "7.5 cl orange juice"],
    "Mint Julep": [
        "6 cL Bourbon whiskey",
        "4 mint leaves",
        "1 teaspoon powdered sugar",
        "2 teaspoons water",
    ],
    "Mojito": [
        "4 cl white rum",
        "3 cl fresh lime juice",
        "6 sprigs of mint",
        "2 teaspoons sugar (or 2 cl of sugar syrup)",
    ],
    "Moscow mule": [
        "4.5 cl (9 parts) vodka",
        "0.5 cl (1 part) lime juice",
        "12 cl (24 parts) ginger beer",
    ],
    "Piña Colada": [
        "50 ml White Rum",
        "30 ml Coconut Cream",
        "50 ml Fresh Pineapple Juice",
    ],
    "Pisco Sour": [
        "60ml Pisco",
        "30ml lime juice",
        "20ml simple syrup",
        "1 egg white",
        "Several drops of aromatic bitters at the end",
    ],
    "Sea Breeze": ["4 cl Vodka", "12 cl Cranberry juice", "3 cl Grapefruit juice"],
    "Sex on the Beach": [
        "4 cl Vodka",
        "2 cl Peach schnapps",
        "4 cl Orange juice",
        "4 cl cranberry juice",
    ],
    "Singapore Sling": [
        "3 cl gin",
        "1.5 cl cherry liqueur (cherry brandy)",
        "0.75 cl Cointreau",
        "0.75 cl DOM Bénédictine",
        "1 cl Grenadine",
        "12 cl pineapple juice",
        "1.5 cl fresh lime juice",
        "1 dash Angostura bitters",
    ],
    "Tequila sunrise": [
        "4.5 cl (3 parts) Tequila",
        "9 cl (6 parts) Orange juice",
        "1.5 cl (1 part) Grenadine syrup",
    ],
    "Vesper": ["4.5 cl gin", "1.5 cl vodka", "0.75 cl Lillet Blanc"],
    "Zombie": [
        "1 1/2 oz  Puerto Rican golden rum",
        "1 1/2 oz Jamaican rum",
        "1 oz demerara 151 rum",
        "1/2 oz Donn's Mix (2:1 mix of grapefruit juice & cinnamon syrup)",
        "1/2 oz velvet falernum",
        "3/4 oz  lime juice",
        "1/4 oz grenadine",
        "2 dashes absinthe",
        "1 dash angostura bitters",
    ],
    "Barracuda": [
        "4.5 cl Gold rum",
        "1.5 cl Galliano",
        "6 cl Pineapple juice",
        "1 dash fresh lime juice",
        "Top with Prosecco",
    ],
    "Bee's Knees": ["2 oz gin", "3/4 oz lemon juice", "3/4 oz honey"],
    "Bramble": [
        "5 cl gin",
        "2.5 cl lemon juice",
        "1.25 cl simple syrup",
        "1.5 cl Creme de Mure (blackberry liqueur)",
    ],
    "Canchanchara": [
        "6 cl rum (Cuban aguardiente)",
        "1.5 cl fresh lime juice",
        "1.5 cl raw honey",
        "5 cl water",
    ],
    "Dark 'n' Stormy": ["6 cl dark rum", "10 cl ginger beer"],
    "Espresso martini": [
        "5 cl vodka",
        "3 cl Kahlúa",
        "Sugar syrup (according to individual preference of sweetness)",
        "1 strong espresso",
    ],
    "Fernandito": ["5 cl Fernet-Branca", "Cola to top up"],
    "French martini": [
        "4.5 cl vodka",
        "1.5 cl Raspberry Liqueur",
        "1.5 cl fresh pineapple juice",
    ],
    "Illegal": [
        "3 cl Mezcal (espadín)",
        "1.5 cl Jamaica overproof white rum",
        "1.5 cl Falernum liqueur",
        "1 barspoon maraschino Luxardo",
        "2.25 cl fresh lime juice",
        "1.5 cl simple syrup",
        "Few drops of egg white (optional)",
    ],
    "Lemon Drop Martini": [
        "3 cl vodka citron",
        "2 cl triple sec",
        "1.5 cl lemon juice",
    ],
    "Naked and Famous": [
        "2.25 cl mezcal",
        "2.25 cl yellow Chartreuse",
        "2.25 cl Aperol",
        "2.25 cl fresh lime juice",
    ],
    "New York Sour": [
        "6 cl whiskey (rye or bourbon)",
        "2.25 cl Simple syrup",
        "3 cl fresh lemon juice",
        "Few drops of egg white",
        "1.5 cl red wine (Shiraz or Malbec)",
    ],
    "Old Cuban": [
        "4.5 cl aged rum",
        "2.25 cl fresh lime juice",
        "3 cl simple syrup",
        "2 dashes Angostura bitters",
        "6 to 8 mint leaves",
        "6 cl champagne brut or Prosecco",
    ],
    "Paloma": ["One part tequila", "Three parts grapefruit soda"],
    "Paper Plane": [
        "3 cl Bourbon whiskey",
        "3 cl amaro Nonino",
        "3 cl Aperol",
        "3 cl fresh lemon juice",
    ],
    "Penicillin": [
        "6 cl blended Scotch whiskey",
        "0.75 cl Lagavulin 16y whiskey",
        "2.25 cl fresh lemon juice",
        "2.25 cl honey syrup",
        "2-3 quarter-sized slices of fresh ginger",
    ],
    "Russian Spring Punch": [
        "2.5 cl Vodka",
        "1.5 cl Crème de cassis",
        "1 cl Sugar Syrup",
        "2.5 cl Lemon Juice, fresh",
    ],
    "South Side or Southside": [
        "2 oz gin",
        "1 oz lime juice",
        "3/4 oz simple syrup",
        "1 sprig mint",
        "1 fresh mint leaf[1]",
    ],
    "Spicy Fifty": [
        "5 cl vodka vanilla",
        "1.5 cl elderflower cordial",
        "1.5 cl fresh lemon juice",
        "1 cl Monin honey syrup",
        "2 thin slices red chili pepper",
    ],
    "Spritz Veneziano": ["9 cl Prosecco", "6 cl Aperol", "Splash of soda water"],
    "Suffering Bastard": [
        "1 ounce gin",
        "1 ounce brandy (or bourbon)",
        "1/2 ounce lime juice cordial",
        "2 dashes Angostura bitters",
        "4 ounces ginger beer, chilled",
    ],
    "Tipperary": [
        "5 cl Irish whiskey",
        "2.5 cl sweet red vermouth",
        "1.5 cl green Chartreuse",
        "2 dashes Angostura bitters",
    ],
    "Tommy's margarita": [
        "4.5 cl Tequila",
        "1.5 cl Freshly squeezed lime juice",
        "2 bar spoons of agave nectar",
    ],
    "Trinidad Sour": [
        "4.5 cl Angostura bitters",
        "3 cl orgeat syrup",
        "2.25 cl fresh lemon juice",
        "1.5 cl rye whiskey",
    ],
    "Ve.n.to": [
        "4.5 cl white smooth grappa",
        "2.25 cl fresh lemon juice",
        "1.5 cl honey mix (made with chamomile infusion if desired)",
        "1.5 cl chamomile cordial",
        "1 cl egg white (optional)",
    ],
    "Yellow Bird": [
        "3 cl White Rum",
        "1.5 cl Galliano",
        "1.5 cl Triple sec",
        "1.5 cl Lime juice",
    ],
}

group_name = 'ing'
# Number patterns
# 1
# 1.1
# 1 1/1
# Volume labels
# ml
# oz
# cl
volume_regex = re.compile('(\d+|(\d+)?\.\d+|(\d+ )?\d+?/\d+|one|two) ?(ml|cl|oz|dash(es)?|bar ?spoon(s)?|ounce|tsp|drop(s)?|teaspoon(s)?) (?P<ing>.*)', flags=re.IGNORECASE)
parts_regex = re.compile('(\()?.* part(s)?(\))? (?P<ing>.*)', flags=re.IGNORECASE)
static_matches = {
    "london dry gin": "gin",
    "gin (old tom)": "gin",
    "freshly squeezed lemon juice": "lemon juice",
    "fresh lemon juice": "lemon juice",
    "lemon juice, fresh": "lemon juice",
    "vodka citron": "vodka",
    "vodka vanilla": "vodka",
    "freshly squeezed lime juice": "lime juice",
    "fresh lime juice": "lime juice",
    "cola to top up": "cola",
    "red vermouth": "sweet red vermouth",
    "sweet vermouth": "sweet red vermouth",
    "sugar (or 2 cl of sugar syrup)": "sugar",
    "bourbon whiskey": "bourbon",
    "bourbon or rye whiskey": "bourbon",
    "whiskey (rye or bourbon)": "bourbon",
    "fernet-branca": "fernet branca",
    "cointreau (curaçao)": "cointreau",
    "blended scotch whiskey": "scotch whiskey",
    "scotch whisky": "scotch whiskey",
    "fresh pineapple juice": "pineapple juice",
    "fresh orange juice": "orange juice",
    "maraschino": "maraschino liqueur",
    "dash angostura bitters": "angostura bitters",
    "dash of angostura bitter (optional)": "angostura bitters",
    "3 or 4 dashes angostura bitters": "angostura bitters",
    "jamaica overproof white rum": "white rum",
    "mezcal (espadín)": "mezcal"
}

def substring_matches(ingredient: str) -> Optional[str]:
    if "mint" in ingredient:
        return "mint"
    elif "egg white" in ingredient:
        return "egg white"
    elif "sugar" in ingredient:
        return "sugar"
    elif "honey" in ingredient:
        return "honey"
    else:
        return None



def strip_measurement(ingredient: str) -> str:
    substring_match = substring_matches(ingredient)
    if substring_match:
        return substring_match

    volume_match = volume_regex.match(ingredient)
    parts_match = parts_regex.match(ingredient)
    if volume_match is not None:
        stripped_ingredient = volume_match.group(group_name)
        volume_parts_match = parts_regex.match(stripped_ingredient)
        if volume_parts_match is not None:
            volume_ingredient = volume_parts_match.group(group_name)
            if volume_ingredient in static_matches:
                return static_matches[volume_ingredient]
            else:
                return volume_ingredient
        elif stripped_ingredient in static_matches:
            return static_matches[stripped_ingredient]
        return stripped_ingredient
    elif parts_match is not None:
        return parts_match.group(group_name)
    elif ingredient in static_matches:
        return static_matches[ingredient]
    return ingredient


def simplify_ingredients(ingredients: List[str]) -> List[str]:
    """
    Strip measurements/details from a list of ingredients
    """
    return [strip_measurement(ingredient.lower().strip()).strip() for ingredient in ingredients]


def most_frequent():
    frequencies = Counter()
    for drink, ingredients in cocktail_ingredients.items():
        for ingredient in ingredients:
            frequencies[strip_measurement(ingredient).lower()] += 1
    return frequencies


def build_matrix(canonical_cocktails: List[str]) -> (List[List[bool]], List[str]):
    """
    """
    # Build ingredients set
    all_ingredients = set()
    for ingredients in canonical_cocktails:
        print(ingredients)
        all_ingredients.update(ingredients)
    print("All ingredients", len(all_ingredients))
    all_ingredients = list(all_ingredients)
    result = []
    for ingredients in canonical_cocktails:
        bool_ingredients = [True if ingredient in ingredients else False for ingredient in all_ingredients]
        result.append(bool_ingredients)
    return (result, all_ingredients)


def filter_useless_ingredients(matrix: List[List[bool]]) -> (List[List[bool]], List[int], List[int]):
    """
    If an ingredient appears in at most one cocktail, there's no point keeping it.
    Remove it, and any cocktails it appears in. Return the updated matrix, 
    the list of removed columns, and the list of removed rows
    """
    culled_columns = []
    culled_rows = []
    for column in range(len(matrix[0])):
        ingredient_usage = [cocktail[column] for cocktail in matrix]
        true_rows = [j for j, b in enumerate(ingredient_usage) if b]
        if (len(true_rows) <= 1):
            # Cull the weak
            culled_columns.append(column)
            for row in true_rows:
                culled_rows.append(row)
    new_matrix = [[value for j, value in enumerate(row) if j not in culled_columns] 
                    for i, row in enumerate(matrix) if i not in culled_rows]
    return (new_matrix, culled_rows, culled_columns)


def solve(matrix: List[List[bool]], n: int) -> (List[int], List[int]):
    all_combinations = combinations(range(0, len(matrix[0])), n)
    most_cocktails = []
    best_combination = []
    for combination in all_combinations:
        # Count the number of cocktails that overlap
        count = 0
        cocktails_created = []
        for row, drink in enumerate(matrix):
            # If any non-combination index is True, stop
            for i, value in enumerate(drink):
                if value and not i in combination:
                    break
            else:
                cocktails_created.append(row)
                count += 1
        if count > len(most_cocktails):
            print(f"Updating best cocktail to combination: {combination}")
            most_cocktails = cocktails_created
            best_combination = combination
    print(f"This combination can make {len(most_cocktails)} cocktails")
    return (best_combination, most_cocktails)



def largest_subset(n: int) -> List[str]:
    """
    Return the list of ingredients that allows the largest number of cocktails to be created
    :param n: the number of ingredients to find
    """
    # Filter by cocktails that have at most n ingredients
    possible = {drink: ingredients for drink, ingredients in cocktail_ingredients.items() if len(ingredients) <= n}
    # Convert to a canonical ingredients list
    simplified_cocktails = {drink: simplify_ingredients(ingredients) for drink, ingredients in possible.items()}
    simplified_cocktail_names = list(simplified_cocktails.keys())
    # Create the matrix
    (matrix, simplified_cocktail_ingredients) = build_matrix(simplified_cocktails.values())
    # print(simplified_cocktail_ingredients)
    # Filter
    new_matrix, culled_rows, culled_columns = filter_useless_ingredients(matrix)
    simplified_cocktail_ingredients = [ingredient for i, ingredient in enumerate(simplified_cocktail_ingredients) if i not in culled_columns]
    names = [name for i, name in enumerate(simplified_cocktail_names) if i not in culled_rows]
    print(f"Went from {len(matrix)} cocktails to {len(new_matrix)} cocktails")
    print(f"Went from {len(matrix[0])} ingredients to {len(new_matrix[0])} ingredients")
    print(f"New ingredients list is {simplified_cocktail_ingredients}")
    # Identify the most rows with the most numbers in common
    best_combination, most_cocktails = solve(new_matrix, n)
    best_ingredients = [simplified_cocktail_ingredients[i] for i in best_combination]
    cocktail_names = [names[i] for i in most_cocktails]
    return (best_ingredients, cocktail_names)

def run(): 
    return largest_subset(7)

if __name__ == "__main__":
    ingredients, names = run()
    print(f"The best {len(ingredients)} ingredients are:")
    print(", ".join(ingredients))
    print(f"They make the {', '.join(names)}")