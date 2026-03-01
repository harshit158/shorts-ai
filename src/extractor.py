from src.llms import get_llm
from src.schemas import LLMProvider
from src.scraper import Scraper
from src.prompts.extractor_prompts import SYSTEM_PROMPT, USER_PROMPT
from pydantic import BaseModel, Field
from typing import Optional
    
class Concept(BaseModel):
    """A concept in the passage."""
    name: str = Field(description="The concept text")
    description: str = Field(description="The concept description")
    reason_to_include: str = Field(description="Reasons why this concept is important to include in the concept graph")
    # prerequisites: list[str] = Field(description="List of prerequisite concepts that are required to understand this concept")
    # alternative_to: list[str] = Field(description="List of concepts that are alternatives to this concept. Eg: write-through vs write-back cache")
    # part_of: list[str] = Field(description="List of concepts that this concept is a part of. Eg: write-through cache is a part of caching")
    
    def __str__(self):
        repr = f"Concept: {self.name}\n"
        repr += f"Description: {self.description}\n"
        repr += f"Reason to include: {self.reason_to_include}\n"
        return repr

class Concepts(BaseModel):
    """A list of concepts in a passage."""
    concepts: list[Concept] = Field(description="List of concepts in the passage")
    
class Extractor():
    def __init__(self, llm_provider=LLMProvider.OLLAMA):
        self.llm = get_llm(llm_provider)
        self.llm_structured = self.llm.with_structured_output(Concepts)
        self.scraper = Scraper()
        
    def _extract(self, text: str) -> Concepts:
        messages = [
            ("system", SYSTEM_PROMPT),
            ("human", USER_PROMPT.format(content=text))
        ]
        return self.llm_structured.invoke(messages)

    def extract(self, text: Optional[str] = None, url: Optional[str] = None) -> Concepts:
        if not text and not url:
            raise ValueError("Either text or url must be provided")
        
        if url:
            text = self.scraper.scrape(url)
        
        return self._extract(text)