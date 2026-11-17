"""Fill templates/answers-flipbook.html -> BOOK_DIR/index.html
usage: python3 make_index.py BOOK_DIR DATA.json "Book title" [TOC.json]
 DATA.json : zones dumped by your answer spec (see examples/*: json.dump(ZONES ...)), keys = page numbers
 TOC.json  : optional [{"p":3,"t":"Unit 1"}...]; default = one entry per page that has zones
NPAGES is taken from the img/ folder. Page 0 = cover (img/p0.jpg), pages 1..N = book pages."""
import json, os, sys, glob, re
if len(sys.argv) < 4: sys.exit(__doc__)
book, data, title = sys.argv[1], sys.argv[2], sys.argv[3]
D = json.load(open(data))
n = max(int(re.search(r'p(\d+)\.jpg', f).group(1)) for f in glob.glob(book + '/img/p*.jpg'))
toc = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else [{'p': int(k), 't': f'Page {k}'} for k in sorted(D, key=int) if D[k]]
t = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates', 'answers-flipbook.html'), encoding='utf-8').read()
t = t.replace('{{TITLE}}', title).replace('{{NPAGES}}', str(n)).replace('{{TOC}}', json.dumps(toc, ensure_ascii=False)).replace('/*DATA*/null', json.dumps(D, ensure_ascii=False))
open(book + '/index.html', 'w', encoding='utf-8').write(t)
print('wrote', book + '/index.html', '| pages', n, '| zones', sum(len(v) for v in D.values()))
