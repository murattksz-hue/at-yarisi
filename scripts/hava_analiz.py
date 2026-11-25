"""Hava etkisi: ıslaklık ve sıcaklığa göre sonuçlar. Kullanım: hava_analiz.py sonuc_dizini hava_gecmis.json cikti.json"""
import sys,glob,os,re,json,collections
H=json.load(open(sys.argv[2],encoding='utf-8'))
def kat(i): return 'kuru' if i<1 else ('hafif' if i<5 else 'ıslak')
def sic(t): return 'soğuk(<12)' if t<12 else ('ılık' if t<28 else 'sıcak(28+)')
def bant(m): return 'kisa' if m<=1400 else ('orta' if m<=1900 else 'uzun')
S=collections.defaultdict(lambda:dict(k=0,fav=0,hpl=0.0,alan=0,ic=[0,0.0],dis=[0,0.0],ayg=collections.defaultdict(lambda:[0,0.0,0])))
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    b=os.path.basename(f); hv=H.get(b[:-4])
    if not hv: continue
    cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            m=re.search(r'(\d{3,4})m',l); cur=dict(irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),h=[]); rs.append(cur); continue
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            st=re.match(r'(\d+)',c[9]); cur['h'].append(dict(pos=int(c[0]) if c[12].strip() else 99,o=o,hp=int(c[11]) if c[11].isdigit() else 0,baba=c[3].strip(),st=int(st.group(1)) if st else 0))
    for r in rs:
        h=r['h']
        if len(h)<4: continue
        oo=[x for x in h if x['o']>1]; tot=sum(1/x['o'] for x in oo) or 1
        for key in (f"{r['irk']}|{r['pist']}|{kat(hv['islaklik'])}",f"tümü|{r['pist']}|{kat(hv['islaklik'])}",f"tümü|sıcaklık|{sic(hv['sicaklik'] or 20)}"):
            s=S[key]; s['k']+=1; s['alan']+=len(h)
            if oo and min(oo,key=lambda x:x['o'])['pos']==1: s['fav']+=1
            mh=max(x['hp'] for x in h); L=[x for x in h if x['hp']==mh and mh>0]
            if L: s['hpl']+=sum(x['pos']==1 for x in L)/len(L)
            for x in h:
                mp=(1/x['o'])/tot if x['o']>1 else 0; w=x['pos']==1
                if 1<=x['st']<=3: s['ic'][0]+=w; s['ic'][1]+=mp
                if x['st']>=10: s['dis'][0]+=w; s['dis'][1]+=mp
                if key.startswith('tümü|') and 'sıcaklık' not in key: a=s['ayg'][r['irk']+'|'+x['baba']]; a[0]+=w; a[1]+=mp; a[2]+=1
out={}
print(f"{'grup':28} koşu  alan  favori%  HPlideri%  iç(1-3) piyasa-A/E  dış(10+)")
for k in sorted(S):
    s=S[k]
    if s['k']<10: continue
    ae=lambda v:round(v[0]/v[1],2) if v[1] else None
    out[k]=dict(kosu=s['k'],alan=round(s['alan']/s['k'],1),favori=round(100*s['fav']/s['k'],1),hp_lideri=round(100*s['hpl']/s['k'],1),ic_ae=ae(s['ic']),dis_ae=ae(s['dis']))
    o=out[k]; print(f"{k:28} {o['kosu']:4} {o['alan']:5} {o['favori']:7} {o['hp_lideri']:9}  {o['ic_ae']}  {o['dis_ae']}")
# aygır: ıslakta vs kuruda (piyasaya göre)
A=collections.defaultdict(dict)
for k,s in S.items():
    if k.startswith('tümü|') and 'sıcaklık' not in k:
        pist,kt=k.split('|')[1:]
        for a,v in s['ayg'].items():
            d=A[a].setdefault(kt,[0,0.0,0]); d[0]+=v[0]; d[1]+=v[1]; d[2]+=v[2]
cam={}
for a,d in A.items():
    if 'ıslak' in d and d['ıslak'][2]>=25 and 'kuru' in d and d['kuru'][2]>=60:
        cam[a]=dict(islak_ae=round((d['ıslak'][0]+2)/(d['ıslak'][1]+2),2),kuru_ae=round((d['kuru'][0]+2)/(d['kuru'][1]+2),2),islak_kosu=d['ıslak'][2])
print("\nIslak pistte piyasaya göre en iyi / en kötü aygırlar (en az 25 ıslak koşu):")
srt=sorted(cam.items(),key=lambda kv:-(kv[1]['islak_ae']-kv[1]['kuru_ae']))
for a,v in srt[:10]+[('...',{})]+srt[-6:]:
    print(f"  {a:34} {v}" if v else '  ...')
out['aygir_islak']=cam
json.dump(out,open(sys.argv[3],'w'),ensure_ascii=False,indent=1)
