from flask import Flask, redirect

app = Flask(__name__)

# Initialize Redis
import redis as redis_db
from config import REDIS
redis = redis_db.Redis(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'], password=REDIS['password'])

# Initialize MongoDB
from pymongo import MongoClient
from config import MONGODB_URL
mongo = MongoClient(MONGODB_URL).analysis

# Initialize Memcache
import bmemcached
from config import MEMCACHED
memcached = bmemcached.Client(MEMCACHED['host'], MEMCACHED['username'], MEMCACHED['password'])

from . import imgcolor

@app.route('/')
def index():
    return redirect('https://gather-play.com', code=302)
