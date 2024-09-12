import  csv
from faker import Faker
from seller import locales

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

with open('data/fake_products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product_id', 'Product_name', 'Price'])

    for _ in range(nbre_produits):
        writer.writerow([
            'P_'+f'{fake.random_number(digits=3, fix_len=True)}',
            fake.random_element(elements=products),
            fake.random_int(min=550, max=35000)
        ])