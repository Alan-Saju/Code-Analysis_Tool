from analyzer.ai_suggestions import get_optimization_suggestions
from analyzer.code_analysis import analyze_code
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        submitted_code = request.form.get("code")
        if not submitted_code:
            return jsonify({"error": "No code provided"}), 400

        # Analyze the code
        analysis = analyze_code(submitted_code)

        # Get AI-based suggestions
        suggestions = get_optimization_suggestions(submitted_code)

        # Combine results
        result = {"analysis": analysis, "suggestions": suggestions}
        return jsonify(result)

    return render_template("index.html")

if __name__ == "__main__":
    import os
    os.environ["API_KEY"] = "AIzaSyClCyMoI5M4Q5E9fOUDOcUSdZ_IGztUfS8cle"
    app.run(debug=True)
