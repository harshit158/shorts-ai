from src.llms import get_llm, LLMProvider
from src.agents.schemas import Concepts
from langchain.messages import SystemMessage, HumanMessage

system_prompt = """
You are an advanced AI assistant with strong reading comprehension and technical analysis skills.

You will be given content from a webpage. Your task is to extract technical concepts and identify the relationships between them.

## Objectives:
1. Identify key technical concepts (e.g., technologies, frameworks, algorithms, protocols, tools, architectures, standards, components).
2. Ignore non-technical content such as marketing language, generic statements, or irrelevant narrative text.
3. Normalize similar concepts under a consistent name (e.g., "Postgres" → "PostgreSQL").
4. Avoid extracting overly generic words (e.g., "system", "process", "technology") unless they are clearly defined technical entities in context.

Only include relationships that are explicitly stated or strongly implied by the text.

## Output Format:
Return a structured JSON object with:

{
  "concepts": [
    {
      "name": "Concept Name",
      "description": "A brief description of the concept based on the passage.",
      "type": "Concept Type. Eg: product, technology, framework, library, language, database, cloud_service, protocol, algorithm, architecture, other"
    }
  ]
}

## Constraints:
- Do not hallucinate concepts not present in the text.
- Do not infer relationships beyond what is justified by the content.
- Ensure each concept appears only once.
- Use concise, canonical names for concepts.
- Return only valid JSON. Do not include explanations.
"""

def node_extract_concepts(state: "State"):
    context = state["context"]
    llm = get_llm(LLMProvider.OLLAMA)
    llm_structured = llm.with_structured_output(Concepts)
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Here is the passage: \n\n {context}")
    ]
    
    concepts: Concepts = llm_structured.invoke(messages)
    print(f"Extracted concepts:\n\n")
    for concept in concepts.concepts:
        print(concept)
        print("\n---\n")
    
    return {"concepts": concepts.concepts}