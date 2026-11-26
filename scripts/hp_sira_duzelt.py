"""Tek seferlik düzeltme (26.11.2026): HP sırası eşitlik hatası. veri/kazanan_profil.csv 'hp_sira' ve veri/para_takip.csv 'sinyal' (HP ilk 3 koşulu) sütunlarını doğru hesapla yeniden yazar.
Kullanım: hp_sira_duzelt.py  (HP kaynağı: veri/at_gecmisi, o gün yoksa ebayi sonuç JSON'u; eşitlikte sıra yok: sıra = 1 + HP'si kesin daha büyük at sayısı).
para_takip sinyal kuralı değişmedi: son ganyan>=10, AGF payı >= 1,3 × ganyan olasılığı (koşu içi 1/ganyan toplamına normalize), HP ilk 3. Yalnızca sinyal sütunu dolu olan satırlar yeniden hesaplanır."""
import os,sys,csv,gzip,io,json,glob,subprocess,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EB={'İzmir':'IZMIR','İstanbul':'ISTANBUL','Şanlıurfa':'SANLIURFA','Elazığ':'ELAZIG','Diyarbakır':'DIYARBAKIR','Adana':'ADANA','Bursa':'BURSA','Ankara':'ANKARA','Kocaeli':'KOCAELI','Antalya':'ANTALYA'}
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
HPC={}   # (tarih,hip,kosu) -> {at: hp}
def hp_yukle(t,hip):
    if (t,hip) in HPC: return
    HPC[(t,hip)]=True
    fn=os.path.join(K,'veri','at_gecmisi',t[:4],f'{t}.csv.gz'); got=False
    if os.path.exists(fn):
        for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')):
            if r['hip']==hip: HPC.setdefault((t,hip,r['kosu']),{})[r['at']]=f(r['hp']) or 0; got=True
    if not got:
        try: J=json.loads(subprocess.run(['curl','-sS','--max-time','40','-A','Mozilla/5.0',f"https://ebayi.org/s/d/sonuclar/{t.replace('-','')}/full/{EB[hip]}.json"],capture_output=True,text=True).stdout)
        except Exception: return
        for k in J.get('kosular',[]):
            HPC[(t,hip,str(k['NO']))]={a['AD']:f(a.get('HANDIKAP')) or 0 for a in k['atlar'] if not a.get('KOSMAZ')}
def sira(d,at):
    return 1+sum(1 for b in d if d[b]>d[at]) if at in d else None
# --- kazanan_profil.csv ---
p=os.path.join(K,'veri','kazanan_profil.csv'); R=list(csv.DictReader(open(p,encoding='utf-8'))); fn_=list(R[0]); d1=0; once=0; sonra=0
for r in R:
    hp_yukle(r['tarih'],r['hip']); d=HPC.get((r['tarih'],r['hip'],r['kosu']))
    if not d: continue
    n=sira(d,r['at'])
    if n is None: continue
    if str(n)!=str(r['hp_sira']): d1+=1
    once+=(str(r['hp_sira'])=='1'); sonra+=(n==1); r['hp_sira']=n
with open(p,'w',encoding='utf-8',newline='') as fh: w=csv.DictWriter(fh,fieldnames=fn_); w.writeheader(); w.writerows(R)
print(f'kazanan_profil: {len(R)} kazanan, hp_sira değişen {d1}; HP sırası 1 olanlar {once} → {sonra}')
# --- para_takip.csv ---
p=os.path.join(K,'veri','para_takip.csv'); P=list(csv.DictReader(open(p,encoding='utf-8'))); fn_=list(P[0])
gr=collections.defaultdict(list)
for r in P: gr[(r['tarih'],r['hip'],r['kosu'])].append(r)
ch=0; s_once=0; s_sonra=0
for (t,h,k),rs in gr.items():
    hp_yukle(t,h); d=HPC.get((t,h,k)) or {}
    gs={r['at']:f(r['g_son']) for r in rs if f(r['g_son'])}; tq=sum(1/g for g in gs.values()) if gs else 0
    for r in rs:
        if r.get('sinyal') in (None,''): continue
        g=gs.get(r['at']); a=f(r['agf_son']); s=int(bool(g and tq and a and g>=10 and (a/100)>=1.3*(1/g)/tq and (sira(d,r['at']) or 99)<=3))
        s_once+=int(r['sinyal']); s_sonra+=s
        if str(s)!=str(r['sinyal']): ch+=1
        r['sinyal']=s
with open(p,'w',encoding='utf-8',newline='') as fh: w=csv.DictWriter(fh,fieldnames=fn_); w.writeheader(); w.writerows(P)
print(f'para_takip: sinyal değişen satır {ch}; sinyal=1 toplamı {s_once} → {s_sonra}')
