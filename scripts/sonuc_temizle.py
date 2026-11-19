"""Sonuç CSV'lerinden koşmayan (çekilen) atları çıkarır. Ham veri (veri/sonuc) değişmez; temiz kopya veri/sonuc_temiz.
Koşmayan at: derece sütunu 'Koşmaz' (ya da isimde '(Koşmaz)'). Kullanım: sonuc_temizle.py [kaynak] [hedef]"""
import sys,os,glob
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=sys.argv[1] if len(sys.argv)>1 else os.path.join(K,'veri','sonuc'); dst=sys.argv[2] if len(sys.argv)>2 else os.path.join(K,'veri','sonuc_temiz')
os.makedirs(dst,exist_ok=True); n=c=0
for f in glob.glob(os.path.join(src,'*.csv')):
    out=os.path.join(dst,os.path.basename(f))
    if os.path.exists(out) and os.path.getmtime(out)>=os.path.getmtime(f): continue
    L=open(f,encoding='utf-8-sig').read().splitlines(); K_=[]
    for l in L:
        p=l.split(';')
        if p[0].isdigit() and len(p)>12 and ('Koşmaz' in p[12] or '(Koşmaz)' in p[1]): c+=1; continue
        K_.append(l)
    open(out,'w',encoding='utf-8').write('\n'.join(K_)+'\n'); n+=1
print(f"{n} dosya temizlendi, {c} koşmayan at satırı çıkarıldı")
