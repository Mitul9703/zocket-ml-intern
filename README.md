# Web Content Analyzer Agent

This project implements an AI agent that can:
- Accept a URL as input
- Retrieve and analyze the content of the provided web link
- Extract key information from the web page
- Generate a concise summary of the extracted content

## Features

- Built using LangGraph for agent orchestration
- Uses FireCrawl for efficient web scraping
- Powered by Google's Gemini 2.0 Flash Lite model
- Simple agent architecture with a dedicated web scraping tool

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   ```

3. Run the agent:
   ```
   python web_analyzer_agent.py
   ```

## Usage

```python
from web_analyzer_agent import WebAnalyzerAgent

# Initialize the agent
agent = WebAnalyzerAgent()

# Analyze a URL
result = agent.analyze_url("https://example.com")
print(result)
```

## Project Structure

- `web_analyzer_agent.py`: Main agent implementation
- `tools.py`: Contains the web scraping tool implementation
- `requirements.txt`: Project dependencies
