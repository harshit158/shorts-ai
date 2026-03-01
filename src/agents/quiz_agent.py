from typing import TypedDict
from langgraph.graph import StateGraph, END
from src.agents.nodes.node_concept_extraction import node_extract_concepts
from src.agents.nodes.node_plan_steps import node_plan_steps
from src.agents.nodes.node_generate_questions import node_generate_questions
from src.agents.schemas import Concept, Step, Quiz

class State(TypedDict):
    context: str # The context of the passage
    concepts: list[Concept] # The concepts extracted from the passage
    steps: list[Step] # The steps in the plan to learn the concepts
    quizzes: list[Quiz] # The generated questions

# Define the graph
graph = StateGraph(State)

graph.add_node("concept_extractor", node_extract_concepts)
graph.add_node("planner",  node_plan_steps)
graph.add_node("question_generator", node_generate_questions)

graph.set_entry_point("concept_extractor")
graph.add_edge("concept_extractor", "planner")
graph.add_edge("planner", "question_generator")
graph.add_edge("question_generator", END)

quiz_agent = graph.compile()


if __name__ == "__main__":
    context = """
    Local LLMs have gotten a lot of attention lately, especially now that tools like LM Studio make them easy to run. But one thing I keep noticing is that people treat them the same as cloud LLMs, expecting the same results they’d get from ChatGPT. Sometimes this could work, but more often the responses will likely be weaker or disappointing, which can lead to people thinking the model itself is the problem.

Usually, the issue is in how the model is being prompted. Local models don’t have the same layers of assistance that cloud models add behind the scenes - they rely much more on the clarity of what you give them. I had the same problem when first setting up my local model, but once I started approaching it differently and being more deliberate with my prompts, the quality of its responses improved a lot and its behavior became more predictable. So if you just got started with a local LLM, shifting how you think about using it could improve the results you get…

Local LLMs behave differently
They don’t adapt to the way you think
gpt model in LM Studio
When you run a model through a runner like Ollama or LM Studio, what you’re using is a pre-trained model exactly as it was trained. During a normal chat session the model’s weights are fixed, so it isn’t learning from you or gradually adjusting its behavior the way you’d expect it to. It can still use the conversation context to form its responses, as long as the total token count stays within the context window (the model can only use conversation history that fits in its memory limit). But that’s not the same as adapting long-term.

A lot of cloud AI platforms layer extra systems on top of the base model that help with reasoning, retrieval, tool use, and simulated empathy. Local setups usually skip those pieces unless you configure them yourself, if that’s an option. So because of that, local models tend to be more predictable, but also less forgiving. Many of them are smaller, and smaller models rely on the exact wording of your prompt…

Local models could still infer what you mean to an extent because they’re trained on patterns in language, but without the scale and extra systems behind cloud AI, that inference is usually weaker and depends much more on how you prompt. If a prompt is vague, loosely written, incomplete, or grammatically incorrect, the model closely sticks to the literal input instead of trying to guess your intent and filling in the gaps. This is why people sometimes think a local model is underperforming, when the real difference is how directly it responds to what you actually wrote.
    """

    result = quiz_agent.invoke({"context": context})