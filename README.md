```markdown
# MSFS_Copilot

Welcome to the repository for my ongoing personal project! This involves creating a chatbot designed to be used in conjunction with Microsoft Flight Simulator (MSFS). My goal is to develop an application that helps users learn 
aviation skills and increases the immersion of the simulator experience. The aim is to create a tool that has access to all documents and tools available in a cockpit.
The chatbot is powered by an LLM agent, which is built with Ollama and Langchain, and has access to custom tools for retrieving data from a multitude of sources.

## Features

### Current Features

- **Streamlit UI**: Currently, the chatbot uses Streamlit for creating an intuitive user interface.
- **Airport Weather Tool**: Allows interaction with the Checkwx API to retrieve weather data from any airport by providing the ICAO code. Additionally, it is possible to search just with an airport name, which is accomplished by adding a SQL lookup to a PostgreSQL database.
- **Pilot's Operating Handbook (POH) QA**: Answers questions from an airplane's POH, including all checklists, performance values, terminology, etc. The tool interacts with a Neo4j knowledge graph database used for storing the POHs. The first airplane available in this tool is the Cessna 172 G1000 model.

### Upcoming Features

- **Airport Charts QA**: A tool for answering questions from airport charts. I have a prototype using a fine-tuned multi-modal language model to extract information from airport charts, but there are still some technical difficulties to overcome for consistency and reliability.
- **Calculator / Conversion Tool**: Useful for various conversions and calculations in aviation.

### Planned Features

- **Flight Plan QA**: Ability to provide the chatbot with a SimBrief flight plan and allow it to read back information from the flight plan.
- **Aviation Terminology**: Access to additional documents on aviation terminology, regarding flight rules, reading navigation charts, and others.

```