import google.generativeai as genai
import os
import re

def get_optimization_suggestions(code: str) -> list:
    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)
    
    # Refined prompt to get structured output
    prompt = f"""Analyze the following code and provide a structured response:

1. Identify potential performance bottlenecks
2. Suggest specific optimizations
Evaluation Criteria: for code optimzation
1. Correctness
2. Code Quality
3. Usage of typed parameters and typedefs

For each section, provide:
- Clear, concise points
- Practical, implementable suggestions
- Focus on most impactful improvements

Code to analyze:
{code}

Response Format:
**Potential Bottlenecks:**
- Concise bottleneck point 1
- Concise bottleneck point 2

**Optimization Suggestions:**
- Specific optimization 1
- Specific optimization 2
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    suggestions = model.generate_content(prompt)
    
    # Process the response to extract bottlenecks and optimizations
    response_text = suggestions.text
    
    # Extract bottlenecks
    bottlenecks_match = re.search(r'\*\*Potential Bottlenecks:\*\*(.*?)\*\*Optimization Suggestions:\*\*', response_text, re.DOTALL)
    bottlenecks = []
    if bottlenecks_match:
        bottlenecks = [line.strip('- ') for line in bottlenecks_match.group(1).split('\n') if line.strip()]
    
    # Extract optimizations
    optimizations_match = re.search(r'\*\*Optimization Suggestions:\*\*(.*)', response_text, re.DOTALL)
    optimizations = []
    if optimizations_match:
        optimizations = [line.strip('- ') for line in optimizations_match.group(1).split('\n') if line.strip()]
    
    # Combine and return
    return {
        "bottlenecks": bottlenecks,
        "optimizations": optimizations
    }