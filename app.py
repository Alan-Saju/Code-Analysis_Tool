from flask import Flask, jsonify, render_template, request
import os
import analyzer.ai_suggestions as ai
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        submitted_code = request.json.get("code")
        if not submitted_code:
            return jsonify({"error": "No code provided"}), 400
        
        try:
            # Get suggestions from the AI optimization module
            suggestions = ai.get_optimization_suggestions(submitted_code)
            
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