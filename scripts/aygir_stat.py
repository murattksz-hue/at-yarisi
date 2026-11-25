"""Sonuç CSV'lerinden aygır (baba) istatistiği üretir.
A/E = gerçek birincilik / beklenen birincilik (beklenen = 1/koşan at sayısı).
Pazar A/E = gerçek birincilik / ganyan oranından türeyen olasılık (değer ölçüsü)."""
import sys,glob,re,json,collections
def bant(m): return 'kisa' if m<=1400 else ('orta' if m<=1900 else 'uzun')
S=collections.defaultdict(lambda: collections.defaultdict(lambda:[0,0,0.0,0.0,0]))  # n,w,exp,mexp,top3
kos=0
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    lines=open(f,encoding='utf-8-sig').read().splitlines(); hdr=None; runners=[]
    def flush():
        global kos
        if not hdr or not runners: return
        irk='Arap' if 'Arap' in hdr else ('İngiliz' if 'İngiliz' in hdr else '?')
        m=re.search(r'(\d{3,4})m',hdr); pist=next((p for p in ('Kum','Çim','Sentetik') if p in hdr),'?')
        if not m: return
        b=bant(int(m.group(1))); n=len(runners); kos+=1
        inv=[1/o for *_ ,o in runners if o>1]; tot=sum(inv) or 1
        for pos,baba,o in runners:
            mp=(1/o)/tot if o>1 else 1/n
            for key in ('genel',pist,b,pist+'_'+b):
                r=S[irk+'|'+baba][key]; r[0]+=1; r[1]+=pos==1; r[2]+=1/n; r[3]+=mp; r[4]+=pos<=3
    for l in lines:
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            flush(); hdr=l; runners=[]; continue
        if hdr and c[0].isdigit() and len(c)>13:
            try: o=float(c[13].replace(',','.'))
            except Exception: o=0
            runners.append((int(c[0]) if c[12].strip() else 99,c[3].strip(),o))
    flush()
out={k:{kk:dict(n=v[0],w=v[1],exp=round(v[2],2),mexp=round(v[3],2),top3=v[4]) for kk,v in d.items()} for k,d in S.items()}
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
print('koşu:',kos,'aygır:',len(out))
