import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        pass
    
    def scrape(self, url: str) -> str:
        """Scrape the content of a webpage."""
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove unwanted elements (script, style, etc.)
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        
        # Extract text content
        text = soup.get_text(separator="\n")
        
        # Clean empty lines and whitespace
        clean_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        
        return clean_text