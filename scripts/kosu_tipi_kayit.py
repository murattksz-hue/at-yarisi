"""Koşu çeşidi kaydı (türetilmiş, her çalıştırmada yeniden üretilir). Kullanım: kosu_tipi_kayit.py   (gün sonu agf_plan.py çağırır)
Kaynak: veri/kazanan_profil.csv (her biten koşu: kazanan, ganyan, sürpriz, v9 AGF'li/AGF'siz modelin kazanana verdiği sıra, piyasa sırası, çeşit/mesafe/pist/ırk) + veri/tahminler_10dk/kosu_sonuclari.csv (−10 dk kol sıraları, varsa).
Çıktı: veri/kosu_tipi_kayit.csv: koşu başına satır: tarih, hip, kosu, irk, tur, aile, mesafe, mesafe_band, pist, kosan, kazanan, kesin (ganyan), surpriz, fav_kazandi, v9_agfli_ilk, v9_agfsiz_ilk, agf_fav_kazandi, b10_ilk, piyasa10_ilk.
Mantık: 'ilk' = modelin ilk seçimi kazanan mı (kazanan sırası 1)."""
import os,sys,csv
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(K,'scripts')); import kosu_tipi as T
def oku(p): return list(csv.DictReader(open(os.path.join(K,p),encoding='utf-8'))) if os.path.exists(os.path.join(K,p)) else []
KP=oku('veri/kazanan_profil.csv'); B10={(r['tarih'],r['hip'],r['kosu']):r for r in oku('veri/tahminler_10dk/kosu_sonuclari.csv')}
f=lambda v:(float(v.replace(',','.')) if v not in ('',None) else None)
ilk=lambda v:('' if f(v) is None else int(f(v)==1))
out=[]
for r in KP:
    t=T.tur(r['tur']); b=B10.get((r['tarih'],r['hip'],r['kosu']),{})
    out.append(dict(tarih=r['tarih'],hip=r['hip'],kosu=r['kosu'],irk=r['irk'] or ('Arap' if 'Arap' in r['tur'] else ''),tur=t,aile=T.aile(t),mesafe=r['mesafe'],mesafe_band=T.mesafe_band(r['mesafe']),pist=r['pist'],kosan=r['kosan'],
        kazanan=r['at'],kesin=r['kesin'],surpriz=r['surpriz'],fav_kazandi=ilk(r['ganyan_sira']),v9_agfli_ilk=ilk(r['model_agfli_sira']),v9_agfsiz_ilk=ilk(r['model_agfsiz_sira']),agf_fav_kazandi=ilk(r['agf_son_sira']),
        b10_ilk=ilk(b.get('birlesik10_sira')) if b else '',piyasa10_ilk=ilk(b.get('piyasa10_sira')) if b else ''))
if out:
    with open(os.path.join(K,'veri','kosu_tipi_kayit.csv'),'w',newline='',encoding='utf-8') as fh:
        w=csv.DictWriter(fh,fieldnames=list(out[0])); w.writeheader(); w.writerows(sorted(out,key=lambda r:(r['tarih'],r['hip'],int(r['kosu']))))
print('koşu çeşidi kaydı:',len(out),'koşu')
