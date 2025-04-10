"""
Agent:
- Accept a URL as input
- Retrieve and analyze the content of the provided web link
- Extract key information from the web page
- Generate a concise summary of the extracted content
"""

import os
from typing import Annotated, Dict, Any, List, TypedDict, Optional, Tuple
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from tools import WebScrapeTool

load_dotenv()

class AgentState(TypedDict):
    """State for the agent."""
    messages: Annotated[List, add_messages]
    url: Optional[str]
    scraped_content: Optional[Dict[str, Any]]
    analysis_result: Optional[str]


def initialize_llm():
    """Initializing the LLM (Here I have used Gemini 2.0 Flash since its free)"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.2,
        convert_system_message_to_human=True
    )

GEMINI_MODEL = initialize_llm()


def process_input(state: AgentState) -> Dict:
    """Extracting URL from user input. If no URL is found, return an error message."""
    last_message = state["messages"][-1]
    
    if not isinstance(last_message, HumanMessage):
        return state
    
    content = last_message.content
    
    import re
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, content)
    
    if urls:
        return {"url": urls[0]}
    else:
        return {
            "messages": [
                AIMessage(content="I couldn't find a URL in your message. Please provide a valid URL.")
            ]
        }

def scrape_website(state: AgentState) -> Dict:
    """Scrape the website using the Custom built WebScrapeTool (Uses the firecrawl API behind. Visit /tools.py for the implementation)."""
    url = state.get("url")
    if not url:
        return state
    
    scraper = WebScrapeTool()
    result = scraper._run(url)
    
    return {"scraped_content": result}

def analyze_content(state: AgentState) -> Dict:
    """LLM Call to Analyze and Extract key information from the scraped content. And then generate the summary"""
    scraped_content = state.get("scraped_content")
    if not scraped_content or not scraped_content.get("success", False):
        error_message = scraped_content.get("error", "Failed to scrape the website") if scraped_content else "No content to analyze"
        return {
            "messages": [
                AIMessage(content=f"Error: {error_message}")
            ]
        }
    
    llm = GEMINI_MODEL
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at analyzing web content. Your task is to:"
                  "\n1. Extract the most important information from the web page"
                  "\n2. Identify main topics, key facts, and important data points"
                  "\n3. Generate a detailed, comprehensive analysis"
                  "\n\nYour response should be well-structured with the following sections:"
                  "\n- KEY INFORMATION/HIGHLIGHTS: A detailed list of the most important facts, features, and data points"
                  "\n- ANALYSIS: A thorough examination of the content, including context and implications"
                  "\n- SUMMARY: A comprehensive yet concise summary of the entire page"
                  "\n\nUse appropriate formatting with headings, bullet points, and sections to make your response clear and readable."),
        ("user", "URL: {url}\n\n"
                 "Title: {title}\n\n"
                 "Description: {description}\n\n"
                 "Content:\n{content}\n\n"
                 "Please provide a detailed analysis of this web page content.")
    ])
    
    content = scraped_content.get("content", "")
    metadata = scraped_content.get("metadata", {})
    url = scraped_content.get("url", "")
    
    chain = prompt | llm
    result = chain.invoke({
        "url": url,
        "title": metadata.get("title", ""),
        "description": metadata.get("description", ""),
        "content": content
    })
    
    return {
        "analysis_result": result.content,
        "messages": [AIMessage(content=result.content)]
    }


def router(state: AgentState) -> str:
    """Routing to different nodes in thegraph based on state."""
    if state.get("url") and not state.get("scraped_content"):
        return "scrape_website"
    elif state.get("scraped_content") and not state.get("analysis_result"):
        return "analyze_content"
    else:
        return END

class WebAnalysisAgent:
    
    def __init__(self):
        
        self.workflow = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
       
        graph = StateGraph(AgentState)
        
        graph.add_node("process_input", process_input)
        graph.add_node("scrape_website", scrape_website)
        graph.add_node("analyze_content", analyze_content)
        
        graph.add_edge(START, "process_input")
        graph.add_conditional_edges(
            "process_input",
            router,
            {
                "scrape_website": "scrape_website",
                END: END
            }
        )
        graph.add_conditional_edges(
            "scrape_website",
            router,
            {
                "analyze_content": "analyze_content",
                END: END
            }
        )
        graph.add_edge("analyze_content", END)
        
        return graph.compile()
    
    def analyze_url(self, url: str) -> str:
        """
        Analyze a URL and return a summary of its content.
        
        Args:
            url: The URL to analyze
            
        Returns:
            A string containing the analysis and summary
        """
        state = {
            "messages": [HumanMessage(content=f"Please analyze this URL: {url}")],
            "url": None,
            "scraped_content": None,
            "analysis_result": None
        }
        
        result = self.workflow.invoke(state)
        
        if result and result.get("messages"):
            messages = result["messages"]
            if messages and isinstance(messages[-1], AIMessage):
                return messages[-1].content
        
        return "Failed to analyze the URL."


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python agent.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    agent = WebAnalysisAgent()
    result = agent.analyze_url(url)
    print(result)
