from flask import Flask, request, jsonify, abort
import os

app = Flask(__name__)

LEAKS_FOLDER = "leaks"
API_KEY = os.environ.get("API_KEY", "coldfinder")

def load_data():
    data = []
    for root, dirs, files in os.walk(LEAKS_FOLDER):
        for file in files:
            if file.lower().endswith((".txt", ".log", ".csv", ".json", ".cfg", ".sql")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                data.append({
                                    "file": file,
                                    "content": line
                                })
                except:
                    pass
    return data

DATA = load_data()

def require_api_key():
    key = request.headers.get("X-API-Key")
    if key != API_KEY:
        abort(401, description="Unauthorized: Invalid API key")

@app.route("/")
def home():
    return "Secure Search API is running."

@app.route("/search", methods=["GET"])
def search():
    require_api_key()

    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify({"error": "Missing query"}), 400

    results = [x for x in DATA if query in x["content"].lower()]

    return jsonify({
        "query": query,
        "count": len(results),
        "results": results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
