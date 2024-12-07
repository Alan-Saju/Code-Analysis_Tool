import google.generativeai as genai

def get_optimization_suggestions(code: str) -> list:
    
    genai.configure(api_key="AIzaSyClCyMoI5M4Q5E9fOUDOcUSdZ_IGztUfS8")
    model=genai.GenerativeModel("gemini-1.5-flash")
    suggestions =model.generate_content("identify potential performance bottlenecks and  Provides suggestions for optimization"+code)

    return suggestions
