import numpy as np, json, pytesseract
from PIL import Image
S=72/160  # px -> pt
_cache={}
def arr(n):
    if n not in _cache: _cache[n]=np.asarray(Image.open(f'BOOK_DIR/img/p{n}.jpg').convert('L')).astype(int)
    return _cache[n]
def hlines(n,box=None,minlen=40,dark=150):
    a=arr(n);H,W=a.shape
    x0,y0,x1,y1=[int(v/S) for v in (box or (0,60,595,800))]
    segs=[]
    for y in range(y0,y1):
        row=a[y,x0:x1]<dark
        # runs
        d=np.diff(np.concatenate([[0],row.astype(int),[0]]))
        st=np.where(d==1)[0];en=np.where(d==-1)[0]
        for s,e in zip(st,en):
            if e-s>=minlen:
                # thin: pixel above/below mostly light
                above=(a[max(0,y-3),x0+s:x0+e]<dark).mean(); below=(a[min(H-1,y+3),x0+s:x0+e]<dark).mean()
                if above<.3 and below<.3: segs.append([x0+s,x0+e,y])
    # merge consecutive rows
    segs.sort(key=lambda s:(s[2],s[0]));out=[]
    for s in segs:
        if any(abs(o[2]-s[2])<=4 and abs(o[0]-s[0])<8 and abs(o[1]-s[1])<8 for o in out[-12:]): continue
        out.append(s)
    out.sort(key=lambda s:(round(s[2]/4),s[0]))
    return [[round(float(s[0])*S,1),round(float(s[1])*S,1),round(float(s[2])*S,1)] for s in out]
def ocr(n,box=None):
    im=Image.open(f'BOOK_DIR/img/p{n}.jpg')
    if box: x0,y0,x1,y1=[int(v/S) for v in box]; im=im.crop((x0,y0,x1,y1))
    else: x0=y0=0
    dd=pytesseract.image_to_data(im,output_type=pytesseract.Output.DICT)
    W=[]
    for i,t in enumerate(dd['text']):
        if t.strip(): W.append([round((dd['left'][i]+x0)*S,1),round((dd['top'][i]+y0)*S,1),round((dd['left'][i]+dd['width'][i]+x0)*S,1),round((dd['top'][i]+dd['height'][i]+y0)*S,1),t])
    return W
