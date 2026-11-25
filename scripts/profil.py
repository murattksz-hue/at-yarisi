"""Irk x zemin x mesafe profilleri ve hipodrom start (kulvar) etkisi. Kullanım: profil.py sonuc_dizini cikti.json"""
import sys,glob,os,re,json,collections
def bant(m): return 'kisa' if m<=1400 else ('orta' if m<=1900 else 'uzun')
def kova(s): return '1-3' if s<=3 else '4-6' if s<=6 else '7-9' if s<=9 else '10+'
P=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0.0,0.0]))  # [kazanma, beklenen(1/n), piyasa beklentisi]
K=collections.Counter(); ALAN=collections.Counter(); FAV=collections.Counter(); HPL=collections.Counter()
D=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0.0]))
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    hip=os.path.basename(f)[11:-4]; cur=None; races=[]
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            m=re.search(r'(\d{3,4})m',l)
            cur=dict(irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),bant=bant(int(m.group(1))) if m else '?',h=[]); races.append(cur); continue
        if cur and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            st=re.match(r'(\d+)',c[9]); y=re.match(r'(\d+)y',c[2]); kg=re.match(r'([\d,]+)',c[5])
            cur['h'].append(dict(pos=int(c[0]) if c[12].strip() else 99,o=o,st=int(st.group(1)) if st else 0,yas=int(y.group(1)) if y else 0,
                ap=' AP' in c[6],kg=float(kg.group(1).replace(',','.')) if kg else 0,hp=int(c[11]) if c[11].isdigit() else 0))
    for r in races:
        h=r['h']; n=len(h)
        if n<4 or r['bant']=='?': continue
        seg=f"{r['irk']}|{r['pist']}|{r['bant']}"; K[seg]+=1; ALAN[seg]+=n
        oo=[x for x in h if x['o']>1]
        if oo and min(oo,key=lambda x:x['o'])['pos']==1: FAV[seg]+=1
        if max(h,key=lambda x:x['hp'])['pos']==1: HPL[seg]+=1
        mk=max(x['kg'] for x in h); tot=sum(1/x['o'] for x in oo) or 1
        for x in h:
            w=x['pos']==1
            for k in ('start '+kova(x['st']),'yaş '+(str(x['yas']) if x['yas']<7 else '7+'),'apranti' if x['ap'] else 'usta jokey','en ağır kilo' if x['kg']==mk else 'diğer kilo'):
                P[seg][k][0]+=w; P[seg][k][1]+=1/n; P[seg][k][2]+=(1/x['o'])/tot if x['o']>1 else 0
            d=D[f"{hip}|{r['pist']}|{r['bant']}"][kova(x['st'])]; d[0]+=w; d[1]+=1/n
out={'segment':{},'kulvar':{}}
for seg in sorted(K,key=lambda s:-K[s]):
    out['segment'][seg]=dict(kosu=K[seg],ort_alan=round(ALAN[seg]/K[seg],1),favori_kazanma=round(100*FAV[seg]/K[seg],1),hp_lideri_kazanma=round(100*HPL[seg]/K[seg],1),
        ae={k:dict(ae=round(v[0]/v[1],2) if v[1] else None,piyasa_ae=round(v[0]/v[2],2) if v[2] else None) for k,v in sorted(P[seg].items())})
for k,v in D.items():
    if sum(x[1] for x in v.values())>=15:
        out['kulvar'][k]={b:round(x[0]/x[1],2) for b,x in sorted(v.items()) if x[1]>0}
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print("segment                  koşu alan fav% HPlid | start1-3 ham/piyasa  10+ | apranti | en ağır kilo | yaş (piyasa)")
for seg,s in out['segment'].items():
    a=s['ae']; g=lambda k,t='ae':a.get(k,{}).get(t) or 0
    print(f"{seg:24} {s['kosu']:4} {s['ort_alan']:4} {s['favori_kazanma']:5} {s['hp_lideri_kazanma']:5} | {g('start 1-3'):.2f}/{g('start 1-3','piyasa_ae'):.2f} {g('start 10+'):.2f}/{g('start 10+','piyasa_ae'):.2f} | {g('apranti'):.2f}/{g('apranti','piyasa_ae'):.2f} | {g('en ağır kilo'):.2f}/{g('en ağır kilo','piyasa_ae'):.2f} | 3y {g('yaş 3','piyasa_ae'):.2f} 7+ {g('yaş 7+','piyasa_ae'):.2f}")
