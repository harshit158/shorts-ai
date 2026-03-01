from src.llms import get_llm, LLMProvider
from src.agents.schemas import Concept, Steps
from langchain.messages import SystemMessage, HumanMessage

def _format_concepts(concepts: list[Concept]) -> str:
    formatted = ""
    for concept in concepts:
        formatted += f"- {concept.name} ({concept.type}): {concept.description}\n"
    return formatted

def node_plan_steps(state: "State"):
    concepts = state["concepts"]
    formatted_concepts = _format_concepts(concepts)

    system_prompt = """
You are an expert planner that creates step-by-step plans for generating quiz questions based on technical concepts.
You will be given a passage and a list of technical concepts extracted from that passage. 
Your task is to create a logical plan to outline the order of concepts in which they should be learned.

## Task:
- Re-arrange the concepts in a logical order for learning, and provide a reason for why each concept should be learned in that order.
- Each step should lay the foundation for the next, starting with basic concepts and building up to more complex ones.
"""

    prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Given the following concepts extracted from a passage:\n\n{formatted_concepts}\n\nCreate a step-by-step plan for how to generate insightful quiz questions based on these concepts.")
    ]

    llm = get_llm(LLMProvider.OLLAMA)
    llm_structured = llm.with_structured_output(Steps)
    response = llm_structured.invoke(prompt)

    # For simplicity, we won't parse the plan in this example, but in a real implementation you might want to.
    print(f"Generated plan:\n\n")
    for step in response.steps:
        print(step)
        print("\n---\n")

    return {
        "steps": response.steps
    }