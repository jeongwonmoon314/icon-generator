from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.error
import os
import re
from datetime import datetime

ARCHIVE_FILE = "archive.json"

def load_archive():
    if os.path.exists(ARCHIVE_FILE):
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_archive(data):
    with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def call_gemini(api_key, prompt):
    system_prompt = """You are an expert SVG icon designer specializing in technical/industrial icons for PowerPoint presentations.

RULES:
- Output ONLY raw SVG code, nothing else. No markdown, no explanation.
- ViewBox must be "0 0 48 48"
- Use ONLY these colors: currentColor for strokes/fills (so color can be changed in PPT)
- Style: clean line icon, stroke-based, strokeWidth 1.5-2, rounded linecaps
- No background rectangle
- Icons must be recognizable at small sizes (32px)
- Use <title> tag with the icon name inside SVG

STYLE GUIDE:
- Minimalist line art
- stroke="currentColor" fill="none" on main elements
- Use fill="currentColor" with opacity for subtle fills if needed
- strokeLinecap="round" strokeLinejoin="round"
"""

    full_prompt = f"{system_prompt}\n\nCreate an SVG icon for: {prompt}"

    payload = json.dumps({
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1024}
    }).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
    # 마크다운 코드블록 제거
    text = re.sub(r"```(?:svg)?", "", text).strip().rstrip("`").strip()
    if not text.startswith("<svg"):
        raise ValueError("SVG 코드가 반환되지 않았습니다.")
    return text

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # 로그 억제

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/archive":
            self.send_json(200, load_archive())
        elif self.path == "/" or self.path == "/index.html":
            self.serve_file("index.html", "text/html; charset=utf-8")
        else:
            self.send_json(404, {"error": "Not found"})

    def serve_file(self, filename, content_type):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_json(404, {"error": "File not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8"))

        if self.path == "/api/generate":
            api_key = body.get("apiKey", "").strip()
            prompt = body.get("prompt", "").strip()
            label = body.get("label", prompt[:30])
            tags = body.get("tags", [])

            if not api_key or not prompt:
                return self.send_json(400, {"error": "apiKey와 prompt가 필요합니다."})

            try:
                svg = call_gemini(api_key, prompt)
                entry = {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                    "label": label,
                    "prompt": prompt,
                    "tags": tags,
                    "svg": svg,
                    "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                archive = load_archive()
                archive.insert(0, entry)
                save_archive(archive)
                self.send_json(200, {"svg": svg, "id": entry["id"]})
            except Exception as e:
                self.send_json(500, {"error": str(e)})

        elif self.path == "/api/delete":
            icon_id = body.get("id")
            archive = load_archive()
            archive = [x for x in archive if x["id"] != icon_id]
            save_archive(archive)
            self.send_json(200, {"ok": True})

        else:
            self.send_json(404, {"error": "Not found"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"✅ 서버 시작: http://localhost:{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
