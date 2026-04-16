from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url: return "No URL", 400
    res = requests.get(url)
    return Response(res.content)

@app.route('/')
def home():
    return open('index.html', encoding='utf-8').read()
