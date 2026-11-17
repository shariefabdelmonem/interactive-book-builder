import json,re,os
BOOK=os.environ.get('BOOK_DIR','.')
D=json.load(open(f'{BOOK}/all.json'))
HDR=re.compile(r'^([A-D]\.|[A-D]\))\s*(Circle|Put|Choose|Fill|Correct|Rewrite|Complete|Read the text|Write|Answer|Match)',re.I)
NUM=re.compile(r'^\d+\s*[\.\-\)]\s*\S')
OPT=re.compile(r'^[A-D]\.\s*\S')
def blocks(n):
    L=[l for l in D[str(n)]['lines'] if l[1]>53 and l[1]<800]
    L.sort(key=lambda r:(r[1],r[0]))
    B=[];cur=None
    for l in L:
        t=l[4]
        if HDR.match(t) or (NUM.match(t)):
            cur={'head':l,'lines':[l]};B.append(cur)
        elif cur: cur['lines'].append(l)
    for b in B:
        y0=b['head'][1];y1=max(l[3] for l in b['lines'])
        b['opts']=[l for l in b['lines'][1:] if OPT.match(l[4]) and not HDR.match(l[4])]
        b['blanks']=[w for w in D[str(n)]['blanks'] if y0-1<=(w[1]+w[3])/2<=y1+1]
        b['box']=[min(l[0] for l in b['lines']),y0,max(l[2] for l in b['lines']),y1]
    return B
if __name__=='__main__':
    import sys
    for n in map(int,sys.argv[1:]):
        print('==== PAGE',n)
        for i,b in enumerate(blocks(n)):
            print(f"[{i}] {b['head'][4][:70]!r} opts={[o[4][:18] for o in b['opts']]} blanks={len(b['blanks'])}")
