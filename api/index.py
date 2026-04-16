from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Proxy is working. Usage: /api?url=https://example.com", 200
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        proxy_headers = [(name, value) for (name, value) in res.raw.headers.items() if name.lower() not in excluded_headers]
        
        return Response(res.content, res.status_code, proxy_headers)
    except Exception as e:
        return str(e), 500

@app.errorhandler(404)
def not_found(e):
    return "Маршрут не найден. Используйте /api?url=...", 404
