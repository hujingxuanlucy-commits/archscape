import sys, os, json, base64, io
_vendor = os.path.join(HERE, 'pylibs')          # optional local Pillow install
if os.path.isdir(_vendor): sys.path.insert(0, _vendor)
from PIL import Image, ImageDraw, ImageFilter

REF = os.path.join(HERE, os.pardir, 'reference') + os.sep

def is_marker(p):
    r, g, b = p
    red  = r > 130 and r - g > 55 and r - b > 45
    blue = b > 110 and b - r > 35 and b - g > 15
    return red or blue

def find_blobs(im):
    """Cluster marker-coloured pixels into blobs (centre, radius)."""
    w, h = im.size
    px = im.load()
    pts = [(x, y) for y in range(0, h, 2) for x in range(0, w, 2) if is_marker(px[x, y])]
    blobs = []
    for x, y in pts:
        for b in blobs:
            if abs(x - b['x']) < 46 and abs(y - b['y']) < 46:
                b['pts'].append((x, y)); b['x'] = sum(p[0] for p in b['pts']) // len(b['pts'])
                b['y'] = sum(p[1] for p in b['pts']) // len(b['pts']); break
        else:
            blobs.append({'x': x, 'y': y, 'pts': [(x, y)]})
    out = []
    for b in blobs:
        if len(b['pts']) < 12: continue
        xs = [p[0] for p in b['pts']]; ys = [p[1] for p in b['pts']]
        cx, cy = (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2
        r = max(max(xs) - min(xs), max(ys) - min(ys)) // 2 + 7   # +7 covers the white ring
        out.append((cx, cy, r))
    return out

def inpaint(im, blobs):
    """Cover each blob with a soft-edged patch lifted from clean map nearby."""
    for cx, cy, r in blobs:
        d = r * 2
        ox = -int(r * 4.2) if cx - r * 4.2 > 0 else int(r * 4.2)
        box = (cx + ox - r, cy - r, cx + ox + r, cy + r)
        if box[0] < 0 or box[2] > im.width: continue
        patch = im.crop(box)
        mask = Image.new('L', (d, d), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, d - 1, d - 1), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(2.6))
        im.paste(patch, (cx - r, cy - r), mask)
    return im

def enc(im, w, q):
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return im, buf.getvalue()

assets = json.load(open(HERE + '/assets.json'))

# --- city map (Discover): dense organic streets, pins painted out ---
city = Image.open(REF + '02 Homepage Discovery 1.png').convert('RGB').crop((88, 285, 709, 680))
blobs = find_blobs(city)
print('city markers found:', blobs)
city = inpaint(city, blobs)
city, data = enc(city, 560, 78)
assets['map_city'] = 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
print('map_city  %dx%d  %.1f KB' % (city.width, city.height, len(data) / 1024))

# --- grid map (Journey / Crossing): clean lower half of the concept map ---
grid = Image.open(REF + '05 Concept Map 1.png').convert('RGB').crop((130, 760, 660, 1126))
blobs = find_blobs(grid)
print('grid markers found:', blobs)
grid = inpaint(grid, blobs)
grid, data = enc(grid, 530, 78)
assets['map_grid'] = 'data:image/jpeg;base64,' + base64.b64encode(data).decode()
print('map_grid  %dx%d  %.1f KB' % (grid.width, grid.height, len(data) / 1024))

json.dump(assets, open(HERE + '/assets.json', 'w'))
print('assets now:', len(assets))
