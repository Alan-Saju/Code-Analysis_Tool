from analyzer.ai_suggestions import get_optimization_suggestions
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        submitted_code = request.form.get("code")
        if not submitted_code:
            return jsonify({"error": "No code provided"}), 400

        # Get AI-based suggestions
        try:
            suggestions = get_optimization_suggestions(submitted_code)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify(suggestions)

        

    return render_template("index.html")

if __name__ == "__main__":
    import os
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise EnvironmentError("API_KEY environment variable not set")
    app.run(debug=True)
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1", "t"]
    app.run(debug=debug_mode)
