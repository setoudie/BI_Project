import csv
import os
import xml.etree.cElementTree as ET
from xml.dom import minidom
from tqdm import tqdm
from neo4j import GraphDatabase

uri = "neo4j+s://8c8966cb.databases.neo4j.io"
username = "neo4j"
password = "_RbNDCuv52-Mk5OvUuAzrQDKEZC6SyQvBF7tdZ54G-I"

driver = GraphDatabase.driver(uri, auth=(username, password))

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
        n.vendeur AS VendeurName, 
        n.client AS ClientName, 
        n.produit AS Product, 
        n.quantite AS Quantite, 
        n.date AS CommandeDate     
    """)

    with open(f'{save_dir}/neo4j_orders.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CommandeID', 'VendeurName', 'ClientName', 'Product', 'Quantite', 'CommandeDate'])
        for record in tqdm(results, desc="Téléchargement des commandes"):
            writer.writerow([
                record["CommandeID"],
                record["VendeurName"],
                record["ClientName"],
                record['Product'],
                record['Quantite'],
                record['CommandeDate']
            ])
    print('file path : data/neo4j_orders.csv')


def download_orders_data_xml(drv):
    save_dir = "data"
    root = ET.Element("Commandes")

    # Vérifier et créer le répertoire de sauvegarde si nécessaire
    check_and_create_save_dir(s_dir=save_dir)

    # Requête Neo4j pour récupérer les données
    results = drv.session().run("""
        MATCH (n:Order) RETURN n.o_id AS CommandeID, 
                               n.vendeur AS VendeurName, 
                               n.client AS ClientName, 
                               n.produit AS Product, 
                               n.quantite AS Quantite, 
                               n.date AS CommandeDate     
    """)

    # Itérer sur les résultats et construire le fichier XML
    for record in tqdm(results, desc="Téléchargement des commandes"):
        commande = ET.SubElement(root, "Commande")
        ET.SubElement(commande, "CommandeID").text = str(record["CommandeID"])
        ET.SubElement(commande, "VendeurName").text = record["VendeurName"]
        ET.SubElement(commande, "ClientName").text = record["ClientName"]
        ET.SubElement(commande, "Product").text = record["Product"]
        ET.SubElement(commande, "Quantite").text = str(record["Quantite"])  # Conversion int en string
        ET.SubElement(commande, "CommandeDate").text = record["CommandeDate"]

    # Beautification du XML
    xml_string = ET.tostring(root, 'utf-8')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="   ")

    # Sauvegarde du fichier XML
    file_path = os.path.join(save_dir, 'neo4j_orders.xml')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)

    print(f'Fichier XML téléchargé et sauvegardé à: {file_path}')


def download_clients_data_xml(drv):
    save_dir = "data"

    # Vérifier et créer le répertoire 'data' si nécessaire
    check_and_create_save_dir(s_dir=save_dir)

    # Requête pour obtenir les données des clients
    results = drv.session().run(
        """
            MATCH (n:Client) RETURN n.c_id AS ClientID, n.name AS FullName, n.phone AS PhoneNumber, n.type As ClientType, n.gender AS Genre
        """
    )

    # Créer la structure XML
    root = ET.Element("Clients")

    # Parcourir les résultats et ajouter les données dans l'arbre XML
    for record in tqdm(results, desc="Téléchargement des clients"):
        client = ET.SubElement(root, "Client")
        ET.SubElement(client, "ClientID").text = record["ClientID"]
        ET.SubElement(client, "FullName").text = record["FullName"]
        ET.SubElement(client, "PhoneNumber").text = record["PhoneNumber"]
        ET.SubElement(client, "ClientType").text = record["ClientType"]
        ET.SubElement(client, "Genre").text = record["Genre"]

    # Beautification du fichier XML
    xml_string = ET.tostring(root, 'utf-8')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="   ")

    # Chemin de sauvegarde
    file_path = os.path.join(save_dir, 'neo4j_clients.xml')

    # Sauvegarder le fichier XML
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)

    print(f'Fichier XML téléchargé et sauvegardé à: {file_path}')


def download_product_data_xml(drv):
    save_dir = "data"
    check_and_create_save_dir(s_dir=save_dir)

    # Requête pour récupérer les données des produits
    results = drv.session().run("""
        MATCH (n:Product) RETURN n.p_id AS ProduitID, n.product_name AS Product, n.price AS Prix
    """)

    # Créer la structure XML
    root = ET.Element("Products")

    # Parcourir les résultats et ajouter les données au XML
    for record in tqdm(results, desc="Téléchargement des produits"):
        product = ET.SubElement(root, "Product")
        ET.SubElement(product, "ProduitID").text = record["ProduitID"]
        ET.SubElement(product, "ProductName").text = record["Product"]
        ET.SubElement(product, "Prix").text = str(record["Prix"])  # Conversion en string si nécessaire

    # Beautifier le XML
    xml_string = ET.tostring(root, 'utf-8')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="   ")

    # Chemin de sauvegarde
    file_path = os.path.join(save_dir, 'neo4j_products.xml')

    # Sauvegarde du fichier XML
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)

    print(f'Fichier XML téléchargé et sauvegardé à: {file_path}')


def download_sellers_data_xml(drv):
    save_dir = "data"
    check_and_create_save_dir(s_dir=save_dir)

    # Requête pour récupérer les données des vendeurs
    results = drv.session().run(
        """
            MATCH (n:Seller) RETURN n.s_id AS VendeurID, n.name AS FullName, n.phone AS PhoneNumber, n.gender AS Genre
        """
    )

    # Créer la structure XML
    root = ET.Element("Sellers")

    # Parcourir les résultats et ajouter les données dans l'arbre XML
    for record in tqdm(results, desc="Téléchargement des vendeurs"):
        seller = ET.SubElement(root, "Seller")
        ET.SubElement(seller, "VendeurID").text = record["VendeurID"]
        ET.SubElement(seller, "FullName").text = record["FullName"]
        ET.SubElement(seller, "PhoneNumber").text = record["PhoneNumber"]
        ET.SubElement(seller, "Genre").text = record["Genre"]

    # Beautifier le XML
    xml_string = ET.tostring(root, 'utf-8')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="   ")

    # Chemin de sauvegarde
    file_path = os.path.join(save_dir, 'neo4j_sellers.xml')

    # Sauvegarde du fichier XML
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(pretty_xml)

    print(f'Fichier XML téléchargé et sauvegardé à: {file_path}')


def download_data(drv, choice):
    if choice == str(1):
        download_sellers_data_xml(drv)
        download_clients_data_xml(drv)
        download_orders_data_xml(drv)
        download_product_data_xml(drv)
        print("Donnees téléchargées\nFormat : XML")
    else:
        download_orders_data(drv)
        download_product_data(drv)
        download_sellers_data_xml(drv)
        download_product_data(drv)
        print("Donnees téléchargées\nFormat : CSV")

driver.close()