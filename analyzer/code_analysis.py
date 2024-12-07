import ast

def analyze_code(code: str) -> dict:
    """
    Analyzes the code for performance bottlenecks.
    Returns a dictionary with findings.
    """
    try:
        tree = ast.parse(code)
        bottlenecks = []

        # Example: Check for nested loops
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                inner_loops = [n for n in ast.walk(node) if isinstance(n, ast.For)]
                if len(inner_loops) > 1:
                    bottlenecks.append("Nested loops detected, consider optimizing.")

        return {"bottlenecks": bottlenecks}

    except SyntaxError as e:
        return {"error": f"Syntax error in code: {e}"}
