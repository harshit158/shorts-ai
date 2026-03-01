from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal

# Concept Extraction
class ConceptType(str, Enum):
    PRODUCT = "product"
    TECHNOLOGY = "technology"
    FRAMEWORK = "framework"
    LIBRARY = "library"
    LANGUAGE = "language"
    DATABASE = "database"
    CLOUD_SERVICE = "cloud_service"
    PROTOCOL = "protocol"
    ALGORITHM = "algorithm"
    ARCHITECTURE = "architecture"
    OTHER = "other"
    
class Concept(BaseModel):
    """A concept in the passage."""
    name: str = Field(description="The concept text")
    description: str = Field(description="The concept description")
    type: ConceptType = Field(description="The type of the concept. Eg: product, technical concept, etc.")
    
    def __str__(self):
        repr = f"Concept: {self.name}\n"
        repr += f"Type: {self.type}\n"
        repr += f"Description: {self.description}\n"
        return repr

class Concepts(BaseModel):
    """A list of concepts in a passage."""
    concepts: list[Concept] = Field(description="List of concepts in the passage")

# Plan Steps
class Step(BaseModel):
    """A step in the plan."""
    concept: str = Field(description="The concept being addressed in this step")
    order_reason: str = Field(description="The reason for the order of this step in the plan")
    
    def __str__(self):
        repr = f"Concept: {self.concept}\n"
        repr += f"Reason for order: {self.order_reason}\n"
        return repr

class Steps(BaseModel):
    """A list of steps in the plan."""
    steps: list[Step] = Field(description="List of steps in the plan")
    
# Generate Questions

class Option(BaseModel):
    """A quiz option."""
    text: str = Field(description="The quiz option text")

class Quiz(BaseModel):
    """A quiz question with options and correct answer."""
    question: str = Field(description="The quiz question")
    options: list[Option] = Field(description="List of 4 quiz options")
    correct_answer: Literal[1, 2, 3, 4] = Field(description="The correct answer in terms of the index of the correct option (1-4)")
    correct_answer_explanation: str = Field(description="A detailed explanation of why the correct answer is correct")
    
    def __str__(self):
        """Compose and the quiz question and options."""
        string = f"Question: {self.question}\n"
        for idx, option in enumerate(self.options, start=1):
            string += f"{idx}. {option.text}\n"
        string += f"Correct Answer: {self.correct_answer}\n"
        string += f"Explanation: {self.correct_answer_explanation}"
        return string

class Quizzes(BaseModel):
    """A list of quiz questions."""
    quizzes: list[Quiz] = Field(description="List of quiz questions")