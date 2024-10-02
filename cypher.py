from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Neo4jVector
from examples import examples
from secret import langsmith_key
from llm import embeddings, llm, llm_cypher
from graph import graph, cypher_examples
import os

# Langsmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = langsmith_key

# POH retriever with fewshot prompting.
example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)

# Neo4jvector database for storing the embeddings from the examples
neo4jvector = Neo4jVector(embedding=embeddings, database="examples")

# Example selector from user query 
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    embeddings,
    neo4jvector,
    k=5,
    input_keys=["question"],
)

# Prompt for the Cypher query generator
prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="""
    You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query to run, no pre amble. 
    Your sole task is to write Cypher code. Do not write any sentences or words before or after the cypher code, your only task is to create the cypher query for retrieving the correct information.
    It is imperative that you generate the cypher query right from the beginning of your answer. Be extremely precise in writing the cypher query, use lower case words only. 
    Pay close attention to the examples you will be provided, as they give you valuable information about the structure of the database. 
    
    \n\nHere is the schema information
    \n\nNode properties are the following:
    Airplane_type {{id: STRING, name: STRING}},poh {{id: STRING}},poh_section {{id: STRING, index: INTEGER}},poh_subsection {{id: STRING, description: STRING}},
    poh_subsection_item {{id: STRING, description: STRING, instruction: STRING}},item_values {{id: STRING, instruction: STRING, index: INTEGER, description: STRING}}

    Relationship properties are the following:

    The relationships are the following:
    (:poh)-[:IS_MANUAL_FROM]->(:Airplane_type),(:poh_section)-[:BELONGS_TO]->(:poh),(:poh_subsection)-[:BELONGS_TO]->(:poh_section),(:poh_subsection_item)-[:BELONGS_TO]->(:poh_subsection),(:item_values)-[:BELONGS_TO]->(:poh_subsection_item),
    (:item_values)-[:BELONGS_TO]->(:poh_subsection),(:table)-[:BELONGS_TO]->(:poh_subsection),(:table)-[:IS_TABLE_FROM]->(:poh_subsection).

    \n\nBelow are a number of examples of questions and their corresponding Cypher queries.""",
    suffix="User input: {question}\nCypher query: ",
    input_variables=["question"],
)

# Define LLM chain for querying the knowledge graph
chain_cypher = GraphCypherQAChain.from_llm(
    graph=graph,
    cypher_llm=llm_cypher,
    cypher_prompt=prompt,
    verbose=True,
    qa_llm=llm,
    allow_dangerous_requests = True,
)

# Define the tool for the LLM agent
def aircraft_poh(input):
    return chain_cypher.invoke(input = str({input}))