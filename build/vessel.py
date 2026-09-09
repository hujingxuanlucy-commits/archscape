"""Extract Vessel imagery (images/) for the capture flow and building record."""
import sys, os, io, json, base64
HERE = os.path.dirname(os.path.abspath(__file__))
_vendor = os.path.join(HERE, 'pylibs')
if os.path.isdir(_vendor): sys.path.insert(0, _vendor)
from PIL import Image

SRC = os.path.join(HERE, os.pardir, 'images')

def crop_to(im, aspect):
    """Centre-crop to the given width/height ratio."""
    w, h = im.size
    if w / h > aspect:
        nw = int(h * aspect); return im.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
    nh = int(w / aspect);     return im.crop((0, (h - nh) // 2, w, (h + nh) // 2))

# key: (file, target aspect w/h, output width, quality)
JOBS = {
    'vessel_ar':   ('image 1.png', 393 / 852, 480, 74),   # held-up viewfinder, whole structure
    'vessel_shot': ('image 3.png', 720 / 380, 720, 74),   # the capture itself
    'vessel_hero': ('image 4.png', 740 / 430, 740, 74),   # building page hero, in context
    'vessel_a':    ('image 2.png', 1.0,       320, 74),
    'vessel_b':    ('image 5.png', 1.0,       320, 74),
    'vessel_c':    ('image 6.png', 1.0,       320, 74),
}

assets = json.load(open(os.path.join(HERE, 'assets.json')))
total = 0
for key, (fn, aspect, w, q) in JOBS.items():
    im = Image.open(os.path.join(SRC, fn)).convert('RGB')
    im = crop_to(im, aspect)
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    data = buf.getvalue(); total += len(data)
    assets[key] = 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
    print('%-12s %4dx%-4d %7.1f KB' % (key, im.width, im.height, len(data) / 1024))

json.dump(assets, open(os.path.join(HERE, 'assets.json'), 'w'))
print('added %.1f KB; %d assets total' % (total / 1024, len(assets)))
