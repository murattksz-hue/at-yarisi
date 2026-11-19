"""AGF ve ganyan: her koşu için 4 nokta — 1) sabah ilk, 2) öğle (12:30'a en yakın), 3) koşudan 30 dk önce, 4) koşudan 5 dk önce (son). Eski ad: zaman çizelgesi (gerçek kayıtlar: veri/agf_kayit/<tarih>/). Kullanım: takip_rapor.py GG.AA.YYYY Hipodrom [koşu_no]
Her koşu için en çok oynanan 5 at: her kayıttaki AGF ve ganyan (İstanbul saati), bitiş (TJK canlı sayfası) ve kesin ganyan (TJK sonuç dosyası, varsa)."""
import sys,os,re,glob,json,datetime,subprocess,urllib.parse
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date(); hip=sys.argv[2]; sec=sys.argv[3] if len(sys.argv)>3 else None
kd=os.path.join(K,'veri','agf_kayit',g.isoformat())
def tr(s): h,m=int(s[:2]),int(s[2:]); return f"{(h+3)%24:02d}:{m:02d}"
C=sorted(glob.glob(os.path.join(kd,f"{hip}_*UTC.csv"))); G=sorted(glob.glob(os.path.join(kd,f"{hip}_*UTC_ganyan.json")))
BAS={}
def oku(f):
    R={};no=None
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            no=c[0].split('.')[0]; R[no]={}; m=re.search(r'(\d{1,2})\.(\d{2})',c[0].split(':',1)[1] if ':' in c[0] else '')
            if m: BAS[no]=int(m.group(1))*60+int(m.group(2))
            continue
        if no and re.match(r'^\d+$',c[0]) and len(c)>10:
            m=re.match(r'%([\d.]+)',c[10]); R[no][ad_(c[1])]=dict(no=c[0],agf=float(m.group(1)) if m else None)
    return R
SN=[(os.path.basename(f)[len(hip)+1:len(hip)+5],oku(f)) for f in C]
GN={os.path.basename(f)[len(hip)+1:len(hip)+5]:json.load(open(f,encoding='utf-8')) for f in G}
# kesin sonuç: resmi sonuç dosyası (gün bitince) ya da canlı sayfa
son={}; sf=os.path.join(K,'veri','sonuc',f"{g.isoformat()}_{hip}.csv")
u=f"https://medya-cdn.tjk.org/raporftp/TJKPDF/{g.year}/{g.isoformat()}/CSV/GunlukYarisSonuclari/{g.strftime('%d.%m.%Y')}-{urllib.parse.quote(hip)}-GunlukYarisSonuclari-TR.csv"
b=open(sf,'rb').read() if os.path.exists(sf) else subprocess.run(['curl','-sS','-f','--max-time','60',u],capture_output=True).stdout
no=None
for l in b.decode('utf-8-sig','replace').splitlines():
    c=l.split(';')
    if re.match(r'^\d+\. Kosu',c[0]): no=c[0].split('.')[0]; continue
    if no and c[0].isdigit() and len(c)>13: son.setdefault(no,{})[ad_(c[1])]=(int(c[0]) if c[12].strip() else 99,c[13])
if not SN: sys.exit('kayıt yok')
dk=lambda s_:((int(s_[:2])+3)%24)*60+int(s_[2:])   # UTC SSDD -> İstanbul dakikası
def nokta(liste,k,hedef_fn):
    # liste: [(saat, değer-sözlüğü)] ; hedef_fn: saat dakikası -> uygun mu
    uy=[(s_,v) for s_,v in liste if hedef_fn(dk(s_))]
    return uy[-1] if uy else (None,None)
for k in SN[-1][1]:
    if sec and k!=sec: continue
    bas=BAS.get(k); son_agf=SN[-1][1][k]; top=sorted(son_agf,key=lambda a:-(son_agf[a]['agf'] or 0))[:5]
    dolu=[(s_,R) for s_,R in SN if any((R.get(k,{}).get(a) or {}).get('agf') for a in R.get(k,{}))]
    ilk=dolu[0] if dolu else (None,None)
    ogle=min(dolu,key=lambda x:abs(dk(x[0])-750)) if dolu else (None,None)
    n30=nokta(dolu,k,lambda m:bas is not None and m<=bas-25) ; n5=nokta(dolu,k,lambda m:bas is not None and m<=bas-2)
    GL=sorted(GN.items())
    g_ilk=GL[0] if GL else (None,{}); g_og=min(GL,key=lambda x:abs(dk(x[0])-750)) if GL else (None,{})
    g30=nokta(GL,k,lambda m:bas is not None and m<=bas-25); g5=nokta(GL,k,lambda m:bas is not None and m<=bas-2)
    t_=lambda x:tr(x) if x else '—'
    print(f"\n=== {hip} {k}. koşu (başlangıç {bas//60:02d}:{bas%60:02d}) ===" if bas else f"\n=== {hip} {k}. koşu ===")
    print(f"  {'at':22} {'AGF: sabah '+t_(ilk[0]):>17} {'öğle '+t_(ogle[0]):>11} {'-30dk '+t_(n30[0]):>12} {'-5dk '+t_(n5[0]):>11} | {'ganyan: sabah':>13} {'öğle':>6} {'-30dk':>6} {'-5dk':>6} | kesin ganyan, sonuç")
    for a in top:
        fa=lambda sn:(f"%{sn[1][k][a]['agf']:.0f}" if sn[1] and sn[1].get(k,{}).get(a,{}).get('agf') else '—')
        fg=lambda sn:(f"{sn[1][a]:.2f}" if sn[1] and sn[1].get(a,0)>1 else '—')
        sn_=son.get(k,{}).get(a); bt=f"{sn_[1] or '—'}, {str(sn_[0])+'.' if sn_[0]<99 else 'derecesiz'}" if sn_ else '—'
        print(f"  #{son_agf[a]['no']:>2} {a[:18]:18} {fa(ilk):>17} {fa(ogle):>11} {fa(n30):>12} {fa(n5):>11} | {fg(g_ilk):>13} {fg(g_og):>6} {fg(g30):>6} {fg(g5):>6} | {bt}")
