"""Photo/scan of a page -> clean page image ready for the pipeline.
usage: python3 image_to_page.py in.jpg out.jpg
Finds the paper quad (largest bright 4-corner contour), warps it flat, whitens the background.
If no quad is found the image is only auto-contrasted. Always check the result visually."""
import sys,numpy as np
from PIL import Image,ImageOps
import cv2
src,dst=sys.argv[1],sys.argv[2]
im=cv2.imread(src)
if im is None: sys.exit('cannot read '+src)
g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);g=cv2.GaussianBlur(g,(5,5),0)
e=cv2.Canny(g,50,150);e=cv2.dilate(e,None,iterations=2)
cs,_=cv2.findContours(e,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);quad=None
for c in sorted(cs,key=cv2.contourArea,reverse=True)[:5]:
    a=cv2.approxPolyDP(c,.02*cv2.arcLength(c,True),True)
    if len(a)==4 and cv2.contourArea(a)>.3*im.shape[0]*im.shape[1]:quad=a.reshape(4,2).astype('float32');break
if quad is not None:
    s=quad.sum(1);d=np.diff(quad,axis=1).ravel();q=np.array([quad[s.argmin()],quad[d.argmin()],quad[s.argmax()],quad[d.argmax()]])
    w=int(max(np.linalg.norm(q[0]-q[1]),np.linalg.norm(q[2]-q[3])));h=int(max(np.linalg.norm(q[0]-q[3]),np.linalg.norm(q[1]-q[2])))
    im=cv2.warpPerspective(im,cv2.getPerspectiveTransform(q,np.float32([[0,0],[w,0],[w,h],[0,h]])),(w,h))
col=cv2.cvtColor(im,cv2.COLOR_BGR2RGB);out=Image.fromarray(col);out=ImageOps.autocontrast(out,cutoff=1)
out.save(dst,quality=90);print('quad' if quad is not None else 'no quad found','->',dst,out.size)
