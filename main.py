from tqdm import tqdm
import time
from neo4j import GraphDatabase
from faker import Faker
from function import *

# Configurations de connexion --> AuraDB
uri = "neo4j+s://8c8966cb.databases.neo4j.io"
username = "neo4j"
password = "_RbNDCuv52-Mk5OvUuAzrQDKEZC6SyQvBF7tdZ54G-I"

# Configuration de connexion locale
loc_uri = "neo4j://localhost:7687"
password_loc="tryagain"

# Créer une connexion au serveur Neo4j
driver = GraphDatabase.driver(loc_uri, auth=(username, password_loc))
# driver = GraphDatabase.driver(loc_uri, auth=(username, password_loc))

nbre_produits = 80
nbre_clients = 300
nbre_vendeur = 30
nbre_commandes = 2000


locales = [
    'en_US',  # États-Unis
    'fr_FR',  # France
    'es_ES',  # Espagne
]

fake = Faker(locale=locales)

delete_all_data(drv=driver)

for pid in tqdm(range(nbre_produits), desc="Creation des Produits"):
    p_name = fake.random_element(elements=products)
    p_price = fake.random_int(min=550, max=35000)
    create_product(driver, p_id=f"prd_{pid}", product_name=p_name, price=p_price)
# driver.close()


for cid in tqdm(range(nbre_clients), desc="Création des Clients"):
    # print(cid)
    c_name = fake.name()
    c_phone = fake.phone_number()
    c_gender = fake.passport_gender()
    c_type = fake.random_element(elements=('XXL', 'XL', 'L'))
    create_customer(drv=driver, c_id=f"clt_{cid}", name=c_name, phone=c_phone, gender=c_gender, type=c_type)


for vid in tqdm(range(nbre_vendeur), desc="Creation des Vendeurs"):
    v_name = fake.name()
    v_phone = fake.phone_number()
    fv_gender = fake.passport_gender()
    create_seller(drv=driver, s_id=f"vnd_{vid}", name=v_name, phone=v_phone, gender=fv_gender)

clients_ids = get_clients_ids(drv=driver)
sellers_ids = get_sellers_ids(drv=driver)
product_ids = get_products_ids(drv=driver)


# print(f"Clients IDs : {clients_ids}")
# print(f"Sellers IDs : {sellers_ids}")
# print(f"Products Names : {product_names}")
driver.close()
time.sleep(5)

driver = GraphDatabase.driver(loc_uri, auth=(username, password_loc))
# driver = GraphDatabase.driver(uri, auth=(username, password))

for oid in tqdm(range(nbre_commandes), desc="Creation des Commandes"):
    # print(oid)
    c_id = fake.random_element(elements=clients_ids)
    v_id = fake.random_element(elements=sellers_ids)
    date = fake.date()
    create_order(drv=driver, id_order=f"cmd_{oid}", id_client=c_id, id_vendeur=v_id, date=date)

driver.close()
time.sleep(5)

driver = GraphDatabase.driver(loc_uri, auth=(username, password_loc))
orders_ids = get_order_ids(drv=driver)
# print(orders_ids)

for _ in tqdm(range(nbre_commandes), desc="Creation des Commandes-Produits"):
    o_id = fake.random_element(elements=orders_ids)
    p_id = fake.random_element(elements=product_ids)
    product_name = fake.random_element(elements=products)
    quantite = fake.random_int(min=1, max=300)
    create_order_product(drv=driver, o_id=o_id, p_id=p_id, prd_name=product_name, quantite=quantite)

driver.close()