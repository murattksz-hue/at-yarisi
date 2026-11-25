"""Jokey tablosu (sonuçlardan, gerçek sayılar). Kullanım: jokey_tablo.py sonuc_dizini cikti.json
Her jokey: 180 gün biniş/galibiyet, son 30 gün, hipodrom bazında, favori (en düşük ganyan birimi) ile kazanma oranı, piyasa A/E."""
import sys,glob,os,re,json,collections,datetime
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
fs=sorted(glob.glob(sys.argv[1]+'/*.csv')); son=max(os.path.basename(f)[:10] for f in fs); s30=(datetime.date.fromisoformat(son)-datetime.timedelta(days=30)).isoformat()
J=collections.defaultdict(lambda:dict(b=0,w=0,b30=0,w30=0,fb=0,fw=0,q=0.0,wq=0,hip=collections.defaultdict(lambda:[0,0])))
for f in fs:
    b=os.path.basename(f); g=b[:10]; hip=b[11:-4]; cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): cur=dict(h=[],ek=[]); rs.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except Exception:o=0
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,o=o,jok=c[6].replace(' AP','').strip()))
    for r in rs:
        h=r['h']
        if len(h)<4: continue
        grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
        for x in h: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
        ok=all(x['o']>1 for x in h); tot=sum(1/L[0]['o'] for L in U.values()) if ok else 1
        fav=min(U.values(),key=lambda L:L[0]['o'])[0]['o'] if ok else None
        for L in U.values():
            for x in L:
                j=J[x['jok']]; w=x['pos']==1; j['b']+=1; j['w']+=w; j['hip'][hip][0]+=1; j['hip'][hip][1]+=w
                if g>=s30: j['b30']+=1; j['w30']+=w
                if ok:
                    j['q']+=(1/x['o'])/tot/len(L); j['wq']+=w
                    if x['o']==fav: j['fb']+=1; j['fw']+=w
out={k:dict(binis=v['b'],galibiyet=v['w'],yuzde=round(100*v['w']/v['b'],1),son30_binis=v['b30'],son30_galibiyet=v['w30'],
            favori_binis=v['fb'],favori_galibiyet=v['fw'],piyasa_ae=round(v['wq']/v['q'],2) if v['q'] else None,
            hipodrom={h:dict(binis=a,galibiyet=b_) for h,(a,b_) in v['hip'].items()}) for k,v in J.items() if v['b']>=10}
json.dump(dict(son_tarih=son,jokey=out),open(sys.argv[2],'w'),ensure_ascii=False)
print(len(out),'jokey; son tarih',son)
