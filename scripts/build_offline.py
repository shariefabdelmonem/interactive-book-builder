"""Inline page images + fonts (+ three.js if the page uses it) into ONE offline HTML.
usage: python3 build_offline.py BOOK_DIR OUT.html FIRST_PAGE LAST_PAGE
Works for all three templates (answers / science-3d / math). Needs node+npm once (auto-installed into $FONTS_DIR, default /tmp/fonts)."""
import base64, re, sys, os, subprocess
if len(sys.argv) != 5: sys.exit(__doc__)
book, out, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
FD = os.environ.get('FONTS_DIR', '/tmp/fonts'); N = FD + '/node_modules/'
s = open(book + '/index.html', encoding='utf-8').read()
uses3d = 'importmap' in s
need = ['@fontsource/cairo', '@fontsource/caveat'] + (['three@0.160.0'] if uses3d else [])
if not os.path.exists(N + '@fontsource/cairo'):
    os.makedirs(FD, exist_ok=True)
    subprocess.run(['npm', 'i', '--prefix', FD, *need], check=True)
elif uses3d and not os.path.exists(N + 'three'):
    subprocess.run(['npm', 'i', '--prefix', FD, 'three@0.160.0'], check=True)
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
F = N + '@fontsource/'
css = ''
for fam, files in [('Caveat', [('700', 'caveat/files/caveat-latin-700-normal.woff2', None)]),
                   ('Cairo', [(w, f'cairo/files/cairo-{x}-{w}-normal.woff2', x) for w in ('400', '500', '600', '700', '800') for x in ('latin', 'arabic')])]:
    for w, p, x in files:
        if not os.path.exists(F + p): continue          # weight not shipped -> skip
        rng = 'unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF;' if x == 'arabic' else ''
        css += f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:block;{rng}src:url(data:font/woff2;base64,{b64(F + p)}) format('woff2')}}\n"
s = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', s)
s = re.sub(r'<link href="https://fonts.googleapis.com[^>]*>', '<style>' + css + '</style>', s)
imgs = '{' + ','.join(f'{n}:"data:image/jpeg;base64,{b64(f"{book}/img/p{n}.jpg")}"' for n in range(a, b + 1) if os.path.exists(f'{book}/img/p{n}.jpg')) + '}'
s = re.sub(r'`url\(img/p\$\{(\w+)\}\.jpg\)`', r'`url(${IMG[\1]})`', s)   # css background refs
s = re.sub(r'`img/p\$\{(\w+)\}\.jpg`', r'IMG[\1]', s)                    # src refs
s = re.sub(r"'img/p(\d+)\.jpg'", lambda m: f"IMG[{m.group(1)}]", s)     # fixed single-page refs
inject = '<script>const IMG=' + imgs + ';</script>\n'
if uses3d:   # three.js -> data: URLs in the import map (bare 'three' is also resolved inside OrbitControls)
    core = 'data:text/javascript;base64,' + b64(N + 'three/build/three.module.js')
    oc = open(N + 'three/examples/jsm/controls/OrbitControls.js', encoding='utf-8').read()
    oc = 'data:text/javascript;base64,' + base64.b64encode(oc.encode()).decode()
    s = re.sub(r'<script type="importmap">.*?</script>', '<script type="importmap">{"imports":{"three":"%s","three/addons/controls/OrbitControls.js":"%s"}}</script>' % (core, oc), s, flags=re.S)
    assert not re.search(r"from 'three/addons/(?!controls/OrbitControls\.js)", s), 'template imports another three addon: add it to build_offline.py'
i = s.index('<script', s.index('</script>') + 9) if uses3d else s.index('<script')
s = s[:i] + inject + s[i:]
chk = re.sub(r'(base64|data:[a-z/]+;base64),[A-Za-z0-9+/=]+', '', s)
assert 'img/p' not in chk and 'googleapis' not in chk and 'jsdelivr' not in chk, 'external refs left'
open(out, 'w', encoding='utf-8').write(s); print('wrote', out, round(len(s) / 1e6, 1), 'MB')
