"""−10 dk tahminlerinin puanlaması (tutturma yüzdesi). Kullanım: puan_10dk.py [tarih ...]   (tarih verilmezse veri/tahminler_10dk altındaki bütün günler; gün sonu agf_plan.py çağırır)
Sonuç: ebayi.org sonuç JSON'u (koşmaz at sayılmaz). Yalnızca eBayi görüntüsü koşuya <=20 dk kala alınmış tahminler 'geçerli' sayılır (bayat görüntü dışarıda, ayrıca sayılır).
Ölçütler (her kol: BİRLEŞİK_10, piyasa_10, v9 AGF'li, v9 AGF'siz): 1. seçim kazandı (%), kazanan ilk 2'de (%), kazanan ilk 3'te (%), kazananın ort. log-olasılığı; Wilson %95 aralığı; n>=100'de BİRLEŞİK_10 − piyasa_10 eşli bootstrap farkı.
Çıktı: veri/tahminler_10dk/SONUC.md"""
import os,sys,json,re,math,glob,random,subprocess,datetime
import numpy as np
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EB={'İzmir':'IZMIR','İstanbul':'ISTANBUL','Şanlıurfa':'SANLIURFA','Elazığ':'ELAZIG','Diyarbakır':'DIYARBAKIR','Adana':'ADANA','Bursa':'BURSA','Ankara':'ANKARA','Kocaeli':'KOCAELI','Antalya':'ANTALYA'}
ak=lambda s:re.sub(r'\W','',str(s).upper())
od=os.path.join(K,'veri','tahminler_10dk')
gunler=sys.argv[1:] or sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(od,'????-??-??.json')))
ARMS=[('birlesik10','p_birlesik10',"BİRLEŞİK_10"),('piyasa10','p_piyasa10','piyasa_10'),('v9_agfli','p_v9_agfli',"v9 AGF'li (sabah)"),('v9_agfsiz','p_v9_agfsiz',"v9 AGF'siz (sabah)")]
def wilson(k,n,z=1.96):
    if n==0: return (0,0)
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return (c-h,c+h)
S=[]; bayat=0; sonucsuz=0; cache={}
for gun in gunler:
    D=json.load(open(os.path.join(od,f'{gun}.json'),encoding='utf-8'))
    for k,v in D['kosular'].items():
        hip=v['hip']; key=(gun,hip)
        if key not in cache:
            try: cache[key]=json.loads(subprocess.run(['curl','-sS','--max-time','60','-A','Mozilla/5.0',f"https://ebayi.org/s/d/sonuclar/{gun.replace('-','')}/full/{EB.get(hip,hip.upper())}.json"],capture_output=True).stdout.decode('utf-8'))
            except Exception: cache[key]={}
        sk={str(x['NO']):{ak(a['AD']):int(a['SONUC']) for a in x.get('atlar',[]) if not a.get('KOSMAZ') and str(a.get('SONUC') or '').isdigit()} for x in cache[key].get('kosular',[])}
        r=sk.get(str(v['kosu']))
        if not r or sorted(r.values()).count(1)!=1: sonucsuz+=1; continue
        if not (0<=v['goruntu_koşuya_dk']<=20): bayat+=1; continue
        win=[a for a in v['atlar'] if r.get(ak(a['ad']))==1]
        if len(win)!=1: continue
        row=dict(gun=gun,hip=hip,kosu=v['kosu'],kazanan=win[0]['ad'],guven=v['guven'],tip=v.get('tip') or {},risk=v.get('surpriz_riski'),KL=v.get('liste_uzunlugu'),listede=(win[0]['ad'] in (v.get('secim_liste') or [])) if v.get('secim_liste') else None)
        for n,pk,_ in ARMS:
            ps=[a[pk] for a in v['atlar']]
            if any(p is None for p in ps): row[n]=None; continue
            sira=sorted(v['atlar'],key=lambda a:-a[pk]); w=win[0][pk]
            rk=1+sum(1 for a in v['atlar'] if a[pk]>w)
            row[n]=(rk,math.log(max(w,1e-4)))
        S.append(row)
L=[f'# −10 dk tahmin puanlaması','',f'Günler: {", ".join(gunler) or "—"}. Puanlanan (geçerli) koşu: **{len(S)}**; sonucu henüz yok: {sonucsuz}; bayat görüntü (koşuya >20 dk): {bayat}.','',
   '| Kol | Koşu | 1. seçim kazandı | %95 aralık | Kazanan ilk 2\'de | İlk 3\'te | Kazananın ort. log-olasılığı |','|---|---|---|---|---|---|---|']
for n,_,ad in ARMS:
    R=[r[n] for r in S if r[n] is not None]; m=len(R)
    if not m: L.append(f'| {ad} | 0 | — | | | | |'); continue
    t1=sum(x[0]==1 for x in R); t2=sum(x[0]<=2 for x in R); t3=sum(x[0]<=3 for x in R); lo,hi=wilson(t1,m)
    L.append(f"| {ad} | {m} | {t1} (%{100*t1/m:.1f}) | %{100*lo:.0f}–{100*hi:.0f} | %{100*t2/m:.1f} | %{100*t3/m:.1f} | {np.mean([x[1] for x in R]):.3f} |")
LS=[r for r in S if r['listede'] is not None]
if LS:
    L+=['','**Sürpriz riskine göre değişken liste (yüksek risk 5, orta 4, düşük 3 at):** kazanan listede %{:.0f} ({}/{} koşu).'.format(100*sum(r['listede'] for r in LS)/len(LS),sum(r['listede'] for r in LS),len(LS)),'','| Risk | Liste | Koşu | Kazanan listede | İlk 3\'te |','|---|---|---|---|---|']
    for rk in ('yüksek','orta','düşük'):
        q=[r for r in LS if r['risk']==rk]
        if q: L.append(f"| {rk} | {q[0]['KL']} at | {len(q)} | %{100*sum(r['listede'] for r in q)/len(q):.0f} | %{100*sum(r['birlesik10'][0]<=3 for r in q if r['birlesik10'])/len(q):.0f} |")
    L.append('Geçmiş beklenti (17.873 koşu, kapanış piyasası): düşük risk K3 %77, orta K4 %81, yüksek K5 %76 (yüksek riskte yalnızca 3 at olsaydı %60).')
E=[(r['birlesik10'],r['piyasa10']) for r in S if r['birlesik10'] and r['piyasa10']]
if len(E)>=100:
    d=[(a[1]-b[1]) for a,b in E]; rr=random.Random(1); bs=sorted(np.mean([d[rr.randrange(len(d))] for _ in d]) for _ in range(1000))
    L+=['',f'BİRLEŞİK_10 − piyasa_10 (kazananın log-olasılığı, eşli bootstrap, {len(E)} koşu): {np.mean(d):+.4f} [{bs[25]:+.4f}, {bs[974]:+.4f}]']
else: L+=['',f'BİRLEŞİK_10 − piyasa_10 aralığı için en az 100 koşu gerekir (şimdi {len(E)}).']
for gv in ('net','orta','düşük'):
    sel=[r for r in S if r['guven']==gv and r['birlesik10']]
    if sel: L.append(f"- Güven '{gv}': {len(sel)} koşu, 1. seçim tuttu %{100*sum(r['birlesik10'][0]==1 for r in sel)/len(sel):.0f}")
L+=['','Rastgele beklenti ≈ 1/ortalama at sayısı (≈%10); piyasa favorisi tarihsel olarak ~%33–35 kazanır.']
import csv as _csv
with open(os.path.join(od,'kosu_sonuclari.csv'),'w',newline='',encoding='utf-8') as _f:   # koşu başına kol sıraları (koşu çeşidi raporu için; her çalıştırmada yeniden üretilir)
    _w=_csv.writer(_f); _w.writerow(['tarih','hip','kosu','irk','tur','aile','mesafe','pist','guven','birlesik10_sira','piyasa10_sira','v9_agfli_sira','v9_agfsiz_sira'])
    for r in S: _w.writerow([r['gun'],r['hip'],r['kosu'],r['tip'].get('irk',''),r['tip'].get('tur',''),r['tip'].get('aile',''),r['tip'].get('mesafe',''),r['tip'].get('pist',''),r['guven']]+[(r[n][0] if r[n] else '') for n in ('birlesik10','piyasa10','v9_agfli','v9_agfsiz')])
open(os.path.join(od,'SONUC.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n'); print('\n'.join(L))
