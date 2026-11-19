"""Beyer tipi hız puanı tablosu. Kullanım: hiz_tablosu.py sonuc_dizini cikti.json
Puan = -1000 × ((at süresi - par)/par - günün pist değişkeni). Par: o hipodrom+pist+mesafe+ırk için
ÖNCEKİ günlerin kazanan süre medyanı (en az 4 örnek). Değişken: o gün o pistte kazananların par'dan sapma medyanı.
Çıktı: at -> {sayi (koşu sayısı), galibiyetler [hipodrom,pist,mesafe], son 3 hız puanı}; sahip -> [galibiyet, alan beklentisi]."""
import sys,glob,os,re,json,collections,statistics
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
def sn(x):
    m=re.match(r'(\d+):(\d+)\.(\d+)',x.strip()); return int(m.group(1))*60+int(m.group(2))+int(m.group(3))/100 if m else None
R=[]
for f in sorted(glob.glob(sys.argv[1]+'/*.csv')):
    b=os.path.basename(f); cur=None
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            m=re.search(r'(\d{3,4})m',l); cur=dict(g=b[:10],hip=b[11:-4],irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),m=int(m.group(1)) if m else 0,h=[]); R.append(cur); continue
        if cur is not None and c[0].isdigit() and len(c)>13:
            cur['h'].append(dict(ad=ad_(c[1]),pos=int(c[0]) if c[12].strip() else 99,t=sn(c[12]),sah=c[7].strip()))
PAR=collections.defaultdict(list); HIS=collections.defaultdict(list); SH=collections.defaultdict(lambda:[0,0.0])
for g in sorted(set(r['g'] for r in R)):
    gun=[r for r in R if r['g']==g and r['m'] and len(r['h'])>=4]; var=collections.defaultdict(list)
    par=lambda r:statistics.median(PAR[(r['hip'],r['pist'],r['m'],r['irk'])]) if len(PAR[(r['hip'],r['pist'],r['m'],r['irk'])])>=4 else None
    for r in gun:
        p=par(r); w=[x for x in r['h'] if x['pos']==1 and x['t']]
        if p and w: var[(r['hip'],r['pist'])].append((w[0]['t']-p)/p)
    for r in gun:
        p=par(r); v=statistics.median(var[(r['hip'],r['pist'])]) if var[(r['hip'],r['pist'])] else 0
        n=len(r['h'])
        for x in r['h']:
            HIS[f"{r['irk']}|{x['ad']}"].append(dict(tarih=g,puan=round(-1000*((x['t']-p)/p-v),1) if (p and x['t'] and x['pos']<99) else None,hipodrom=r['hip'],pist=r['pist'],mesafe=r['m'],derece=x['pos']))
            SH[x['sah']][0]+=x['pos']==1; SH[x['sah']][1]+=1/n
        w=[x for x in r['h'] if x['pos']==1 and x['t']]
        if w: PAR[(r['hip'],r['pist'],r['m'],r['irk'])].append(w[0]['t'])
json.dump(dict(at={k:dict(sayi=len(v),galibiyetler=[dict(hipodrom=y['hipodrom'],pist=y['pist'],mesafe=y['mesafe']) for y in v if y['derece']==1],son=[y for y in v if y['puan'] is not None][-3:]) for k,v in HIS.items()},
           sahip={k:[v[0],round(v[1],3)] for k,v in SH.items()}),open(sys.argv[2],'w'),ensure_ascii=False)
print(len(HIS),'at; son tarih',max(r['g'] for r in R))
