from flask import Flask, request, Response
import requests
from urllib.parse import urljoin

app = Flask(__name__)

@app.route('/')
def home():
    try:
        return open('index.html', encoding='utf-8').read()
    except:
        return "Error: index.html not found"

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url: return "No URL", 400
    
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        res = requests.get(url, params=request.args, headers=headers, timeout=15)
        
        content_type = res.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            html = res.text
            proxy_path = "/proxy?url="
            
            base_tag = f'<base href="{url}">'
            html = html.replace('<head>', f'<head>{base_tag}')
            
            html = html.replace('href="/', f'href="{proxy_path}{urljoin(url, "/")}')
            html = html.replace('src="/', f'src="{proxy_path}{urljoin(url, "/")}')
            html = html.replace('action="/', f'action="{proxy_path}{urljoin(url, "/")}')

            response = Response(html, status=res.status_code)
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
        else:
            response = Response(res.content, status=res.status_code, content_type=content_type)

        response.headers['X-Frame-Options'] = 'ALLOWALL'
        response.headers['Content-Security-Policy'] = "frame-ancestors *"
        return response
    except Exception as e:
        return str(e), 500
