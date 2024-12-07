from flask import Flask, jsonify, render_template, request
import os
from analyzer.ai_suggestions import get_optimization_suggestions

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        submitted_code = request.json.get("code")
        if not submitted_code:
            return jsonify({"error": "No code provided"}), 400
        
        try:
            # Convert the response to a list of strings
            suggestions = get_optimization_suggestions(submitted_code)
            
            # If it's a GenerateContentResponse, extract text
            if hasattr(suggestions, 'text'):
                suggestions = [suggestions.text]
            elif hasattr(suggestions, 'candidates'):
                # If it has candidates, extract text from them
                suggestions = [candidate.text for candidate in suggestions.candidates]
            
            # Ensure suggestions is a list of strings
            if not isinstance(suggestions, list):
                suggestions = [str(suggestions)]
            
            return jsonify({"suggestions": suggestions})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return render_template("index.html")

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise EnvironmentError("API_KEY environment variable not set")
    
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1", "t"]
    app.run(debug=debug_mode)