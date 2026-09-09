import json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(HERE, 'app.template.html'), encoding='utf-8').read()

style_a = tpl.index('<style>')
style_b = tpl.index('</style>')
js_a    = tpl.index('<script>\n(function')

# Non-ASCII inside <style> can't be entity-escaped; make sure there is none.
bad = [c for c in tpl[style_a:style_b] if ord(c) > 127]
if bad:
    sys.exit('non-ASCII in <style>: %r' % set(bad))

def html_esc(t):
    return ''.join(c if ord(c) < 128 else '&#x%X;' % ord(c) for c in t)

def js_esc(t):
    return ''.join(c if ord(c) < 128 else '\\u%04X' % ord(c) for c in t)

out = html_esc(tpl[:js_a]) + js_esc(tpl[js_a:])

assets = open(os.path.join(HERE, 'assets.json'), encoding='utf-8').read()
assert '__ASSETS__' in out
out = out.replace('__ASSETS__', assets)

assert not [c for c in out if ord(c) > 127], 'still non-ASCII'
open(os.path.join(HERE, os.pardir, 'archscape.html'), 'w', encoding='ascii').write(out)
print('built  %.2f MB  pure ASCII' % (len(out) / 1024 / 1024))
