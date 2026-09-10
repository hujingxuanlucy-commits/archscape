"""Full-bleed viewfinder frames at phone aspect, from the full-size originals.

The camera is the one place a soft image is obvious: it fills the screen and
it is meant to read as a live frame. These are cut from images/ at 3000-4200px
rather than from the 797px mockups, so they stay sharp at 2x.
"""
import sys, os, io, json, base64
HERE = os.path.dirname(os.path.abspath(__file__))
_vendor = os.path.join(HERE, 'pylibs')
if os.path.isdir(_vendor): sys.path.insert(0, _vendor)
from PIL import Image

SRC = os.path.join(HERE, os.pardir, 'images')
PHONE = 393 / 852          # viewfinder aspect
W, Q = 620, 80             # ~1.6x the CSS width, high enough for 2x screens

def crop_to(im, aspect, bias=0.5):
    """Crop to the given ratio; bias shifts the window vertically (0 = top)."""
    w, h = im.size
    if w / h > aspect:
        nw = int(h * aspect)
        x = int((w - nw) * 0.5)
        return im.crop((x, 0, x + nw, h))
    nh = int(w / aspect)
    y = int((h - nh) * bias)
    return im.crop((0, y, w, y + nh))

# key: (file, vertical bias) - six viewpoints of the same structure
JOBS = [
    ('shot_v1', 'image 1.png', 0.50),
    ('shot_v2', 'image 3.png', 0.42),
    ('shot_v3', 'image 4.png', 0.46),
    ('shot_v4', 'image 2.png', 0.44),
    ('shot_v5', 'image 5.png', 0.48),
    ('shot_v6', 'image 6.png', 0.40),
]

assets = json.load(open(os.path.join(HERE, 'assets.json')))
total = 0
for key, fn, bias in JOBS:
    im = Image.open(os.path.join(SRC, fn)).convert('RGB')
    im = crop_to(im, PHONE, bias)
    if im.width > W:
        im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=Q, optimize=True, progressive=True)
    data = buf.getvalue(); total += len(data)
    assets[key] = 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
    print('%-9s %4dx%-5d %7.1f KB' % (key, im.width, im.height, len(data) / 1024))

json.dump(assets, open(os.path.join(HERE, 'assets.json'), 'w'))
print('added %.1f KB; %d assets total' % (total / 1024, len(assets)))
