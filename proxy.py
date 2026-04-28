# proxy.py
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434"

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route("/api/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        return make_response("", 200)
    data = request.json
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json=data)
    return jsonify(resp.json())

@app.route("/api/tags", methods=["GET", "OPTIONS"])
def tags():
    if request.method == "OPTIONS":
        return make_response("", 200)
    resp = requests.get(f"{OLLAMA_URL}/api/tags")
    return jsonify(resp.json())

if __name__ == "__main__":
    print("🚀 프록시 서버 실행: http://localhost:5000")
    app.run(port=5000)