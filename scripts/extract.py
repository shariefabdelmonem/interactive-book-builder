"""Render every PDF page and dump text lines + blanks with coordinates (PDF points).
usage: python3 extract.py book.pdf BOOK_DIR   -> BOOK_DIR/img/p{n}.jpg + BOOK_DIR/all.json
Then run every other script with:  BOOK_DIR=<that folder> python3 ...   (default: current folder)"""
import json, re, sys, os
try: import pymupdf as fitz
except ImportError: import fitz
from PIL import Image
if len(sys.argv) != 3: sys.exit(__doc__)
pdf, book = sys.argv[1], sys.argv[2]
os.makedirs(book + '/img', exist_ok=True)
d = fitz.open(pdf); out = {}
for i, p in enumerate(d):
    n = i + 1; pix = p.get_pixmap(dpi=160)
    Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(f'{book}/img/p{n}.jpg', quality=80, optimize=True)
    lines = [[round(v, 1) for v in l['bbox']] + [''.join(s['text'] for s in l['spans']).strip()] for b in p.get_text('dict')['blocks'] for l in b.get('lines', [])]
    lines = [l for l in lines if l[4]]
    blanks = [[round(v, 1) for v in w[:4]] + [w[4]] for w in p.get_text('words') if re.search(r'_{3,}|…|\.{4,}', w[4])]
    out[n] = {'lines': sorted(lines, key=lambda r: (round(r[1] / 4), r[0])), 'blanks': sorted(blanks, key=lambda r: (round(r[1] / 4), r[0]))}
json.dump(out, open(book + '/all.json', 'w'), ensure_ascii=False)
print(d.page_count, 'pages ->', book, '| page size (pt):', round(d[0].rect.width, 2), 'x', round(d[0].rect.height, 2))
