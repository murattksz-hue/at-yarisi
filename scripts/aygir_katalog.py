"""SİAYSD 2026 aygır kataloğu PDF'lerinden tablo. Kullanım: aygir_katalog.py pdf_dizini cikti.json
Her aygır: ad, don, doğum yılı, haraya giriş, kendi yarış kariyeri (koşu/1./2./3.), babası, tay istatistikleri (yıllara göre ve toplam: koşan, kazanan, koşu, galibiyet)."""
import sys,os,re,glob,json,subprocess
OUT={}
for f in sorted(glob.glob(sys.argv[1]+'/*.pdf')):
    t=subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True).stdout.decode('utf-8','replace')
    if not t.strip(): continue
    L=t.splitlines(); ad=L[0].strip()
    d=dict(dosya=os.path.basename(f))
    m=re.search(r'DON:\s*(\S+).*?D\.Y\.:\s*(\d{4}).*?HARA G[İI]R[İI]Ş:\s*([A-Z]{2,3})?\s*(\d{4})',t,flags=re.S)
    if m: d.update(don=m.group(1),dogum=int(m.group(2)),hara_ulke=m.group(3),hara_giris=int(m.group(4)))
    m=re.search(r'Toplam\s+(\d+)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)',t)
    if m: d['kariyer']=dict(kosu=int(m.group(1)),birinci=0 if m.group(2)=='-' else int(m.group(2)),ikinci=0 if m.group(3)=='-' else int(m.group(3)),ucuncu=0 if m.group(4)=='-' else int(m.group(4)))
    m=re.search(r'\((?:e|a),\s*([^)]+?)\)\s*Söz konusu Aygır',t)
    if m: d['baba']=m.group(1).strip()
    yil={}
    for y,a,b,c_,e in re.findall(r'\s(20[0-2]\d)\s{2,}(\d+)\s{2,}(\d+)\s{2,}(\d+)\s{2,}(\d+)\s*$',t,flags=re.M):
        yil[y]=dict(kosan=int(a),kazanan=int(b),kosu=int(c_),galibiyet=int(e))
    if yil: d['yillar']=yil
    # katalogun kendi tay toplamı: 'Toplam' satırlarındaki SON dört sayı, koşu sayısı en büyük olan (aygırın kendi kariyer satırı küçük)
    adaylar=[tuple(map(int,m.groups())) for m in re.finditer(r'Toplam\s{2,}(\d+)\s{2,}(\d+)\s{2,}(\d+)\s{2,}(\d+)\s*$',t,flags=re.M)]
    if adaylar:
        a=max(adaylar,key=lambda x:x[2]); d['katalog_toplam']=dict(kosan=a[0],kazanan=a[1],kosu=a[2],galibiyet=a[3])
    if yil:
        d['tay_toplam']=dict(kosu=sum(v['kosu'] for v in yil.values()),galibiyet=sum(v['galibiyet'] for v in yil.values()),yil_sayisi=len(yil))
        k_=d.get('katalog_toplam')
        d['uyusmazlik']=bool(k_ and (abs(k_['kosu']-d['tay_toplam']['kosu'])>0.02*max(k_['kosu'],1) or k_['galibiyet']>k_['kosu']))
    gr=re.findall(r'\((G[123])\)',t); d['taylarin_grup_galibiyet_sayisi']={k:gr.count(k) for k in ('G1','G2','G3')}
    OUT[ad]=d
json.dump(OUT,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
tam=[k for k,v in OUT.items() if 'tay_toplam' in v]
print(len(OUT),'aygır;',len(tam),'aygırın yıllık tay verisi okundu;',sum(v.get('uyusmazlik',False) for v in OUT.values()),'uyuşmazlık;',sum('baba' in v for v in OUT.values()),'aygırın babası okundu')
for k in sorted(tam,key=lambda k:-OUT[k]['tay_toplam']['galibiyet'])[:15]:
    v=OUT[k]; T_=v['tay_toplam']; K_=v.get('katalog_toplam',{})
    print(f"  {k:26} doğum {v.get('dogum','?')} baba {v.get('baba','?')[:18]:18} {T_['yil_sayisi']} yıl, {T_['kosu']:5} koşu, {T_['galibiyet']:4} galibiyet (%{100*T_['galibiyet']/max(T_['kosu'],1):.1f})"+(f" | katalog: {K_.get('kosan')} tay koşan, {K_.get('kazanan')} kazanan" if K_ else '')+(' ⚠uyuşmazlık' if v.get('uyusmazlik') else ''))
