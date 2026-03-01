from src.llms import get_llm, LLMProvider
from src.agents.schemas import Quizzes, Step
from langchain.messages import SystemMessage, HumanMessage

def _format_steps(steps: list[Step]) -> str:
    formatted = ""
    for idx, step in enumerate(steps, start=1):
        formatted += f"{idx}. {step.concept}: {step.order_reason}\n"
    return formatted

def node_generate_questions(state: "State"):
    context = state["context"]
    steps = state["steps"]
    steps_formatted = _format_steps(steps)
    
    system_prompt = """
You are an expert question generator that creates thoughtful, high-quality quiz questions from context and a learning plan.
You will be given a passage and a step-by-step plan for learning the technical concepts in that passage.
Generate 5 insightful quiz questions from the passage and learning plan provided. Each question should have 4 answer options, with one correct answer and a detailed explanation of why the correct answer is correct.

## Passage:
{context}

## Learning Plan:
{steps}
"""

    human_message = """
Generate 5 insightful quiz questions from the passage and learning plan provided. Each question should have 4 answer options, with one correct answer and a detailed explanation of why the correct answer is correct.
"""

    messages = [
        SystemMessage(content=system_prompt.format(context=context, steps=steps_formatted)),
        HumanMessage(content=human_message)
    ]

    llm = get_llm(LLMProvider.OLLAMA)
    llm_structured = llm.with_structured_output(Quizzes)
    quizzes: Quizzes = llm_structured.invoke(messages)
    
    print(f"Generated quizzes:\n\n")
    for quiz in quizzes.quizzes:
        print(quiz)
        print("\n---\n")

    return {
        "quizzes": quizzes.quizzes
    }