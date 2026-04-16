from flask import Flask, request, Response
import requests
from urllib.parse import urljoin

app = Flask(__name__)

@app.route('/')
def home():
    return open('index.html', encoding='utf-8').read()

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url: return "No URL", 400
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 VKMobile/8.5"
        }
        res = requests.get(url, params=request.args, headers=headers, timeout=10)
        
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

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['X-Frame-Options'] = 'ALLOWALL'
        response.headers['Server'] = 'vk-proxy-server'
        return response
    except Exception as e:
        return str(e), 500
