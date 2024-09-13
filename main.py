import time
from neo4j import GraphDatabase
from faker import Faker
from function import *

# Configurations de connexion
uri = "neo4j+s://8c8966cb.databases.neo4j.io"
username = "neo4j"
password = "_RbNDCuv52-Mk5OvUuAzrQDKEZC6SyQvBF7tdZ54G-I"

# Créer une connexion au serveur Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

nbre_produits = 80
nbre_clients = 349
nbre_vendeur = 30
nbre_commandes = 2000


locales = [
    'en_US',  # États-Unis
    'fr_FR',  # France
    'es_ES',  # Espagne
]

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

delete_all_data(drv=driver)

for pid in range(nbre_produits):
    p_name = fake.random_element(elements=products)
    p_price = fake.random_int(min=550, max=35000)
    create_product(driver, p_id=pid, product_name=p_name, price=p_price)
# driver.close()


for cid in range(nbre_clients):
    print(cid)
    c_name = fake.name()
    c_phone = fake.phone_number()
    c_gender = fake.passport_gender()
    c_type = fake.random_element(elements=('XXL', 'XL', 'L'))
    create_customer(drv=driver, c_id=cid, name=c_name, phone=c_phone, gender=c_gender, type=c_type)


for vid in range(nbre_vendeur):
    v_name = fake.name()
    v_phone = fake.phone_number()
    fv_gender = fake.passport_gender()
    create_seller(drv=driver, s_id=vid, name=v_name, phone=v_phone, gender=fv_gender)

clients_ids = get_clients_id(drv=driver)
sellers_ids = get_sellers_id(drv=driver)
product_names = get_products_name(drv=driver)

print(f"Clients IDs : {clients_ids}")
print(f"Sellers IDs : {sellers_ids}")
print(f"Products Names : {product_names}")
driver.close()
time.sleep(5)

driver = GraphDatabase.driver(uri, auth=(username, password))
for oid in range(nbre_commandes):
    print(oid)
    c_id = fake.random_element(elements=clients_ids)
    v_id = fake.random_element(elements=sellers_ids)
    date = fake.date()
    product_name = fake.random_element(elements=product_names)
    qte = fake.random_int(min=1, max=35)
    create_order(drv=driver, id_order=oid, id_client=c_id, id_vendeur=v_id, date=date, produit=product_name, quantite=qte)

driver.close()