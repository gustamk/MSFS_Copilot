from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Neo4jVector
from examples import examples
from llm import embeddings, llm, llm_cypher
from graph import graph
import os

# Langsmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__c3610e3383004dcc954af64e3f57c95d" 

# POH retriever with fewshot prompting.
example_prompt = PromptTemplate.from_template(
    "User input: {question}\nCypher query: {query}"
)

example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    embeddings,
    Neo4jVector(embedding=embeddings),
    k=5,
    input_keys=["question"],
)

prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="You are a Neo4j expert. Given an input question, create a syntactically correct Cypher query to run, no pre amble. It is imperative that you generate the cypher query right from the beginning of your answer. Be extremely precise in writing the cypher query. \n\nHere is the schema information\n{schema}.\n\nBelow are a number of examples of questions and their corresponding Cypher queries.",
    suffix="User input: {question}\nCypher query: ",
    input_variables=["question", "schema"],
)

chain_cypher = GraphCypherQAChain.from_llm(
    graph=graph, llm=llm_cypher, cypher_prompt=prompt, verbose=True, qa_llm=llm
)

def aircraft_poh(input):
    return chain_cypher.invoke(input = str({input}))