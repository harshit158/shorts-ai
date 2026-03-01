from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from src.llms import get_llm, LLMProvider
from langchain.messages import SystemMessage, HumanMessage


# -------------------------
# 1. Define Agent State
# -------------------------
class QuestionState(TypedDict):
    context: str
    questions: List[str]


# -------------------------
# 2. Initialize LLM
# -------------------------
llm = get_llm(LLMProvider.OLLAMA)


# -------------------------
# 3. Node: Generate Questions
# -------------------------
def generate_questions(state: QuestionState) -> QuestionState:
    context = state["context"]

    prompt = [
        SystemMessage(content="You generate thoughtful, high-quality questions from context."),
        HumanMessage(content=f"Generate 5 insightful questions from the following context:\n\n{context}")
    ]

    response = llm.invoke(prompt)

    # Simple parsing (newline split)
    questions = [q.strip("- ").strip() for q in response.content.split("\n") if q.strip()]

    return {
        "context": context,
        "questions": questions
    }


# -------------------------
# 4. Build Graph
# -------------------------
graph = StateGraph(QuestionState)

graph.add_node("question_generator", generate_questions)

graph.set_entry_point("question_generator")
graph.add_edge("question_generator", END)

quiz_agent = graph.compile()


# -------------------------
# 5. Run Agent
# -------------------------
if __name__ == "__main__":
    context = """
    Transformers use self-attention to model long-range dependencies.
    They outperform RNNs on most NLP benchmarks and enable large language models.
    """

    result = quiz_agent.invoke({"context": context})
    print(result["questions"])