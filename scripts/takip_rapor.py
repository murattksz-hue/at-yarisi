"""AGF ve ganyan zaman çizelgesi (gerçek kayıtlar: veri/agf_kayit/<tarih>/). Kullanım: takip_rapor.py GG.AA.YYYY Hipodrom [koşu_no]
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
def oku(f):
    R={};no=None
    for l in open(f,encoding='utf-8-sig'):
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): no=c[0].split('.')[0]; R[no]={}; continue
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
for k in SN[-1][1]:
    if sec and k!=sec: continue
    son_agf=SN[-1][1][k]; top=sorted(son_agf,key=lambda a:-(son_agf[a]['agf'] or 0))[:5]
    saatler=[s for s,_ in SN if any((R.get(k,{}).get(a) or {}).get('agf') for a in top for R in [_])]
    print(f"\n=== {hip} {k}. koşu ===   kayıt saatleri: "+' '.join(tr(s) for s in saatler))
    for a in top:
        agf=' → '.join(f"%{R[k][a]['agf']:.0f}" if R.get(k,{}).get(a,{}).get('agf') else '-' for s,R in SN if s in saatler)
        gy=' → '.join(f"{GN[s][a]:.2f}" for s in sorted(GN) if a in GN[s] and GN[s][a]>1)
        sn=son.get(k,{}).get(a); bt=f" | SONUÇ: {sn[0] if sn[0]<99 else 'derecesiz'}. (kesin ganyan {sn[1]})" if sn else ''
        print(f"  #{son_agf[a]['no']:>2} {a[:18]:18} AGF {agf} | ganyan {gy or '-'}{bt}")
