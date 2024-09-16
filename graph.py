import streamlit as st
import os

# tag::graph[]
from langchain_community.graphs import Neo4jGraph

os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "onUgTkJj35ZV0JI-J6MbgWz3GyxtSzbpkmA4KXUnPwQ"

graph = Neo4jGraph(database='poh')
#end::graph[]