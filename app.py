from flask import Flask, jsonify, render_template, request
import os
import google.generativeai as genai
import re

app = Flask(__name__)

def get_optimization_suggestions(code: str) -> dict:
    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)
    
    # Refined prompt to get structured output
    prompt = f"""Analyze the following code and provide a structured response:

1. Identify potential performance bottlenecks
2. Suggest specific optimizations

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        submitted_code = request.json.get("code")
        if not submitted_code:
            return jsonify({"error": "No code provided"}), 400
        
        try:
            # Get suggestions from the AI optimization module
            suggestions = get_optimization_suggestions(submitted_code)
            
            # Combine bottlenecks and optimizations into a single list for display
            all_suggestions = []
            
            if suggestions.get("bottlenecks"):
                all_suggestions.append("**Potential Bottlenecks:**")
                all_suggestions.extend(suggestions["bottlenecks"])
            
            if suggestions.get("optimizations"):
                all_suggestions.append("**Optimization Suggestions:**")
                all_suggestions.extend(suggestions["optimizations"])
            
            return jsonify({"suggestions": all_suggestions})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return render_template("index.html")

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise EnvironmentError("API_KEY environment variable not set")
    
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1", "t"]
    app.run(debug=debug_mode)