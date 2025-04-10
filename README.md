# Try it out here: [https://zocket-assignment-frontend.vercel.app/](https://zockent-assignment-frontend.vercel.app/)

# Zocket Assignment

This project implements an AI agent that can:
- Accept a URL as input
- Retrieve and analyze the content of the provided web link
- Extract key information from the web page
- Generate a concise summary of the extracted content

## Features

- Built using LangGraph for agent orchestration
- Uses FireCrawl for web scraping
- Powered by Google's Gemini 2.0 Flash Lite model (Free of cost)

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
   python Agent.py
   ```

## Usage

```python
from Agent import WebAnalysisAgent

# Initialize the agent
agent = WebAnalysisAgent()

# Analyze a URL
result = agent.analyze_url("<URL>")
print(result)
```

## Project Structure
![image](https://github.com/user-attachments/assets/acdd4444-4ca4-4d4a-beae-edef382e29c7)

- `Agent.py`: Main agent implementation
- `tools.py`: Contains the web scraping tool implementation using FireCrawl
