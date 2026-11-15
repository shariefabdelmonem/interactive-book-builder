import json, re, textwrap
from blocks import blocks
from imgtools import hlines
D = json.load(open('all.json'))
B = {}
def blk(n):
    if n not in B: B[n] = blocks(n)
    return B[n]
def blanks(n): return D[str(n)]['blanks']

FS = 16          # default answer size (pt)
ZONES = {}

def T(x0, x1, y, txt, fs=FS): return {'k': 't', 'x0': x0, 'x1': x1, 'y': y, 'txt': txt, 'fs': fs}
def C(b): return {'k': 'c', 'b': b}
def on_blank(b, txt, fs=FS, left=False):
    x0, y0, x1, y1 = b[:4]
    return T(x0 + 3, None, y1 - 4, txt, fs) if left else T(x0, x1, y1 - 4, txt, fs)
def ebox(e):
    if e['k'] == 'c': return e['b']
    w = len(e['txt']) * e['fs'] * .45
    x0 = e['x0'] if e['x1'] is None else (e['x0'] + e['x1']) / 2 - w / 2
    return [x0, e['y'] - e['fs'], x0 + w, e['y'] + 3]
def Z(n, label, els, key, flag=None, extra=None, pop=None):
    bs = [ebox(e) for e in els] + ([extra] if extra else [])
    x0 = min(b[0] for b in bs); y0 = min(b[1] for b in bs); x1 = max(b[2] for b in bs); y1 = max(b[3] for b in bs)
    box = [round(min(x0, 44), 1), round(y0 - 4, 1), round(max(x1, 556), 1), round(y1 + 4, 1)]
    ZONES.setdefault(n, []).append({'id': f'{n}-{len(ZONES.get(n, []))}', 'label': label, 'box': box, 'a': els, 'key': key, 'flag': flag, 'pop': pop})

def mcq(n, bi, letter, gap=True, label=None, flag=None):
    b = blk(n)[bi]
    opt = [o for o in b['opts'] if o[4].strip().startswith(letter + '.')][0]
    els = [C([opt[0] - 2, opt[1] + 1, opt[2] + 2, opt[3] - 1])]
    txt = re.sub(r'^[A-D]\.\s*', '', opt[4]).strip()
    if gap and b['blanks']: els.append(on_blank(b['blanks'][0], txt))
    num = re.match(r'^(\d+)', b['head'][4])
    Z(n, label or (f'Q{num.group(1)}' if num else 'Q'), els, f'{letter}. {txt}', flag, extra=b['head'][:4])

def fill(n, bi, txt, label=None, flag=None, k=0, fs=FS):
    b = blk(n)[bi]
    num = re.match(r'^(\d+)', b['head'][4])
    Z(n, label or (f'{num.group(1)}' if num else 'Q'), [on_blank(b['blanks'][k], txt, fs)], txt, flag, extra=b['head'][:4])

def pblank(n, idx_txt, label, fs=FS, left=False, flag=None):
    bl = blanks(n)
    els = [on_blank(bl[i], t, fs, left) for i, t in idx_txt]
    Z(n, label, els, ' / '.join(t for _, t in idx_txt), flag)

def seg(s, txt, fs=FS, left=False):  # image-detected line [x0,x1,y]
    x0, x1, y = s
    return T(x0 + 3, None, y - 3, txt, fs) if left else T(x0, x1, y - 3, txt, fs)

