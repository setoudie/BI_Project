"""
    Dans ce fichier est ecrit toutes les fonctions utiles du project
"""

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

def create_order_product(drv, o_id, p_id, prd_name, quantite):
    query = ("""
        CREATE (cp:CommandeProduit {o_id: $o_id, p_id: $p_id, product_name: $product_name, quantite: $quantite})
        RETURN cp
    """)

    with drv.session() as session:
        result = session.run(query, o_id=o_id, p_id=p_id, product_name=prd_name, quantite=quantite)
        return result.single()

def create_order(drv, id_order, id_client, id_vendeur, date):
    query = """
    CREATE (o:Order {
        o_id: $id_order,
        c_id: $id_client,
        s_id: $id_vendeur,
        date: $date
    })
    CREATE (c)-[:A_PASSE]->(o)
    CREATE (v)-[:A_TRAITE]->(o)
    RETURN o
    """
    with drv.session() as session:
        result = session.run(query, id_order=id_order, id_client=id_client, id_vendeur=id_vendeur, date=date)
        return result.single()


def get_products_ids(drv):
    result = drv.session().run("""
        MATCH (p:Product)
        RETURN p.p_id AS product_id
    """)

    products_ids = []
    for record in result:
        products_ids.append(record['product_id'])

    return products_ids

def get_order_ids(drv):
    result = drv.session().run("""
        MATCH (p:Order)
            RETURN p.o_id AS order_id
    """)

    orders_ids = []
    for record in result:
        orders_ids.append(record['order_id'])

    return orders_ids

def get_clients_ids(drv):
    result = drv.session().run("""
        MATCH (c:Client)
        RETURN c.c_id AS client_id
    """)

    clients_ids = []
    for record in result:
        clients_ids.append(record['client_id'])

    return clients_ids


def get_sellers_ids(drv):
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

