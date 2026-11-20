"""Kazananın AGF hareketi: sabah ilk AGF (ILK_<hip>.csv) → koşudan önceki son kayıt; alandaki artış sırası. Kullanım: agf_hareket.py YYYY-AA-GG [...]"""
import json,glob,os,re,sys,urllib.request
EB={'Antalya':'ANTALYA','İzmir':'IZMIR'}
def csvagf(f):
    D={};k=None
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';'); m=re.match(r'^(\d+)\. Kosu',c[0])
        if m: k=m.group(1); continue
        if k and c[0].isdigit() and len(c)>10:
            a=re.match(r'%([\d.]+)',c[10])
            if a: D.setdefault(k,{})[c[0]]=float(a.group(1))
    return D
for T in sys.argv[1:]:
    d=f'veri/agf_kayit/{T}'; P=json.load(open(f'veri/plan/{T}.json'))['kosular']
    for h in ('Antalya','İzmir'):
        if not os.path.exists(f'{d}/ILK_{h}.csv'): continue
        I=csvagf(f'{d}/ILK_{h}.csv')
        C=[]
        for f in glob.glob(f'{d}/{h}_*UTC.csv'):
            hm=os.path.basename(f)[len(h)+1:len(h)+5]; m=((int(hm[:2])+3)%24)*60+int(hm[2:]); C.append((m,f))
        S=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://ebayi.org/s/d/sonuclar/{T.replace('-','')}/full/{EB[h]}.json",headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read())
        for k in S.get('kosular',[]):
            no=str(k['NO']); A=[a for a in k['atlar'] if str(a.get('SONUC') or '').isdigit()]
            if not A or no not in I: continue
            bas=int(P[h][no][:2])*60+int(P[h][no][3:]); son=[f for m,f in sorted(C) if m<bas]
            if not son: continue
            L=csvagf(son[-1]).get(no,{}); w=next(a for a in A if a['SONUC']=='1')['NO']
            ch={n:L.get(n,0)-I[no].get(n,0) for n in I[no]}
            sira=sorted(ch,key=lambda n:-ch[n]).index(w)+1
            fav0=max(I[no],key=I[no].get); fav1=max(L,key=L.get) if L else '?'
            print(f"{T} {h[:3]} {no}: kazanan {w:>2} AGF %{I[no].get(w,0):4.1f}→%{L.get(w,0):4.1f} ({ch[w]:+5.1f}) artışta {sira:>2}./{len(ch)} | en çok artan {max(ch,key=ch.get)} ({max(ch.values()):+.1f}) | sabah fav {fav0} son fav {fav1} | gny {next(a for a in A if a['SONUC']=='1')['GANYAN']}")
