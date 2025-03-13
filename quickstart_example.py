from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the model from environment variables
MODEL = os.getenv("MODEL")

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
    model=MODEL,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model=MODEL,
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model=MODEL,
)


async def homework_guardrail(ctx, agent, input_data):
    print("Running homework guardrail check...")
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    print(f"Guardrail result: is_homework={final_output.is_homework}, reasoning='{final_output.reasoning}'")
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
    model=MODEL,
)

async def main():
    # history question
    result = await Runner.run(triage_agent, "Help me answer my homework question: When was the first moon landing?")
    print(result.final_output)

    # math question
    result = await Runner.run(triage_agent, "Help me answer my homework question: What is 12*7?")
    print(result.final_output)

    # guardrail trigger example
    try:
        result = await Runner.run(triage_agent, "what is life?")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print(f"Guardrail triggered: {e}")

if __name__ == "__main__":
    asyncio.run(main())