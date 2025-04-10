"""
Web scraping tool implementing FireCrawl builtin langchain tool.
"""
import os
from typing import Dict, Any
from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from langchain_core.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

class WebScrapeTool(BaseTool):
    """Tool for scraping web content using FireCrawl."""
    
    name: str = "web_scraper"
    description: str = "Scrapes content from a given URL using FireCrawl."
    
    def _run(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from the provided URL.
        
        Args:
            url: The URL to scrape.
            
        Returns:
            A dictionary containing the scraped content and metadata.
        """
        try:
            api_key = os.getenv("FIRECRAWL_API_KEY")
            
            loader = FireCrawlLoader(
                api_key=api_key,
                url=url,
                mode="scrape"
            )
            
            documents = loader.load()
            
            if not documents:
                return {"success": False, "error": "No content found at the provided URL"}
            
            document = documents[0]
            
            return {
                "success": True,
                "content": document.page_content,
                "metadata": document.metadata,
                "url": url
            }
            
        except Exception as e:
            return {"success": False, "error": str(e), "url": url}
