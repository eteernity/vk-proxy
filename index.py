from flask import Flask, request, Response
import requests
from urllib.parse import urljoin, urlencode

app = Flask(__name__)

@app.route('/')
def home():
    return open('index.html', encoding='utf-8').read()

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url: return "No URL", 400
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        content_type = res.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            return Response(res.content, status=res.status_code, content_type=content_type)

        html = res.text
        proxy_base = f"/proxy?url="
        
        html = html.replace('href="/', f'href="{proxy_base}{urljoin(url, "/")}')
        html = html.replace('action="/', f'action="{proxy_base}{urljoin(url, "/")}')
        
        response = Response(html, status=res.status_code)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Security-Policy'] = "default-src * 'unsafe-inline' 'unsafe-eval'"
        response.headers['X-Frame-Options'] = 'ALLOWALL'
        return response
    except Exception as e:
        return str(e), 500
