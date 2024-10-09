from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

# LLMs

llm_qa = Ollama(model="deepseek-coder-v2:latest",
            temperature = 0,
            system = """
            you are a helpful assistant to an airplane pilot. Answer the questions with completeness in mind. If you are provided contextual information, it is important that you avoid summarizing the information. If you do not know the answer, then respond that you are unable to help. You may receive contextual information as a result from a tool call, which can appear in a format similar to the following.
            
            Example user question: "What is the standard empty weight for the cessna 172?"
            Example context information: "[{'iv.instruction': '1663 pounds'}]"
            """
            )

llm_agent = Ollama(model= "mistral-nemo:latest",
            temperature = 0,
            verbose=True,
            )

llm_weather = Ollama(model= "mistral-nemo:latest",
            temperature = 0,
            verbose=True,
            )

llm_cypher = Ollama(model="deepseek-coder-v2:latest",
            temperature = 0,
            )

llm_sql = Ollama(model="mistral-nemo:latest",
            temperature = 0,
            )

# Embedding model

embeddings = OllamaEmbeddings(model = "all-minilm:latest")
