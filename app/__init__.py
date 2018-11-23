from flask import Flask, redirect

app = Flask(__name__)

from . import imgcolor

@app.route('/')
def index():
    return redirect('https://gather-play.com', code=302)
