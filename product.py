import  csv
from faker import Faker
from seller import locales
from main import driver
from function import *

nbre_produits = 120
fake = Faker(locale=locales)

products = [
    'Lait', 'Yaourt', 'Fromage', 'Beurre', 'Crème', 'Pain', 'Pâtes', 'Riz', 'Huile', 'Sauce',
    'Confiture', 'Miel', 'Chocolat', 'Biscuits', 'Céréales', 'Purée', 'Moutarde', 'Ketchup', 'Poivre', 'Sel',
    'Amandes', 'Noix', 'Cacahuètes', 'Raisins', 'Épices', 'Herbes', 'Paprika', 'Cumin', 'Cannelle', 'Vinaigre',
    'Olives', 'Cornichons', 'Chips', 'Pop-corn', 'Pâte', 'Gâteaux', 'Poudre', 'Farine', 'Sucre', 'Jus',
    'Bière', 'Vin', 'Liqueur', 'Compote', 'Sauce', 'Saucisse', 'Viande', 'Poulet', 'Poisson', 'Steak',
    'Salami', 'Jambon', 'Bacon', 'Rillettes', 'Pâté', 'Tartinade', 'Hummus', 'Guacamole', 'Salsa', 'Mayonnaise',
    'Vinaigrette', 'Tzatziki', 'Sirops', 'Crêpes', 'Cornflakes', 'Margarine', 'Graines', 'Crackers', 'Flocons', 'Concentré',
    'Compote', 'Sirops', 'Mélange', 'Pâtes', 'Vin', 'Pâtes', 'Mélange', 'Café', 'Thé', 'Cacao'
]

for _ in range(nbre_produits):
    p_name = fake.random_element(elements=products),
    p_price = fake.random_int(min=550, max=35000)
    create_product(driver, product_name=p_name, price=p_price)
driver.close()
