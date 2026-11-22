"""TJK ve ebayi AGF'sinden hangisi doğru? Günler geçtikçe birikir.
Kullanım: agf_dogruluk.py [YYYY-AA-GG]   (tarih verilmezse bütün günler yeniden hesaplanır; bir şeyi silmez)
Ölçüt: AGF günün sonunda kesinleşir (iki kaynak birebir aynı olur). Her görüntüde her kaynağın değerinin kesin değerden
ne kadar uzak olduğuna bakılır: ortalama mutlak fark (puan) ve "favori kesin favoriyle aynı mı". Kesine yakın olan kaynak daha doğru/güncel.
Girdi : veri/agf_kayit/<tarih>/<Hip>_<SSDD>UTC.csv (TJK; yalnızca değişince saklanır, aradaki görüntüler öncekiyle aynı sayılır)
        veri/agf_kayit/<tarih>/<Hip>_<SSDD>UTC_ebayi.json (ebayi)
Çıktı : veri/agf_kayit/dogruluk.csv  (gün, saat dilimi, hipodrom, n, mae_tjk, mae_ebayi, favori_tjk, favori_ebayi)
        veri/agf_kayit/DOGRULUK.md  (günlük ve toplam özet)
Kesin değer: o günün her kaynaktaki son görüntüsü; iki kaynağın son görüntüsü birbirinden >0,02 ayrılıyorsa o hipodrom o gün sayılmaz."""
import sys,os,re,json,glob,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R=os.path.join(K,'veri','agf_kayit')

def tjk(path):   # {(kosu,altili,at): agf}
    D={};k=None
    for l in open(path,encoding='utf-8-sig',errors='replace'):
        m=re.match(r'^(\d+)\. Kosu',l)
        if m: k=m.group(1);continue
        p=l.rstrip('\n').split(';')
        if k and re.match(r'^\d+$',p[0]) and len(p)>10 and 'Koşmaz' not in p[1]:
            for j,x in enumerate(re.findall(r'%([\d.]+)\(',p[10])): D[(k,j,p[1].strip())]=float(x)
    return D
def eb(path):
    D={}
    for k,A in json.load(open(path,encoding='utf-8')).items():
        for ad,v in A.items():
            if v[3]: continue
            for j,x in enumerate([float(a) for a in v[:2] if a not in (None,'')]): D[(k,j,ad)]=x
    return D
def esle(D,E):   # TJK adı ekler taşır ("DOĞANHAN KG DB"), ebayi taşımaz: ebayi sözlüğünü TJK anahtarlarına çevir
    out={}
    names=collections.defaultdict(list)
    for (k,j,n) in E: names[(k,j)].append(n)
    for (k,j,ad) in D:
        u=[n for n in names[(k,j)] if ad==n or ad.startswith(n+' ')]
        if u: out[(k,j,ad)]=E[(k,j,max(u,key=len))]
    return out
def favs(D):
    g=collections.defaultdict(dict)
    for (k,j,ad),x in D.items(): g[(k,j)][ad]=x
    return {kj:max(a,key=a.get) for kj,a in g.items()}

def gun(d):
    dd=os.path.join(R,d); sat=[]
    for f in glob.glob(dd+'/*_*UTC_ebayi.json'):
        h,t=os.path.basename(f).split('_')[:2]; t=t[:4]   # '1902UTC' -> '1902'
        if h!='ILK': sat.append((h,t))
    out=[]
    for h in sorted({h for h,_ in sat}):
        ts=sorted(t for hh,t in sat if hh==h)
        tj={t:os.path.join(dd,f"{h}_{t}UTC.csv") for t in ts if os.path.exists(os.path.join(dd,f"{h}_{t}UTC.csv"))}
        tjall=sorted(glob.glob(dd+f"/{h}_????UTC.csv"))
        if not tjall: continue
        sonT=tjk(tjall[-1]); sonE=esle(sonT,eb(os.path.join(dd,f"{h}_{ts[-1]}UTC_ebayi.json")))
        ortak=[x for x in sonT if x in sonE]
        if not ortak or max(abs(sonT[x]-sonE[x]) for x in ortak)>0.02: out.append(('atla',h)); continue
        kesin={x:sonT[x] for x in ortak}; kf=favs(kesin); last=None
        for t in ts:
            if t in tj: last=tjk(tj[t])     # TJK: değişmediyse öncekini taşı
            if last is None: continue
            E=esle(last,eb(os.path.join(dd,f"{h}_{t}UTC_ebayi.json")))
            T={x:last[x] for x in kesin if x in last}; E={x:E[x] for x in kesin if x in E}
            ft,fe=favs(T),favs(E)
            hr=(int(t[:2])+3)%24
            for x in kesin:
                if x in T and x in E:
                    out.append((hr,h,abs(T[x]-kesin[x]),abs(E[x]-kesin[x])))
            for kj in kf:
                if kj in ft and kj in fe: out.append(('fav',hr,h,ft[kj]==kf[kj],fe[kj]==kf[kj]))
    return out

gunler=[sys.argv[1]] if len(sys.argv)>1 else sorted(x for x in os.listdir(R) if re.match(r'\d{4}-\d\d-\d\d$',x))
CSV=os.path.join(R,'dogruluk.csv'); eski={}
if os.path.exists(CSV):
    for l in open(CSV,encoding='utf-8').read().splitlines()[1:]:
        p=l.split(',')
        if len(p)==8: eski[(p[0],p[1],p[2])]=p
for d in gunler:
    A=collections.defaultdict(lambda:[0,0.0,0.0,0,0,0]); atlanan=set()
    for o in gun(d):
        if o[0]=='atla': atlanan.add(o[1]); continue
        if o[0]=='fav': a=A[(o[1],o[2])]; a[3]+=o[3]; a[4]+=o[4]; a[5]+=1; continue
        a=A[(o[0],o[1])]; a[0]+=1; a[1]+=o[2]; a[2]+=o[3]
    for (hr,h),a in A.items():
        if a[0]: eski[(d,f"{hr:02d}",h)]=[d,f"{hr:02d}",h,str(a[0]),f"{a[1]/a[0]:.4f}",f"{a[2]/a[0]:.4f}",f"{a[3]}/{a[5]}",f"{a[4]}/{a[5]}"]
    if atlanan: print(d,'sayılmayan hipodrom (son görüntüler uyuşmuyor):',', '.join(sorted(atlanan)))
rows=sorted(eski.values())
open(CSV,'w',encoding='utf-8').write("gun,saat,hipodrom,n,mae_tjk,mae_ebayi,favori_tjk,favori_ebayi\n"+"\n".join(','.join(r) for r in rows)+"\n")

# özet
def topla(rs):
    n=sum(int(r[3]) for r in rs)
    if not n: return None
    t=sum(float(r[4])*int(r[3]) for r in rs)/n; e=sum(float(r[5])*int(r[3]) for r in rs)/n
    ft=sum(int(r[6].split('/')[0]) for r in rs); fe=sum(int(r[7].split('/')[0]) for r in rs); fn=sum(int(r[6].split('/')[1]) for r in rs)
    return n,t,e,ft,fe,fn
def kim(t,e): return 'TJK' if t<e-0.005 else 'ebayi' if e<t-0.005 else 'eşit'
L=["# TJK mi ebayi mi? AGF doğruluk özeti","",
   "Ölçüt: günün sonunda kesinleşen AGF'ye ortalama uzaklık (puan, küçük = iyi). Her satır, o saat diliminde alınan görüntülerin ortalaması.","",
   "## Toplam (bütün günler)","","| Saat | Değer | TJK fark | ebayi fark | Daha yakın | Favori doğru TJK | Favori doğru ebayi |","|---|---|---|---|---|---|---|"]
for hr in sorted({r[1] for r in rows}):
    s=topla([r for r in rows if r[1]==hr])
    if s: L.append(f"| {hr}:xx | {s[0]} | {s[1]:.3f} | {s[2]:.3f} | {kim(s[1],s[2])} | {s[3]}/{s[5]} | {s[4]}/{s[5]} |")
s=topla(rows)
if s: L+=["",f"**Genel:** TJK ortalama {s[1]:.3f} puan, ebayi {s[2]:.3f} puan uzak → daha yakın: **{kim(s[1],s[2])}** ({len({r[0] for r in rows})} gün, {s[0]} değer).","",
          "## Günlük","","| Gün | Değer | TJK fark | ebayi fark | Daha yakın |","|---|---|---|---|---|"]
for d in sorted({r[0] for r in rows}):
    s=topla([r for r in rows if r[0]==d]); L.append(f"| {d} | {s[0]} | {s[1]:.3f} | {s[2]:.3f} | {kim(s[1],s[2])} |")
L+=["","Not: saat dilimi İstanbul saatidir. Akşam iki kaynak birebir aynı olduğu için fark orada sıfıra yaklaşır; asıl bilgi sabah ve öğleden sonraki satırlardadır."]
open(os.path.join(R,'DOGRULUK.md'),'w',encoding='utf-8').write("\n".join(L)+"\n")
print("tamam:",len(rows),"satır")
