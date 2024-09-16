import requests
from langchain_core.runnables import RunnableLambda
import os
from llm import llm_weather

# Langsmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__c3610e3383004dcc954af64e3f57c95d" 

# Functions from getting the weather data from a specific ICAO or nearest location.
def get_weather(icao_code):
    url = f"https://api.checkwx.com/metar/{icao_code}/decoded"
    response = requests.request("GET", url, headers={'X-API-Key': 'c19da1f48d204afaa33dc1e9df'})
    return response.text

def get_weather_nearest(icao_code):
    url = f"https://api.checkwx.com/metar/{icao_code}/nearest/decoded"
    response = requests.request("GET", url, headers={'X-API-Key': 'c19da1f48d204afaa33dc1e9df'})
    return response.text

# Output for the weather retriever parser
def parse_tool_input(tool_input):
    """
    Parse the tool input into icao_code and request_type.
    
    Args:
        tool_input (str): The format of the tool input is 'ICAO_CODE near/local'
        
    Returns:
        tuple: A tuple containing icao_code and request_type
    """

    # Split the tool input by space, we expect there to be only one or two spaces
    parts = tool_input.split()
    
    if len(parts) != 2:
        raise ValueError("Invalid tool input format. Expected 'ICAO_CODE near/local'")
        
    icao_code = parts[0]
    request_type = parts[1].lower()  # Convert to lower case for comparison

    if request_type not in ['near', 'local']:
        raise ValueError("Invalid request type. Expected 'near' or 'local'")

    return icao_code, request_type

# Prompt template for the weather retriever
prompt_template = """You are a helpful assistant that retrieves weather information from an API based on airport
ICAO codes. There are two types of request, either 'near' or 'local'.
Given an ICAO code of an airport, provide detailed current weather conditions at that location.
Here is the ICAO code: {{icao_code}}
Here is the type of request: {{request_type}}
Weather Information: {{weather_info}}
"""

# Lambda functions to get and process the data 
def fetch_weather_data_local(icao_code):
    raw_weather_info = get_weather(icao_code)
    
    return raw_weather_info

runnable_local = RunnableLambda(
    func=fetch_weather_data_local
)

def fetch_weather_data_near(icao_code):
    raw_weather_info = get_weather_nearest(icao_code)
    
    return raw_weather_info

runnable_near = RunnableLambda(
    func=fetch_weather_data_near
)

# Define the retriever for the agent tool.
def weather_retriever(tool_input):
    icao_code, request_type = parse_tool_input(tool_input)
    
    # Fetch and process the data
    if request_type == 'local':
        processed_data = runnable_local.invoke({"icao_code": icao_code})
    if request_type == 'near':
        processed_data = runnable_near.invoke({"icao_code": icao_code})
    
    # Update the template with the actual retrieved data for the given ICAO code
    updated_prompt = prompt_template.format(icao_code=icao_code, weather_info=processed_data, request_type=request_type)

    # Respond based on the updated prompt
    response = llm_weather.invoke(updated_prompt)
    return response