"""Inline page images + fonts into one offline HTML.
usage: python3 build_offline.py BOOK_DIR OUT.html FIRST_PAGE LAST_PAGE
needs: npm i @fontsource/cairo @fontsource/caveat  (in /tmp/fonts)"""
import base64,re,sys
book,out,a,b=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
F='/tmp/fonts/node_modules/@fontsource/'
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
css=''
for fam,files in [('Caveat',[('700','caveat/files/caveat-latin-700-normal.woff2',None)]),
  ('Cairo',[(w,f'cairo/files/cairo-{s}-{w}-normal.woff2',s) for w in ('500','700','800') for s in ('latin','arabic')])]:
  for w,p,s in files:
    rng='unicode-range:U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF;' if s=='arabic' else ''
    css+=f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:block;{rng}src:url(data:font/woff2;base64,{b64(F+p)}) format('woff2')}}\n"
s=open(book+'/index.html').read()
s=re.sub(r'<link rel="preconnect"[^>]*>\s*','',s)
s=re.sub(r'<link href="https://fonts.googleapis.com[^>]*>','<style>'+css+'</style>',s)
imgs='{'+','.join(f'{n}:"data:image/jpeg;base64,{b64(f"{book}/img/p{n}.jpg")}"' for n in range(a,b+1))+'}'
s=s.replace('const DATA=','const IMG='+imgs+';\nconst DATA=',1)
s=s.replace("`img/p${p}.jpg`","IMG[p]").replace("`url(img/p${front}.jpg)`","`url(${IMG[front]})`").replace("`url(img/p${back}.jpg)`","`url(${IMG[back]})`")
chk=re.sub(r'base64,[A-Za-z0-9+/=]+','',s)
assert 'img/p' not in chk and 'googleapis' not in chk, 'external refs left'
open(out,'w').write(s);print('wrote',out)
