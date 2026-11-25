"""yenibeygir Blt ile resmi (eBayi) AGF karşılaştırması. Kullanım: blt_agf_karsilastir.py <YYYY-AA-GG> <hipodrom> [agf_dosyası]
Girdi: veri/yenibeygir_el_kayit/blt_<tarih>.csv (en son zaman_tr satırı alınır) ve veri/agf_kayit/<tarih>/TAM_<hip>_ebayi.json (yoksa verilen dosya; yoksa en son <hip>_*UTC_ebayi.json).
Çıktı: ekrana ve veri/yenibeygir_el_kayit/blt_agf_<tarih>_<hip>.md. Ölçütler (koşu başına): ortalama mutlak fark (puan), Spearman sırası, en yüksek Blt = en yüksek AGF mi, Blt toplamı.
Not: yenibeygir tamsayı verir; AGF1/AGF2 varsa (iki altılı) ortalaması değil AGF1 ve AGF2'ye en yakın olan alınır."""
import sys,os,re,csv,json,glob
import numpy as np
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tarih,hip=sys.argv[1:3]
ak=lambda s:re.sub(r'\W','',str(s).upper())
f=lambda v:(float(str(v).replace(',','.')) if v not in (None,'') else None)
B={}
fn=os.path.join(K,'veri','yenibeygir_el_kayit',f'blt_{tarih}.csv')
R=[r for r in csv.DictReader(open(fn,encoding='utf-8')) if r['hipodrom']==hip]
son=max(r['zaman_tr'] for r in R)
for r in R:
    if r['zaman_tr']==son and r['blt'].strip().isdigit(): B.setdefault(r['kosu'],{})[ak(r['at_adi'])]=int(r['blt'])
if len(sys.argv)>3: yol=sys.argv[3]
else:
    yol=os.path.join(K,'veri','agf_kayit',tarih,f'TAM_{hip}_ebayi.json')
    if not os.path.exists(yol): yol=sorted(glob.glob(os.path.join(K,'veri','agf_kayit',tarih,f'{hip}_????UTC_ebayi.json')))[-1]
E=json.load(open(yol,encoding='utf-8'))
def sp(a,b):
    ra=np.argsort(np.argsort(a));rb=np.argsort(np.argsort(b)); return float(np.corrcoef(ra,rb)[0,1]) if len(a)>2 else float('nan')
L=[f'# Blt ve resmi AGF — {tarih} {hip}','',f'Blt kaydı zamanı {son} (TR). AGF kaynağı: {os.path.relpath(yol,K)}.','','| Koşu | At | Blt toplamı | AGF toplamı | Ort. mutlak fark | Spearman | En yüksek aynı mı |','|---|---|---|---|---|---|---|']
T=[]
for no in sorted(B,key=int):
    E_=E.get(no) or {}; ea={ak(a):v for a,v in E_.items() if not v[3]}
    ad=[a for a in B[no] if a in ea]
    if len(ad)<3: L.append(f'| {no} | — | eşleşme yok | | | | |'); continue
    b=np.array([B[no][a] for a in ad],float)
    a1=np.array([f(ea[a][0]) or 0 for a in ad]); a2=np.array([f(ea[a][1]) or 0 for a in ad])
    a=a2 if (a2.sum()>0 and np.abs(b-a2).mean()<np.abs(b-a1).mean()) else a1
    mae=float(np.abs(b-a).mean()); s=sp(b,a); ayni=ad[int(np.argmax(b))]==ad[int(np.argmax(a))]
    T.append((mae,s,ayni)); L.append(f'| {no} | {len(ad)} | {b.sum():.0f} | {a.sum():.0f} | {mae:.1f} | {s:+.2f} | {"evet" if ayni else "hayır"} |')
if T: L+=['',f'Özet: {len(T)} koşu, ort. mutlak fark {np.mean([t[0] for t in T]):.1f} puan, ort. Spearman {np.nanmean([t[1] for t in T]):+.2f}, en yüksek aynı: {sum(t[2] for t in T)}/{len(T)}.','','Yorum: fark ~1–2 puansa Blt = AGF (yuvarlama); belirgin büyükse ayrı bir sinyal. Küçük örnek.']
open(os.path.join(K,'veri','yenibeygir_el_kayit',f'blt_agf_{tarih}_{hip}.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n'); print('\n'.join(L))
