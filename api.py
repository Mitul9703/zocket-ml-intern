"""
FastAPI backend.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Agent import WebAnalysisAgent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Web Analyser API",
    description="API for analyzing web content using the Web Analyser Agent",
    version="1.0.0"
)

# allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
# origins = [allowed_origins] if allowed_origins == "*" else allowed_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = WebAnalysisAgent()

class Analyserequest(BaseModel):
    url: str

class Analyseresponse(BaseModel):
    analysis: str
    success: bool
    error: str = None

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Web Analyser API is running"}

@app.post("/analyze", response_model=Analyseresponse)
async def analyze_url(request: Analyserequest):
    """
    Analyze a URL and return the analysis.
    
    Args:
        request: The request containing the URL to analyze
        
    Returns:
        The analysis of the URL
    """
    try:
        if not request.url.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="Invalid URL. URL must start with http:// or https://")
        
        result = agent.analyze_url(request.url)
        
        if isinstance(result, str):
            analysis = result
        else:
            messages = result.get("messages", [])
            if messages and hasattr(messages[0], "content"):
                analysis = messages[0].content
            else:
                analysis = str(result)
        
        return Analyseresponse(
            analysis=analysis,
            success=True
        )
    except Exception as e:
        return Analyseresponse(
            analysis="",
            success=False,
            error=str(e)
        )

