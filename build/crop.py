import sys, os, json, base64, io
HERE = os.path.dirname(os.path.abspath(__file__))
_vendor = os.path.join(HERE, 'pylibs')          # optional local Pillow install
if os.path.isdir(_vendor): sys.path.insert(0, _vendor)
from PIL import Image

REF = os.path.join(HERE, os.pardir, 'archive', 'prototype-source', 'reference')

# key: (file, x1, y1, x2, y2, target_width, quality)
CROPS = {
  'onb_brick':   ('01 Onboarding 1.png',        0,  250, 200,  670, 300, 70),
  'onb_glass':   ('01 Onboarding 1.png',      145,  300, 420,  665, 360, 70),
  'onb_night':   ('01 Onboarding 1.png',      425,  245, 590,  650, 300, 70),
  'onb_lattice': ('01 Onboarding 1.png',      590,  200, 797,  710, 320, 70),

  'k11':         ('02 Homepage Discovery 1.png', 40, 770, 324, 1050, 340, 74),
  'tate':        ('02 Homepage Discovery 1.png',354, 860, 638, 1150, 340, 74),
  'feedthumb':   ('02 Homepage Discovery 1.png', 65,1258, 218, 1428, 200, 72),

  'ar_facade':   ('03 AR Camera 1.png',          0,  230, 798,  810, 760, 74),

  'checkin':     ('04 Checkin Edit 1.png',      40,  190, 757,  588, 720, 74),

  'prof_cover':  ('06 User Profile 1.png',       0,   88, 797,  305, 780, 74),
  'w1':          ('06 User Profile 1.png',       2,  966, 266, 1196, 300, 74),
  'w2':          ('06 User Profile 1.png',     271,  900, 535, 1196, 300, 74),
  'w3':          ('06 User Profile 1.png',     540,  900, 795, 1196, 300, 74),
  'w4':          ('06 User Profile 1.png',       2, 1204, 266, 1490, 300, 74),
  'w5':          ('06 User Profile 1.png',     271, 1204, 535, 1490, 300, 74),
  'w6':          ('06 User Profile 1.png',     540, 1204, 795, 1490, 300, 74),

  'arc_bcn':     ('07 Travel Archive 1.png',   108,  300, 272,  450, 220, 74),
  'arc_tky':     ('07 Travel Archive 1.png',   108,  520, 272,  670, 220, 74),
  'arc_par':     ('07 Travel Archive 1.png',   108,  740, 272,  890, 220, 74),

  'insp_heydar': ('08 Inspiration Library 1.png', 40, 300, 390,  690, 380, 72),
  'insp_stair':  ('08 Inspiration Library 1.png',402, 300, 675,  452, 380, 72),
  'insp_pavil':  ('08 Inspiration Library 1.png',402, 462, 757,  745, 380, 72),
  'insp_bw':     ('08 Inspiration Library 1.png', 40, 757, 390,  958, 380, 72),
  'insp_nest':   ('08 Inspiration Library 1.png',402, 757, 757,  958, 380, 72),
  'insp_glass':  ('08 Inspiration Library 1.png', 40, 968, 757, 1178, 700, 72),

  'duomo':       ('09 Community Feed 1.png',     0,  325, 797,  830, 740, 74),
  'highline':    ('09 Community Feed 1.png',     0, 1112, 797, 1502, 740, 74),

  'kn_hero':     ('11 Knowledge Search 1.png',   0,   50, 798,  172, 798, 74),
  'kn_barbican': ('11 Knowledge Search 1.png',  40,  640, 390,  938, 380, 72),
  'kn_habitat':  ('11 Knowledge Search 1.png', 402,  640, 757,  938, 380, 72),
  'kn_trellick': ('11 Knowledge Search 1.png',  40, 1076, 757, 1240, 700, 74),
  'w7':          ('03 AR Camera 1.png',        40, 1150, 430, 1440, 300, 74),
  'w8':          ('09 Community Feed 1.png',    0,  380, 300,  760, 300, 74),
  'w9':          ('09 Community Feed 1.png',  480,  340, 797,  720, 300, 74),
  'w10':         ('09 Community Feed 1.png',    0, 1150, 330, 1480, 300, 74),
  'w11':         ('06 User Profile 1.png',    230,  100, 560,  300, 300, 74),
  'w12':         ('04 Checkin Edit 1.png',     60,  210, 380,  560, 300, 74),
}

out = {}
total = 0
for key, (fn, x1, y1, x2, y2, tw, q) in CROPS.items():
    im = Image.open(os.path.join(REF, fn)).convert('RGB')
    im = im.crop((x1, y1, x2, y2))
    if im.width > tw:
        h = round(im.height * tw / im.width)
        im = im.resize((tw, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    b = buf.getvalue()
    total += len(b)
    out[key] = 'data:image/jpeg;base64,' + base64.b64encode(b).decode()
    print(f'{key:14s} {im.width:4d}x{im.height:4d}  {len(b)/1024:7.1f} KB')

print(f'\nTOTAL {total/1024:.1f} KB  ({len(out)} assets)')
with open(os.path.join(HERE, 'assets.json'), 'w') as f:
    json.dump(out, f)
