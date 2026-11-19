"""Canlı test, ilk 2 isabeti: dondurulmuş tahminlerin (veri/tahminler/) ilk 2 atı gerçek 1-2 ile karşılaştırılır.
Kullanım: ikili_takip.py GG.AA.YYYY Hipodrom [Hipodrom...]
Sonuç kaynağı: ebayi sonuç JSON'u. Koşmayan at çıkarılır, sıralama koşanlar arasında yapılır. Eküri birleştirilmez (at bazında).
İKİLİ = ilk 2 seçim, ilk 2 gelen at (sırası önemsiz). SIRALI = 1. seçim 1., 2. seçim 2. AGF ilk 2'si de aynı şekilde."""
import sys,os,json,datetime,subprocess
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EB={'İzmir':'IZMIR','İstanbul':'ISTANBUL','Şanlıurfa':'SANLIURFA','Elazığ':'ELAZIG','Diyarbakır':'DIYARBAKIR','Adana':'ADANA','Bursa':'BURSA','Ankara':'ANKARA','Kocaeli':'KOCAELI','Antalya':'ANTALYA'}
g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date(); TOP={}
for hip in sys.argv[2:]:
    J=json.loads(subprocess.run(['curl','-sS','--max-time','60','-A','Mozilla/5.0',f"https://ebayi.org/s/d/sonuclar/{g:%Y%m%d}/full/{EB[hip]}.json"],capture_output=True).stdout.decode('utf-8') or '{}')
    S={str(k['NO']):{a['AD'].strip():int(a['SONUC']) for a in k.get('atlar',[]) if not a.get('KOSMAZ') and str(a.get('SONUC') or '').isdigit()} for k in J.get('kosular',[])}
    for sr in ('v6','v8','agfsiz'):
        f=os.path.join(K,'veri','tahminler',f"{g.isoformat()}_{hip}{'' if sr=='v6' else '_'+sr}.json")
        if not os.path.exists(f): continue
        for k in json.load(open(f,encoding='utf-8')):
            b=S.get(str(k['kosu']))
            if not b or 1 not in b.values(): continue
            A=[a for a in k['atlar'] if a['ad'] in b]
            ilk2={a for a,v in b.items() if v<=2}; bir=next(a for a,v in b.items() if v==1); iki=next((a for a,v in b.items() if v==2),None)
            for ad,anahtar in ((sr,'p'),('AGF','agf')):
                if ad=='AGF' and (sr!='v8' or k.get('agf_yok')): continue
                t=[a['ad'] for a in sorted(A,key=lambda a:-a[anahtar])[:2]]
                T=TOP.setdefault(ad,[0,0,0,[]]); T[0]+=1; T[1]+=set(t)==ilk2; T[2]+=(t[0]==bir and t[1]==iki)
                T[3].append(f"{hip[:3]}{k['kosu']}: {t[0]}/{t[1]} → {'SIRALI ✅' if t[0]==bir and t[1]==iki else 'İKİLİ ✅' if set(t)==ilk2 else '—'}")
print(f"=== İlk 2 isabeti {g} ({', '.join(sys.argv[2:])}) ===")
for ad in ('v6','v8','agfsiz','AGF'):
    if ad in TOP:
        n,i,s,L=TOP[ad]; print(f"{ad:7} {n} koşu | ikili tuttu {i} (%{100*i/n:.0f}) | sıralı ikili tuttu {s} (%{100*s/n:.0f})")
        for x in L:
            if '✅' in x: print('        ',x)
