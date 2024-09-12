# import pandas as pd
#
# customer_df = pd.read_csv('data/fake_customer.csv')
# products_df = pd.read_csv('data/fake_products.csv')
# seller_df = pd.read_csv('data/fake_seller.csv')
#
# print(customer_df['Cust_id'].value_counts())
from multiprocessing.spawn import set_executable

from neo4j import GraphDatabase

# Configurations de connexion
uri = "neo4j+s://8c8966cb.databases.neo4j.io"
username = "neo4j"
password = "_RbNDCuv52-Mk5OvUuAzrQDKEZC6SyQvBF7tdZ54G-I"

# Créer une connexion au serveur Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_seller(drv, name, phone, gender):
    query = (
        "CREATE (s:Seller {name: $name, phone: $phone, gender: $gender}) "
        "RETURN s"
    )
    # Ouverture d'une session pour exécuter la requête
    with drv.session() as session:
        result = session.run(query, name=name, phone=phone, gender=gender)
        return result.single()  # Récupère le premier résultat s'il existe

    # Fonction pour creer un produit
def create_product(drv, product_name, price):
    query = (
        "CREATE (p:Product {product_name: $product_name, price: $price})"
        "RETURN p"
    )
    with drv.session() as session:
        result = session.run(query, product_name=product_name, price=price)
        return result.single()  # Récupère le premier résultat s'il existe

def create_customer(drv, name, phone, gender, type):
    query = (
        "CREATE (c:Client {name: $name, phone: $phone, gender: $gender, type: $type}) "
        "RETURN c"
    )
    # Ouverture d'une session pour exécuter la requête
    with drv.session() as session:
        result = session.run(query, name=name, phone=phone, gender=gender, type=type)
        return result.single()  # Récupère le premier résultat s'il existe

def create_order(drv, id_client, id_vendeur, date, product, quantite):
    query = (
        "MATCH (c:Client {id: $id_client}), (s:Seller {id: $id_vendeur}), (p:Product {name: $product}) "
        "CREATE (o:Order {date: $date, quantite: $quantite}) "
        "CREATE (c)-[:PLACED]->(o)-[:SOLD_BY]->(s) "
        "CREATE (o)-[:CONTAINS]->(p) "
        "RETURN o"
    )
    # Ouverture d'une session pour exécuter la requête
    with drv.session() as session:
        result = session.run(
            query,
            id_client=id_client,
            id_vendeur=id_vendeur,
            date=date,
            product=product,
            quantite=quantite
        )
        return result.single()  # Retourne l'objet commande créé


# create_seller(driver, name='Seny Diedhiou', phone='+221 777461097', gender='M')
# create_product(driver, product_name="Lait", price=300)
# create_customer(driver, name='Seny Diedhiou', phone='+221 777461097', gender='M', type="VIP")
result = driver.session().run("""
    MATCH (p:Client)
    RETURN id(p) AS product_id, p.product_name AS product_name, p.price AS price
""")

for _ in result:
    print(_['product_id'])

def get_products_name(drv):
    result = driver.session().run("""
        MATCH (p:Product)
        RETURN p.product_name AS product_name
    """)

    products_names = []
    for record in result:
        products_names.append(record['product_name'])

    return products_names

def get_clients_id(drv):
    result = driver.session().run("""
        MATCH (c:Client)
        RETURN id(c) AS client_id
    """)

    clients_ids = []
    for record in result:
        clients_ids.append(record['client_id'])

    return clients_ids


def get_sellers_id(drv):
    result = driver.session().run("""
        MATCH (s:Seller)
        RETURN id(s) AS seller_id
    """)

    sellers_ids = []
    for record in result:
        sellers_ids.append(record['seller_id'])

    return sellers_ids

driver.close()
