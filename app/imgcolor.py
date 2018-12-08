from app import app

from flask import request, jsonify
import requests
from PIL import ImageColor
from .color_thief import ColorThief

from .utils.cached import Cached

def encodeImgColor(palette):
	return ':'.join(palette)

def decodeImgColor(colorStr):
	return colorStr.split(':')

def rgb2hex(color):
    return '{:02x}{:02x}{:02x}'.format(*color)


imgcolorCache = Cached('imgcolor', ttl=3600, encoder=encodeImgColor, decoder=decodeImgColor)
@app.route('/utils/imgcolor/<cachekey>', methods=['GET'])
def imgcolor(cachekey):
	redis_cached = imgcolorCache.get(cachekey)
	if redis_cached:
		return jsonify(redis_cached)
	else:
		response = requests.get('https://s3.amazonaws.com/btoimage/prism-thumbnails/articles/bb8c-2016107-coldplay.jpg-resize_then_crop-_frame_bg_color_FFF-h_1365-gravity_center-q_70-preserve_ratio_true-w_2048_.jpg', stream=True)
		response.raw.decode_content = True

		color_thief = ColorThief(response.raw)
		palette = list(map(rgb2hex, color_thief.get_palette(color_count=6)))
		imgcolorCache.set(cachekey, palette)
		return jsonify(palette)
