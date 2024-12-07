from flask import Flask, render_template, request, jsonify
from analyzer.code_analysis import analyze_code
from analyzer.ai_suggestions import get_optimization_suggestions

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form.get("code")
        if not code:
            return jsonify({"error": "No code provided"}), 400

        # Analyze the code
        analysis = analyze_code(code)

        # Get AI-based suggestions
        suggestions = get_optimization_suggestions(code)

        # Combine results
        result = {"analysis": analysis, "suggestions": suggestions}
        return jsonify(result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
