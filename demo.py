"""
Sample script for testing.
"""

from Agent import WebAnalysisAgent
import sys

def main():
    
    print("Web Analyser Agent Demo")
    print("======================\n")
    
    url = sys.argv[1]
    
    print(f"\nAnalyzing URL: {url}\n")

    
    try:
        agent = WebAnalysisAgent()
        
        result = agent.analyze_url(url)
        
        print("Analysis Results:")
        print("================\n")
        print(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
