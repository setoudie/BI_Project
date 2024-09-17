import csv
import os
from tqdm import tqdm
from neo4j import GraphDatabase

uri = "neo4j+s://8c8966cb.databases.neo4j.io"
username = "neo4j"
password = "_RbNDCuv52-Mk5OvUuAzrQDKEZC6SyQvBF7tdZ54G-I"

loc_uri = "neo4j://localhost:7687"
password_loc="tryagain"

driver = GraphDatabase.driver(loc_uri, auth=(username, password_loc))

def check_and_create_save_dir(s_dir):
    if not os.path.exists(s_dir):
        os.mkdir(s_dir)

def download_clients_data(drv):
    save_dir = "data"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    results = drv.session().run(
        """
            MATCH (n:Client) RETURN n.c_id AS ClientID, n.name AS FullName, n.phone AS PhoneNumber, n.type As ClientType, n.gender AS Genre
        """
    )

    with open(f'{save_dir}/neo4j_clients.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ClientID', 'FullName', 'PhoneNumber', 'ClientType', 'Genre'])
        for record in tqdm(results, desc="Téléchargement des clients"):
            writer.writerow([
                record["ClientID"],
                record["FullName"],
                record["PhoneNumber"],
                record["ClientType"],
                record["Genre"]
            ])
    print('file path : data/neo4j_clients.csv')


def download_sellers_data(drv):
    save_dir = "data"
    check_and_create_save_dir(s_dir=save_dir)

    results = drv.session().run(
        """
            MATCH (n:Seller) RETURN n.s_id AS VendeurID, n.name AS FullName, n.phone AS PhoneNumber, n.gender AS Genre
        """
    )

    with open(f'{save_dir}/neo4j_sellers.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['VendeurID', 'FullName', 'PhoneNumber', 'Genre'])
        for record in tqdm(results, desc="Téléchargement des vendeurs"):
            writer.writerow([
                record["VendeurID"],
                record["FullName"],
                record["PhoneNumber"],
                record["Genre"]
            ])
    print('file path : data/neo4j_sellers.csv')


def download_product_data(drv):
    save_dir = "data"
    check_and_create_save_dir(s_dir=save_dir)

    results = drv.session().run("""
        MATCH (n:Product) RETURN n.p_id AS ProduitID, n.product_name AS Product, n.price AS Prix
    """)

    with open(f'{save_dir}/neo4j_products.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ProduitID', 'Product', 'Prix'])
        for record in tqdm(results, desc="Téléchargement des produits"):
            writer.writerow([
                record["ProduitID"],
                record["Product"],
                record["Prix"],
            ])
    print('file path : data/neo4j_products.csv')


def download_orders_data(drv):
    save_dir = "data"
    check_and_create_save_dir(s_dir=save_dir)

    results = drv.session().run("""
        MATCH (n:Order) RETURN n.o_id AS CommandeID,
        n.s_id AS VendeurID,
        n.c_id AS ClientID,
        n.date AS CommandeDate
    """)

    with open(f'{save_dir}/neo4j_orders.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CommandeID', 'VendeurID', 'ClientID', 'CommandeDate'])
        for record in tqdm(results, desc="Téléchargement des commandes"):
            writer.writerow([
                record["CommandeID"],
                record["VendeurID"],
                record["ClientID"],
                record['CommandeDate']
            ])
    print('file path : data/neo4j_orders.csv')


def download_orders_products_data(drv):
    save_dir = "data"
    check_and_create_save_dir(s_dir=save_dir)

    results = drv.session().run("""
        MATCH (n:CommandeProduit) RETURN n.o_id AS CommandeID,
        n.p_id AS ProductID,
        n.product_name AS ProductName,
        n.quantite AS Quantite
    """)

    with open(f'{save_dir}/neo4j_orders_products.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CommandeID', 'ProductID', 'ProductName', 'Quantite'])
        for record in tqdm(results, desc="Téléchargement des commandes"):
            writer.writerow([
                record["CommandeID"],
                record["ProductID"],
                record["ProductName"],
                record['Quantite']
            ])
    print('file path : data/neo4j_orders_products.csv')


def download_data(drv):
    download_orders_data(drv)
    download_product_data(drv)
    download_sellers_data(drv)
    download_orders_products_data(drv)
    download_clients_data(drv)
    print("Donnees téléchargées\nFormat : CSV")

driver.close()