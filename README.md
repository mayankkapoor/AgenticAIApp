# AgenticAI App leveraging the new OpenAI Agents SDK and Tool usage

An agentic AI application that leverages the OpenAI Agents SDK to create specialized AI agents for different tasks.

## Features

- **Agent Specialization**: Create specialized agents for different domains (math tutoring, history tutoring, web search, file search)
- **Agent Triage**: Implement a triage system to route queries to the appropriate specialized agent
- **Input Guardrails**: Apply guardrails to filter and validate user inputs before processing
- **Knowledge Sources**: Connect to both local knowledge bases and web search capabilities

## Examples

The project includes two main example implementations:

### 1. Educational Assistant (quickstart_example.py)

This example demonstrates:
- A homework validation guardrail that checks if queries are homework-related
- Specialized tutor agents for math and history domains
- A triage agent that routes homework questions to the appropriate tutor

### 2. Knowledge Assistant (file_assistant.py)

This example demonstrates:
- A file search agent that queries local knowledge sources
- A web search agent that retrieves information from the internet
- A triage agent that determines whether to use local knowledge or web search

## Getting Started

1. Set up your environment variables in a `.env` file (including the MODEL variable)
2. Run one of the example files:
   ```
   python quickstart_example.py
   ```
   or
   ```
   python file_assistant.py
   ```

## Dependencies

- OpenAI Agents SDK
- Pydantic
- Python-dotenv
- AsyncIO
