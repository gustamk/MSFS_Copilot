import requests
from langchain_core.runnables import RunnableLambda
from graph import engine
from secret import weather_api_key
from llm import llm_weather, llm_sql
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

# Functions for getting the weather data from Checkwx API
def get_weather(icao_code):
    url = f"https://api.checkwx.com/metar/{icao_code}/decoded"
    response = requests.request("GET", url, headers={'X-API-Key': weather_api_key})
    return response.text

def get_weather_nearest(icao_code):
    url = f"https://api.checkwx.com/metar/{icao_code}/nearest/decoded"
    response = requests.request("GET", url, headers={'X-API-Key': weather_api_key})
    return response.text

# Runnables for retrieving the weather data
runnable_local = RunnableLambda(
    func=get_weather
)

runnable_near = RunnableLambda(
    func=get_weather_nearest
)

# Prompt template for the weather retriever
prompt_template = """You are a helpful assistant that retrieves weather information from an API based on airport
ICAO codes.
Given an ICAO code of an airport, provide detailed current weather conditions at that location.
The ICAO code you have to use is the following: {icao_code}
Weather Information: {weather_info}
"""

# Prompt template for the ICAO search tool
search_template = '''Given an input question, first create a syntactically correct query to run, then look at the results of the query and return the answer. 
Write only the sql query, nothing else.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:.

{table_info}

here is an example question and answer:
question: "what is the icao for ubatuba airport?"
SQLQuery:"""
SELECT DISTINCT icao 
FROM airport_icao 
WHERE lower(airport) like '%ubatuba%'
"""
The sql query only needs to retrieve the icao, nothing else. Do not include the iata. No pre-amble, your first word must be "SELECT".
{top_k}
User question:
Question: {input}'''

sql_db = SQLDatabase(engine)
search_prompt = PromptTemplate.from_template(search_template)

# Function for finding the ICAO code from an airport from a SQL database
def search_icao(tool_input):
    chain = create_sql_query_chain(llm_sql,
                               sql_db,
                               search_prompt,
                               k=5,
                               )

    execute_query = QuerySQLDataBaseTool(db=sql_db)
    chain_retriever = chain | execute_query
    return chain_retriever.invoke({'question': tool_input})
    
# Output parser for the weather retriever
def parse_tool_input(tool_input):
    """
    Parse the tool input into request_type and icao_code.
    
    Args:
        tool_input (str): The format of the tool input is 'near/local ICAO_CODE'
        
    Returns:
        tuple: A tuple containing request_type and icao_code 
    """

    # Split the tool input by space
    parts = tool_input.split()    
    
    # Define the variables from the tool input
    icao_code = parts[1]
    request_type = parts[0].lower()  # Convert to lower case for comparison

    # Error throwback for invalid request type 
    if request_type not in ['near', 'local', 'search']:
        raise ValueError("Invalid request type. Expected 'near', 'local' or 'search'")
    
    #
    elif request_type == 'search':
        icao_code = search_icao(str(parts[1:]))
        request_type = 'local'
        return icao_code[3:7], request_type
        
    return icao_code, request_type

# Define the retriever for the agent tool.
def weather_retriever(tool_input):
    icao_code, request_type = parse_tool_input(tool_input)
    # Fetch and process the data
    if request_type == 'local':
        processed_data = runnable_local.invoke(icao_code)
    elif request_type == 'near':
        processed_data = runnable_near.invoke(icao_code)
    print(processed_data)
    # Update the template with the retrieved data for the given ICAO code
    updated_prompt = prompt_template.format(icao_code=icao_code, weather_info=processed_data, request_type=request_type)

    # Response based on the updated prompt
    response = llm_weather.invoke(updated_prompt)
    return response