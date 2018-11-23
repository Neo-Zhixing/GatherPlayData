from app import app

from flask import request
import requests
from colorthief import ColorThief

color_thief = ColorThief('/path/to/imagefile')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=6)

@app.route('/utils/imgcolor/<cachekey>', methods=['GET'])
def imgcolor():
	return 'Hello World!'



f = open('00000001.jpg','wb')
f.write(requests.get('http://www.gunnerkrigg.com//comics/00000001.jpg').content)
f.close()