"""Profile cover: a wide architectural band cropped from the full-size
Vessel photograph, in place of the mismatched night-street/lantern shot.
"""
import sys, os, io, json, base64
HERE = os.path.dirname(os.path.abspath(__file__))
_vendor = os.path.join(HERE, 'pylibs')
if os.path.isdir(_vendor): sys.path.insert(0, _vendor)
from PIL import Image, ImageEnhance

SRC = os.path.join(HERE, os.pardir, 'archive', 'prototype-source', 'images')
RATIO = 780 / 206   # matches .pf-cover's on-screen aspect

im = Image.open(os.path.join(SRC, 'image 2.png')).convert('RGB')
w, h = im.size
# a horizontal band through the repeating honeycomb structure, avoiding the
# sky at top and the dark plaza floor at bottom
top, bottom = int(h * 0.30), int(h * 0.62)
band = im.crop((0, top, w, bottom))
bw, bh = band.size
nh = int(bw / RATIO)
y = int((bh - nh) * 0.42)
band = band.crop((0, y, bw, y + nh))

band = ImageEnhance.Color(band).enhance(0.72)       # closer to the app's muted palette
band = ImageEnhance.Contrast(band).enhance(1.05)
band = ImageEnhance.Brightness(band).enhance(0.94)

W = 900
band = band.resize((W, round(band.height * W / band.width)), Image.LANCZOS)
buf = io.BytesIO()
band.save(buf, 'JPEG', quality=82, optimize=True, progressive=True)
data = buf.getvalue()
print('prof_cover   %4dx%-4d %7.1f KB' % (band.width, band.height, len(data) / 1024))

assets = json.load(open(os.path.join(HERE, 'assets.json')))
assets['prof_cover'] = 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
json.dump(assets, open(os.path.join(HERE, 'assets.json'), 'w'))
