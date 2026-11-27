"""Hipodrom sicili: koşacak atların bu hipodromda daha önce kaç kez koştuğu, kaç galibiyet ve ilk 3. Kullanım: hipodrom_sicil.py [YYYY-AA-GG] -> veri/hipodrom_sicil/<tarih>.md
Girdi: veri/tahminler/<tarih>_<Hipodrom>.json (koşacak atlar, temiz adlar) + veri/at_gecmisi (2020+). At eşleşmesi AD ile (aynı adlı farklı at nadir, not edilir).
Yalnızca okur; yazar veri/hipodrom_sicil/<tarih>.md. Piyasa ötesi bilgi iddiası yok: bkz hipodrom_galibi_testi.py (galibiyet oranı >=%30 ve >=3 start: A/E 1,08)."""
import os,sys,glob,gzip,csv,io,json,datetime,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUN=sys.argv[1] if len(sys.argv)>1 else datetime.date.today().isoformat()
dosyalar=sorted(glob.glob(os.path.join(K,'veri','tahminler',f'{GUN}_*.json')))
dosyalar=[d for d in dosyalar if not d.endswith('_agfsiz.json')]
adlar=set(); hiplar={}
for fn in dosyalar:
    hip=os.path.basename(fn)[len(GUN)+1:-5]
    J=json.load(open(fn,encoding='utf-8')); hiplar[hip]=J
    for r in J:
        for a in r['atlar']: adlar.add(a['ad'].strip())
H=collections.defaultdict(list)   # ad -> [(tarih,hip,mesafe,pist,sonuc,kosan)]
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')):
        ad=r['at'].strip()
        if ad in adlar and r['tarih']<GUN:
            s=r['sonuc'].strip()
            H[ad].append((r['tarih'],r['hip'],r['mesafe'],(r['pist'] or '').strip(),int(s) if s.isdigit() else None,r['kosan']))
JS={}
L=[f'# Hipodrom sicili — {GUN}','','Her atın bu hipodromdaki geçmişi (start / galibiyet / ilk 3). Kaynak at_gecmisi 2020+, ad eşleşmesi. Aynı adlı farklı at olabilir. Yorum değil kayıt.','']
for hip,J in hiplar.items():
    L+=[f'## {hip}','']
    for r in J:
        baslik=r.get('baslik','').split('Kosu :')[-1].strip()[:90]
        L+=[f"### {r['kosu']}. koşu — {baslik}",'','| At | Bu hip. start | Galibiyet | İlk 3 | Oran | Son bu hipodromda | Bu hipodromda en iyi mesafe |','|---|---|---|---|---|---|---|']
        for a in r['atlar']:
            ad=a['ad'].strip(); h=[x for x in H.get(ad,[]) if x[1]==hip]; h.sort()
            n=len(h); w=sum(1 for x in h if x[4]==1); t=sum(1 for x in h if x[4] and x[4]<=3)
            JS.setdefault(hip,{})[ad]=[sum(1 for x in h if x[4]),w,t]   # start (sonuçlu), galibiyet, ilk 3
            son=f"{h[-1][0]} {h[-1][2]} m {h[-1][4]}." if h else '-'
            iyi=''
            if h:
                m=collections.Counter(x[2] for x in h if x[4] and x[4]<=3)
                iyi=', '.join(f'{k} m ({v}x ilk3)' for k,v in m.most_common(2))
            L.append(f"| {ad} | {n} | {w} | {t} | {('%'+str(round(100*w/n))) if n else '-'} | {son} | {iyi or '-'} |")
        L.append('')
os.makedirs(os.path.join(K,'veri','hipodrom_sicil'),exist_ok=True)
json.dump(JS,open(os.path.join(K,'veri','hipodrom_sicil',f'{GUN}.json'),'w',encoding='utf-8'),ensure_ascii=False)
open(os.path.join(K,'veri','hipodrom_sicil',f'{GUN}.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('yazıldı veri/hipodrom_sicil/%s.md | %d hipodrom, %d at'%(GUN,len(hiplar),len(adlar)))
