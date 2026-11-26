"""Mesafe profili testi: atın kendi ve babasının BUGÜNKÜ mesafe bandındaki geçmişi, piyasanın ötesinde bilgi taşıyor mu? Kullanım: mesafe_profil_testi.py (yalnızca ekrana yazar; veri/at_gecmisi tüm yıllar, kronolojik, sızıntısız)
Özellikler (yalnızca koşudan ÖNCEKİ geçmişten): own = atın bu bantta büzülmüş ilk-3 oranı − genel ilk-3 oranı (n_genel>=4; büzülme a=3); baba = babanın yavrularının bu bantta büzülmüş log(A/E) (n>=30, kapanış ganyanından normalize piyasa p'sine göre; büzülme 5). Koşu içinde standartlaştırılır.
Yöntem: koşullu logit u = log p_piyasa + b*özellik; b ilk %60'ta (zaman) öğrenilir, son %40'ta koşu başına log-olabilirlik kazancı + eşli bootstrap %95 aralığı. Ek: 'uyumlu at' (bantta >=4 koşu, ilk-3 oranı >=%50 ve genel orandan >=15 puan iyi) ve 'uyumsuz at' (bantta >=4 koşu, hiç ilk-3 yok) gruplarının A/E'si, iki yarıda.
Bantlar: <=1200, 1300-1400, 1500-1700, 1800-2100, 2200+. Test koşuları 2024-07'den sonrası; geçmiş özellikleri tüm yıllardan (2021-06→2024-01 arası veri boşluğu nedeniyle bir miktar gürültü olabilir)."""
import os,glob,gzip,csv,io,collections,math,random
import numpy as np
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
def band(m):
    try: m=int(m)
    except Exception: return None
    return 0 if m<=1200 else 1 if m<=1400 else 2 if m<=1700 else 3 if m<=2100 else 4
R=collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')): R[(r['tarih'],r['hip'],r['kosu'])].append(r)
SA=collections.defaultdict(lambda:[0,0,0.0]); DA=collections.defaultdict(lambda:[0,0,0.0]); HA=collections.defaultdict(lambda:[0,0]); HB=collections.defaultdict(lambda:[0,0]); SB=collections.defaultdict(lambda:[0,0,0.0])
races=[]; HROWS=[]   # grup: n,beklenen,gerçek, ... (ilk/ikinci yarı ayrı)
def z(x):
    x=np.array(x,float); s=x.std(); return (x-x.mean())/s if s>1e-9 else x*0
for key in sorted(R):
    rs=R[key]; g=[f(r['ganyan']) for r in rs]; b=band(rs[0]['mesafe'])
    ok=b is not None and not(any(v is None or v<=1 for v in g)) and len(rs)>=5 and sum(1 for r in rs if r['sonuc'].strip()=='1')==1
    if ok and key[0]>='2024-07-01':
        inv=np.array([1/v for v in g]); p=inv/inv.sum(); w=[r['sonuc'].strip()=='1' for r in rs].index(True)
        own=[];bab=[];grp=[];abb=[];ann=[]
        for r in rs:
            hk=r['kod'] or r['at']; na,ta=HA[hk]
            if na>=4:
                nb,tb=HB[(hk,b)]; ra=ta/na; rb=(tb+3*ra)/(nb+3); own.append(rb-ra)
                grp.append('uyumlu' if (nb>=4 and tb/nb>=0.5 and tb/nb-ra>=0.15) else 'uyumsuz' if (nb>=4 and tb==0) else None)
            else: own.append(0.0); grp.append(None)
            s=(r['baba'] or '').upper().strip(); n_s,w_s,e_s=SB[(s,b)] if s else (0,0,0.0)
            bab.append(math.log((w_s+5)/(e_s+5)) if n_s>=30 else 0.0)
            ab=(r['annebaba'] or '').upper().strip(); n_a,w_a,e_a=SA[(ab,b)] if ab else (0,0,0.0)
            abb.append(math.log((w_a+5)/(e_a+5)) if n_a>=30 else 0.0)
            an=(r['anne'] or '').upper().strip(); n_d,w_d,e_d=DA[(an,b)] if an else (0,0,0.0)
            ann.append(math.log((w_d+3)/(e_d+3)) if n_d>=8 else 0.0)
        races.append(dict(t=key[0],L=np.log(p),w=w,F={'kendi':z(own),'baba':z(bab),'ikisi':z(own)+z(bab)},grp=grp,p=p))
        for i,r in enumerate(rs): HROWS.append((key[0],float(p[i]),i==w,own[i],bab[i],grp[i],g[i],abb[i],ann[i]))
    # geçmişi güncelle (bu koşu bitti)
    if b is not None:
        if ok: iv=[1/v for v in g]; sv=sum(iv)
        for i,r in enumerate(rs):
            if not r['sonuc'].strip().isdigit(): continue
            pos=int(r['sonuc']); hk=r['kod'] or r['at']
            HA[hk][0]+=1; HA[hk][1]+=pos<=3; HB[(hk,b)][0]+=1; HB[(hk,b)][1]+=pos<=3
            s=(r['baba'] or '').upper().strip()
            if s and ok: t=SB[(s,b)]; t[0]+=1; t[1]+=pos==1; t[2]+=iv[i]/sv
            ab=(r['annebaba'] or '').upper().strip(); an=(r['anne'] or '').upper().strip()
            if ab and ok: t=SA[(ab,b)]; t[0]+=1; t[1]+=pos==1; t[2]+=iv[i]/sv
            if an and ok: t=DA[(an,b)]; t[0]+=1; t[1]+=pos==1; t[2]+=iv[i]/sv
print('test koşu sayısı',len(races))
dates=sorted({r['t'] for r in races}); cut=dates[int(len(dates)*0.6)]
tr=[r for r in races if r['t']<cut]; te=[r for r in races if r['t']>=cut]
def ll(rs,bs,names):
    out=[]
    for r in rs:
        u=r['L'].copy()
        for bb,nm in zip(bs,names): u=u+bb*r['F'][nm]
        m=u.max(); out.append(u[r['w']]-(m+math.log(np.exp(u-m).sum())))
    return np.array(out)
def fit(names):
    best=np.zeros(len(names))
    for _ in range(3):
        for i in range(len(names)):
            cand=np.linspace(-1,1.5,26); sc=[]
            for c in cand:
                b2=best.copy(); b2[i]=c; sc.append(ll(tr,b2,names).sum())
            best[i]=cand[int(np.argmax(sc))]
    return best
rr=random.Random(1)
print(f"eğitim {len(tr)} koşu (<{cut}), test {len(te)} koşu")
for nm in (['kendi'],['baba'],['kendi','baba'],['ikisi']):
    b=fit(nm); g=ll(te,b,nm)-ll(te,np.zeros(len(nm)),nm)
    bs=sorted(np.mean([g[rr.randrange(len(g))] for _ in range(len(g))]) for _ in range(600))
    isr='ANLAMLI +' if bs[15]>0 else ('ANLAMLI -' if bs[584]<0 else 'anlamsız')
    print(f"{'+'.join(nm):12s} b={np.round(b,2)} kazanç/koşu {g.mean():+.5f} %95 [{bs[15]:+.5f},{bs[584]:+.5f}] {isr}")
print('\nGrup A/E (beklenen = kapanış piyasası; ilk yarı | ikinci yarı):')
orta=dates[len(dates)//2]
for gr in ('uyumlu','uyumsuz'):
    out=[]
    for ad,sel in (('ilk',lambda r:r['t']<orta),('ikinci',lambda r:r['t']>=orta)):
        n=0;e=0.0;o=0;v=0.0
        for r in races:
            if not sel(r): continue
            for i,gg in enumerate(r['grp']):
                if gg==gr: n+=1; e+=r['p'][i]; o+=(i==r['w']); v+=r['p'][i]*(1-r['p'][i])
        out.append(f"{ad} yarı n={n} gerçek {o} beklenen {e:.1f} A/E {o/e if e else 0:.2f} z {(o-e)/math.sqrt(v) if v else 0:+.1f}")
    print(f"  {gr:8s} "+' | '.join(out))

# --- SÜRPRİZ ODAKLI: yalnızca uzun atlar (piyasa olasılığı <%10), ham özellik (standartlaştırılmamış) ---
print('\nUZUN ATLAR (piyasa p<%10): özellik gruplarına göre A/E (beklenen = kapanış piyasası), ilk yarı | ikinci yarı')
def blok(ad,sel):  # sel(ow,ba,gr,ab,an)
    out=[]
    for yn,y in (('ilk',lambda t:t<orta),('ikinci',lambda t:t>=orta)):
        n=0;e=0.0;o=0;v=0.0
        for t,p,w,ow,ba,gr,gn,ab,an in HROWS:
            if p<0.10 and y(t) and sel(ow,ba,gr,ab,an): n+=1;e+=p;o+=w;v+=p*(1-p)
        out.append(f"{yn} n={n:5d} gerçek {o:3d} beklenen {e:6.1f} A/E {o/e if e else 0:.2f} z {(o-e)/math.sqrt(v) if v else 0:+.1f}")
    print(f"  {ad:34s} "+' | '.join(out))
blok('tüm uzun atlar',lambda ow,ba,gr,ab,an:True)
blok('mesafeye uyumlu at',lambda ow,ba,gr,ab,an:gr=='uyumlu')
blok('mesafeye uyumsuz at',lambda ow,ba,gr,ab,an:gr=='uyumsuz')
blok('kendi bant farkı >= +0,15',lambda ow,ba,gr,ab,an:ow>=0.15)
blok('kendi bant farkı <= -0,15',lambda ow,ba,gr,ab,an:ow<=-0.15)
blok('baba bant log(A/E) >= +0,10',lambda ow,ba,gr,ab,an:ba>=0.10)
blok('baba bant log(A/E) <= -0,10',lambda ow,ba,gr,ab,an:ba<=-0.10)
blok('uyumlu at + baba olumlu',lambda ow,ba,gr,ab,an:gr=='uyumlu' and ba>=0.05)
blok('ganyan>=20 ve uyumlu',lambda ow,ba,gr,ab,an:gr=='uyumlu')

print('\nANNE TARAFI (uzun atlar, piyasa p<%10): anne babası ve anne için bant log(A/E)')
blok('anne babası olumlu (>=+0,10)',lambda ow,ba,gr,ab,an:ab>=0.10)
blok('anne babası olumsuz (<=-0,10)',lambda ow,ba,gr,ab,an:ab<=-0.10)
blok('anne (dam) olumlu (>=+0,10; n>=8)',lambda ow,ba,gr,ab,an:an>=0.10)
blok('anne (dam) olumsuz (<=-0,10; n>=8)',lambda ow,ba,gr,ab,an:an<=-0.10)
blok('baba VE anne babası olumlu (>=+0,05)',lambda ow,ba,gr,ab,an:ba>=0.05 and ab>=0.05)
blok('baba VE anne babası olumsuz (<=-0,05)',lambda ow,ba,gr,ab,an:ba<=-0.05 and ab<=-0.05)
blok('uyumlu at + baba + anne babası olumlu',lambda ow,ba,gr,ab,an:gr=='uyumlu' and ba>=0.05 and ab>=0.05)
