"""Her koşudaki her at için, YALNIZCA o günden önceki sonuçlardan geçmiş özellikleri (ham) üretir.
Kullanım: gecmis_ozellik.py sonuc_dizini galop_dizini cikti.json
Anahtar: 'YYYY-AA-GG_Hipodrom|koşuNo|at adı' -> [hiz_en_iyi3, hiz_son, pist_mesafe_galibi, pist_galibi, deneyim, sahip_logAE,
                                               galop_400, galop_yok, galop_son7, galop_sayi30, galop_zorlanarak, galop_veri_var, baba_yas, anne_kardes, kardes_yok, sahip_piyasa, galibiyet6]"""
import sys,glob,os,re,json,collections,statistics,math,datetime
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
def sn(x):
    m=re.match(r'(\d+):(\d+)\.(\d+)',x.strip()); return int(m.group(1))*60+int(m.group(2))+int(m.group(3))/100 if m else None
SD,GD,OUT=sys.argv[1:4]; R=[]
for f in sorted(glob.glob(SD+'/*.csv')):
    b=os.path.basename(f)[:-4]; cur=None
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            m=re.search(r'(\d{3,4})m',l); cur=dict(b=b,g=b[:10],hip=b[11:],no=c[0].split('.')[0].strip(),irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),m=int(m.group(1)) if m else 0,h=[],ek=[]); R.append(cur); continue
        if cur is not None and 'eküridir' in l: cur['ek'].append([ad_(a) for a in re.findall(r'\(\d+\)([^,\]]+)',l)])
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except:o=0
            y=c[2].split()
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,t=sn(c[12]),sah=c[7].strip(),o=o,baba=c[3].strip(),anne=c[4].strip(),genc=bool(y) and y[-1] in ('e','d')))
BY=collections.defaultdict(lambda:[0,0.0]); AK=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0.0])); SP=collections.defaultdict(lambda:[0,0.0])
PAR=collections.defaultdict(list); HIS=collections.defaultdict(list); SH=collections.defaultdict(lambda:[0,0.0]); OUTD={}; GAL={}
for g in sorted(set(r['g'] for r in R)):
    gun=[r for r in R if r['g']==g]; gd=datetime.date.fromisoformat(g)
    for r in gun:   # 1) özellikler (geçmişten)
        gf=os.path.join(GD,r['b']+'.json')
        if r['b'] not in GAL: GAL[r['b']]=json.load(open(gf,encoding='utf-8')) if os.path.exists(gf) else None
        G=GAL[r['b']]
        for x in r['h']:
            H=HIS[(r['irk'],x['ad'])]; sp=[y['fig'] for y in H if y['fig'] is not None][-3:]; ws=[y for y in H if y['pos']==1]
            sh=SH[x['sah']]; v=[max(sp) if sp else None, sp[-1] if sp else None,
               float(any(y['hip']==r['hip'] and y['pist']==r['pist'] and abs(y['m']-r['m'])<=100 for y in ws)), float(any(y['pist']==r['pist'] for y in ws)),
               math.log(1+len(H)), math.log((sh[0]+3)/(sh[1]+3))]
            if G is not None:
                L=[i for i in G.get(x['ad'],{}).get('idmanlar',[]) if datetime.datetime.strptime(i['tarih'],'%d.%m.%Y').date()<gd]
                d30=[i for i in L if (gd-datetime.datetime.strptime(i['tarih'],'%d.%m.%Y').date()).days<=30]; t4=[i['split'].get('400') for i in d30 if i['split'].get('400')]
                gn=(gd-datetime.datetime.strptime(L[0]['tarih'],'%d.%m.%Y').date()).days if L else None
                v+=[min(t4) if t4 else None, float(not t4), float(gn is not None and gn<=7), min(len(d30),5)/5, float(bool(L) and L[0].get('efor')=='Çalışarak'), 1.0]
            else: v+=[None,0.0,0.0,0.0,0.0,0.0]
            by=BY[(r['irk'],x['baba'],x['genc'])]; kd=[q for k,q in AK[(r['irk'],x['anne'])].items() if k!=x['ad']]; kw=sum(q[0] for q in kd); ke=sum(q[1] for q in kd); sp=SP[x['sah']]
            v+=[math.log((by[0]+5)/(by[1]+5)), math.log((kw+2)/(ke+2)), float(not kd), math.log((sp[0]+10)/(sp[1]+10)), float(sum(y['pos']==1 for y in H[-6:]))]
            OUTD[f"{r['b']}|{r['no']}|{x['ad']}"]=v
    var=collections.defaultdict(list)   # 2) günü geçmişe ekle
    par=lambda r:statistics.median(PAR[(r['hip'],r['pist'],r['m'],r['irk'])]) if len(PAR[(r['hip'],r['pist'],r['m'],r['irk'])])>=4 else None
    for r in gun:
        p=par(r); w=[x for x in r['h'] if x['pos']==1 and x['t']]
        if p and w: var[(r['hip'],r['pist'])].append((w[0]['t']-p)/p)
    for r in gun:
        p=par(r); vv=statistics.median(var[(r['hip'],r['pist'])]) if var[(r['hip'],r['pist'])] else 0; n=len(r['h'])
        ok=all(x['o']>1 for x in r['h']) and n>=4
        if ok:
            grp={a:i for i,E in enumerate(r['ek']) for a in E}; U={}
            for x in r['h']: U.setdefault(grp.get(x['ad'],'t'+x['ad']),[]).append(x)
            tot=sum(1/L[0]['o'] for L in U.values())
            for L in U.values():
                for x in L: SP[x['sah']][0]+=x['pos']==1; SP[x['sah']][1]+=(1/x['o'])/tot/len(L)
        for x in r['h']:
            if n>=4:
                BY[(r['irk'],x['baba'],x['genc'])][0]+=x['pos']==1; BY[(r['irk'],x['baba'],x['genc'])][1]+=1/n
                a_=AK[(r['irk'],x['anne'])][x['ad']]; a_[0]+=x['pos']==1; a_[1]+=1/n
            HIS[(r['irk'],x['ad'])].append(dict(fig=-1000*((x['t']-p)/p-vv) if (p and x['t'] and x['pos']<99) else None,pos=x['pos'],hip=r['hip'],pist=r['pist'],m=r['m']))
            if n>=4: SH[x['sah']][0]+=x['pos']==1; SH[x['sah']][1]+=1/n
        w=[x for x in r['h'] if x['pos']==1 and x['t']]
        if w and r['m'] and len(r['h'])>=4: PAR[(r['hip'],r['pist'],r['m'],r['irk'])].append(w[0]['t'])
json.dump(OUTD,open(OUT,'w'),ensure_ascii=False); print(len(OUTD),'at-koşu kaydı; galoplu:',sum(1 for v in OUTD.values() if v[-1]))
