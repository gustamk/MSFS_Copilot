import os
from langchain_community.graphs.neo4j_graph import Neo4jGraph
import psycopg2
from secret import postgre_password, neo4j_uri, neo4j_user, neo4j_password, postgre_port, engine_uri
from sqlalchemy import create_engine

# Neo4j credentials
os.environ["NEO4J_URI"] = neo4j_uri
os.environ["NEO4J_USERNAME"] = neo4j_user
os.environ["NEO4J_PASSWORD"] = neo4j_password

# Define the Neo4j databases 
graph = Neo4jGraph(driver_config={'database': 'poh'})
cypher_examples = Neo4jGraph(driver_config={'database': 'examples'})
sessions = Neo4jGraph(driver_config={'database': 'sessions'})

# Connect to PostgreSQL database
conn = psycopg2.connect(
    database="airports",
    user="postgres",
    password=postgre_password,
    host="localhost",
    port= postgre_port
    ,
)

# Define the engine from the PostgreSQL database
engine = create_engine(
    engine_uri, 
    isolation_level="READ UNCOMMITTED",
    execution_options = {"postgresql_readonly": True}
    )
