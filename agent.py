from llm import llm_agent
from graph import sessions
from utils import get_session_id
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent, Tool
from cypher import aircraft_poh
from weather import weather_retriever
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate

# Define the chat prompt
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an airplane expert providing information about airplanes and aviation."),
        ("human", "{input}"),
    ]
)

# Define LLM agent tools
tools = [
    Tool.from_function(
        name="weather tool",
        func=weather_retriever,
        description="""
        Useful for answering questions related to the weather on a specific airport and for searching an airport's ICAO. 
        Given an user question with an ICAO, such as 'How is the weather at EDDH airport?' or 'What is the weather near to EDDS airport', generate an input to the weather
        your input to the tool should be strictly made of two words:
        
        first word is the type of request, either "local" or "near".
        second word is the airport ICAO, "from the user query"
        
        The tool will return the necessary information based on your request.
        
        If the user asks a question without an icao, such as "what is the weather at porto seguro airport?", then your input should follow the following format:
        
        first word is the type of request, in this case "search".
        the following words are the airport name, in this example "porto seguro airport"
        Do not use your own knowledge about the corresponding ICAOs for each airport. If the user question includes an airport name, you must use the "search" request type. 
        """,
        handle_tool_error = True,
    ),
    Tool.from_function(
        name="poh tool",
        func=aircraft_poh,
        description="""
        Useful for answering questions on the pilot operating handbook (POH) from multiple aircraft.
        When using this tool, pay attention to the specific aircraft type and the specific question that has to be answered from the POH.
        Do not use this tool for searching an airport's ICAO. 
        """,
        handle_tool_error = True,
    ),
     
]

# Define the prompt for the agent
prompt_agent = PromptTemplate.from_template('''
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Previous conversation history:
{chat_history}

Question: {input}          
  
Thought:{agent_scratchpad}'''
)

# Define session memory from Neo4j database
def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=sessions)

# Define the LLM agent with chat history
agent = create_react_agent(llm_agent, tools, prompt_agent)

agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools,
    verbose =True,
    handle_parsing_errors=True
    )

chat_agent = RunnableWithMessageHistory(
    agent_executor,
    get_memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Response handler for streamlit
def generate_response(user_input):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """
    response = chat_agent.invoke(
        {"input": user_input},
        {"configurable": {"session_id": get_session_id()}},)

    return response['output']
