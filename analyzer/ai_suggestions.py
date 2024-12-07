import google.generativeai as genai
import os

def get_optimization_suggestions(code: str) -> list:
    
    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)
    model=genai.GenerativeModel("gemini-1.5-flash")
    suggestions =model.generate_content("identify potential performance bottlenecks and  Provides suggestions for optimization"+code)

    return suggestions
