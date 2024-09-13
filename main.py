
from neo4j import GraphDatabase

# Configurations de connexion
uri = "neo4j+s://8c8966cb.databases.neo4j.io"
username = "neo4j"
password = "_RbNDCuv52-Mk5OvUuAzrQDKEZC6SyQvBF7tdZ54G-I"

# Créer une connexion au serveur Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

