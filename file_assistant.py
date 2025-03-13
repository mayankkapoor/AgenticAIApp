from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, InputGuardrailTripwireTriggered, FileSearchTool, WebSearchTool
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the model from environment variables
MODEL = os.getenv("MODEL")

file_search_agent = Agent(
    name="Knowledge Worker",
    handoff_description="Specialist agent for searching through the provided knowledge sources",
    instructions="You must only use the provided knowledge sources to answer questions. Do not rely on your own knowledge. If the information cannot be found in the provided sources, clearly state that you don't have the information.",
    tools=[FileSearchTool(vector_store_ids=["vs_67d1a6aeb41c8191a29b940182a6e272"], max_num_results=1, include_search_results=False)],
    model=MODEL,
)

web_search_agent = Agent(
    name="Web Search Agent",
    handoff_description="Agent for searching the web",
    instructions="You must only search the web to answer questions. Do not rely on your own knowledge. If the information cannot be found on the web, clearly state that you don't have the information.",
    tools=[WebSearchTool()],
    model=MODEL,
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's query. If the query is about a specific knowledge source, use the file search agent. If the query is about the web, use the web search agent. If the query is about something else, use the web search agent.",
    handoffs=[file_search_agent, web_search_agent],
    model=MODEL,
)

async def main():
    try:
        # web search question
        result = await Runner.run(triage_agent, "What is the capital of France?")
        print(result.final_output)

        # knowledge source question
        result = await Runner.run(triage_agent, "Find in your knowledge sources what is Deep Research?")
        print(result.final_output)

    except Exception as e:
        print(f"Exception triggered: {e}")

if __name__ == "__main__":
    asyncio.run(main())