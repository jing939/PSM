# proxy.py
from flask import Flask, request, jsonify, make_response
import requests

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
    resp = None
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=data, timeout=30, stream=True)
        # Return raw content from Ollama (may be NDJSON / streaming chunks)
        content = resp.content
        content_type = resp.headers.get('Content-Type', 'application/json')
        response = make_response(content, resp.status_code)
        response.headers['Content-Type'] = content_type
        return response
    except requests.exceptions.RequestException as exc:
        error_body = None
        if resp is not None:
            try:
                error_body = resp.text
            except Exception:
                error_body = str(exc)
        else:
            error_body = str(exc)
        return jsonify({
            "detail": "Ollama 요청 실패",
            "error": str(exc),
            "body": error_body
        }), 500

@app.route("/api/tags", methods=["GET", "OPTIONS"])
def tags():
    if request.method == "OPTIONS":
        return make_response("", 200)
    resp = requests.get(f"{OLLAMA_URL}/api/tags")
    return jsonify(resp.json())

if __name__ == "__main__":
    print("🚀 프록시 서버 실행: http://localhost:5000")
    app.run(port=5000)