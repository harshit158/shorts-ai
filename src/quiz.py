from src.llms import llm_openai
from pydantic import BaseModel, Field

class Option(BaseModel):
    """A quiz option."""
    text: str = Field(description="The quiz option text")

class Quiz(BaseModel):
    """A quiz question with options and correct answer."""
    question: str = Field(description="The quiz question")
    options: list[Option] = Field(description="List of 4 quiz options")
    correct_answer: str = Field(description="The correct answer in terms of the index of the correct option (1-4)")
    
    def render(self):
        """Compose the quiz question and options using Telegram HTML."""
        html = f"<b>Question:</b> {self.question}\n\n"

        for idx, option in enumerate(self.options, start=1):
            html += f"<b>{idx}.</b> {option.text}\n\n"

        html += f"\n<b>Correct Answer:</b> {self.correct_answer}"
        return html

def generate_quiz():
    """Generate a quiz question using the LLM."""
    print("Using ", llm_openai.model_name, "to generate quiz")
    messages = [
        (
            "system",
            "You are a helpful tutoring assistant",
        ),
        ("human", "Ask an intermediate multiple choice question of 2 sentences in length on system design cache topic along with 4 options and the correct answer"),
    ]
    llm_structured = llm_openai.with_structured_output(Quiz)
    quiz: Quiz = llm_structured.invoke(messages)
    quiz_str: str = quiz.render()
    return quiz_str