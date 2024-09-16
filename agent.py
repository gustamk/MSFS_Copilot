from llm import llm_agent
from graph import graph
from utils import get_session_id
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent, Tool
from cypher import aircraft_poh
from weather import weather_retriever
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an airplane expert providing information about airplanes and aviation."),
        ("human", "{input}"),
    ]
)

tools = [
    Tool.from_function(
        name="poh tool",
        func=aircraft_poh,
        description="""useful for answering questions on the pilot operating handbook (POH) from multiple aircraft.
        When using this tool, pay attention to the specific aircraft type and the specific question that has to be answered from the POH
        """,
        handle_tool_error = True,
    ),
    Tool.from_function(
        name="weather tool",
        func=weather_retriever,
        description="""
        Useful for answering questions related to the weather on a specific airport.
        Given an user question, such as 'How is the weather at EDDH airport?' or 'What is the weather near to EDDS airport',
        your input to the tool should be strictly made of two words:
        
        first word is the airport ICAO, "in these examples either EDDH or EDDS"
        second word is the type of request, either "local" or "near". 
        
        The tool will return the necessary information based on your request.
        """,
        handle_tool_error = True,
    ),
     
]

prompt_custom = PromptTemplate.from_template('''
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

def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)

agent = create_react_agent(llm_agent, tools, prompt_custom)

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

def generate_response(user_input):
    """
    Create a handler that calls the Conversational agent
    and returns a response to be rendered in the UI
    """

    response = chat_agent.invoke(
        {"input": user_input},
        {"configurable": {"session_id": get_session_id()}},)

    return response['output']
