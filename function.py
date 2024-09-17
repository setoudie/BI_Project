"""
    Dans ce fichier est ecrit toutes les fonctions utiles du project
"""
import csv
import os

from tqdm import tqdm

products = [
    'Lait', 'Yaourt', 'Fromage', 'Beurre', 'Crème', 'Pain', 'Pâtes', 'Riz', 'Huile', 'Sauce',
    'Confiture', 'Miel', 'Chocolat', 'Biscuits', 'Céréales', 'Purée', 'Moutarde', 'Ketchup', 'Poivre', 'Sel',
    'Amandes', 'Noix', 'Cacahuètes', 'Raisins', 'Épices', 'Herbes', 'Paprika', 'Cumin', 'Cannelle', 'Vinaigre',
    'Olives', 'Cornichons', 'Chips', 'Pop-corn', 'Pâte', 'Gâteaux', 'Poudre', 'Farine', 'Sucre', 'Jus',
    'Compote', 'Sauce', 'Saucisse', 'Viande', 'Poulet', 'Poisson', 'Steak', 'Salami', 'Jambon', 'Bacon',
    'Rillettes', 'Pâté', 'Tartinade', 'Hummus', 'Guacamole', 'Salsa', 'Mayonnaise', 'Vinaigrette', 'Tzatziki',
    'Sirops', 'Crêpes', 'Cornflakes', 'Margarine', 'Graines', 'Crackers', 'Flocons', 'Concentré',
    'Compote', 'Sirops', 'Mélange', 'Pâtes', 'Pâtes', 'Mélange', 'Café', 'Thé', 'Cacao', 'Moutarde'
]

def create_seller(drv, s_id, name, phone, gender):
    query = (
        "CREATE (s:Seller {s_id: $s_id, name: $name, phone: $phone, gender: $gender}) "
        "RETURN s"
    )
    # Ouverture d'une session pour exécuter la requête
    with drv.session() as session:
        result = session.run(query, s_id=s_id, name=name, phone=phone, gender=gender)
        return result.single()  # Récupère le premier résultat s'il existe

    # Fonction pour creer un produit
def create_product(drv, p_id, product_name, price):
    query = (
        "CREATE (p:Product {p_id: $p_id, product_name: $product_name, price: $price})"
        "RETURN p"
    )
    with drv.session() as session:
        result = session.run(query, p_id=p_id, product_name=product_name, price=price)
        return result.single()  # Récupère le premier résultat s'il existe

def create_customer(drv, c_id, name, phone, gender, type):
    query = (
        "CREATE (c:Client {c_id: $c_id, name: $name, phone: $phone, gender: $gender, type: $type}) "
        "RETURN c"
    )
    # Ouverture d'une session pour exécuter la requête
    with drv.session() as session:
        result = session.run(query, c_id=c_id, name=name, phone=phone, gender=gender, type=type)
        return result.single()  # Récupère le premier résultat s'il existe

def create_order(drv, id_order, id_client, id_vendeur, date, produit, quantite):
    query = """
    MATCH (c:Client {c_id: $id_client}), (v:Seller {s_id: $id_vendeur}), (p:Product {product_name: $produit})
    CREATE (o:Order {
        o_id: $id_order,
        produit: p.product_name,
        client: c.name,
        vendeur: v.name,
        date: $date,
        quantite: $quantite
    })
    CREATE (c)-[:A_PASSE]->(o)
    CREATE (v)-[:A_TRAITE]->(o)
    CREATE (o)-[:CONTIENT]->(p)
    RETURN o
    """
    with drv.session() as session:
        result = session.run(query, id_order=id_order, id_client=id_client, id_vendeur=id_vendeur, date=date, produit=produit, quantite=quantite)
        return result.single()


def get_products_name(drv):
    result = drv.session().run("""
        MATCH (p:Product)
        RETURN p.product_name AS product_name
    """)

    products_names = []
    for record in result:
        products_names.append(record['product_name'])

    return products_names

def get_clients_id(drv):
    result = drv.session().run("""
        MATCH (c:Client)
        RETURN c.c_id AS client_id
    """)

    clients_ids = []
    for record in result:
        clients_ids.append(record['client_id'])

    return clients_ids


def get_sellers_id(drv):
    result = drv.session().run("""
        MATCH (s:Seller)
        RETURN s.s_id AS seller_id
    """)

    sellers_ids = []
    for record in result:
        sellers_ids.append(record['seller_id'])

    return sellers_ids


def delete_all_data(drv):
    # Exécuter la requête pour supprimer tous les nœuds et relations
    drv.session().run("""
        MATCH (n)
        DETACH DELETE n
    """)
    print("Tous les nœuds ont été supprimés.")


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
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

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
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

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
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

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