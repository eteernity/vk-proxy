from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/proxy')
def proxy():
    url = request.args.get('url')
    if not url: return "No URL", 400
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return Response(res.content, res.status_code)
    except Exception as e:
        return str(e), 500