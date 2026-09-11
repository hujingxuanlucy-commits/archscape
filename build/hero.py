"""Onboarding hero: one full-bleed architectural photograph, in monochrome.

The landing screen carries the whole identity in a single frame, so this is
cut from the full-size original rather than a mockup, and reduced to
grayscale: the red in the UI chrome is then the only colour on the screen.
"""
import sys, os, io, json, base64
HERE = os.path.dirname(os.path.abspath(__file__))
_vendor = os.path.join(HERE, 'pylibs')
if os.path.isdir(_vendor): sys.path.insert(0, _vendor)
from PIL import Image, ImageOps, ImageEnhance

SRC = os.path.join(HERE, os.pardir, 'images')
RATIO = 393 / 378.0   # the hero's on-screen aspect
W, Q = 780, 74

im = Image.open(os.path.join(SRC, 'image 3.png')).convert('RGB')
w, h = im.size
nh = int(w / RATIO)
if nh > h:                     # the frame is wider than the hero: crop its sides
    nw = int(h * RATIO)
    x = int((w - nw) * 0.5)
    im = im.crop((x, 0, x + nw, h))
else:
    y = int((h - nh) * 0.5)
    im = im.crop((0, y, w, y + nh))

im = ImageOps.grayscale(im).convert('RGB')
im = ImageEnhance.Contrast(im).enhance(1.2)
im = ImageEnhance.Brightness(im).enhance(0.98)

im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
buf = io.BytesIO()
im.save(buf, 'JPEG', quality=Q, optimize=True, progressive=True)
data = buf.getvalue()
print('onb_hero  %4dx%-4d %7.1f KB' % (im.width, im.height, len(data) / 1024))

p = os.path.join(HERE, 'assets.json')
assets = json.load(open(p))
assets['onb_hero'] = 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
json.dump(assets, open(p, 'w'))
print('%d assets total' % len(assets))
