"""Geçmiş günler için TAM AGF'yi eski görüntülerden geriye dönük türetir (yalnızca EKLER, mevcut dosyalara yazmaz).
Kullanım: tam_geriye_donuk.py <YYYY-AA-GG> [...]
Her hipodrom için günün en erken TJK görüntüsü <hip>_<HHMM>UTC.csv ve eBayi görüntüsü <hip>_<HHMM>UTC_ebayi.json arasından agf_tam kuralıyla (altılıdaki her koşuda atların >=%90'ı dolu) ilk TAM olanı bulur.
Çıktı: veri/agf_kayit/<tarih>/retro_TAM_<hip>.csv (o görüntünün kopyası; 'TAM_' ile BAŞLAMAZ, canlı dondurma mantığıyla karışmasın) ve veri/agf_kayit/<tarih>/retro_TAM.json (saatler, ILK doluluğu, TAM doluluğu)."""
import sys,os,glob,json,shutil
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(K,'scripts')); import agf_tam as T
def doluluk(b,yar):
    D=T._agf_tjk(b); ks=[k for k in D if (not yar or k in yar)]
    n=sum(len(D[k]) for k in ks); d=sum(1 for k in ks for v in D[k] if v>0)
    return round(d/n,3) if n else None
for g in sys.argv[1:]:
    kd=os.path.join(K,'veri','agf_kayit',g); R={}
    hips=sorted({os.path.basename(f)[4:-4] for f in glob.glob(os.path.join(kd,'ILK_*.csv')) if not f.endswith('_ebayi.json')})
    for h in hips:
        if h.endswith('_ebayi'): continue
        yar=T.altili_yarislar(open(os.path.join(kd,f'ILK_{h}.csv'),'rb').read())
        out={'ilk_doluluk':doluluk(open(os.path.join(kd,f'ILK_{h}.csv'),'rb').read(),yar)}
        for yol in sorted(glob.glob(os.path.join(kd,f'{h}_[0-9][0-9][0-9][0-9]UTC.csv'))):
            b=open(yol,'rb').read()
            if T.tam_tjk(b,T.altili_yarislar(b) or yar):
                saat=os.path.basename(yol)[len(h)+1:len(h)+5]; out['tjk_tam']=saat+' UTC'; out['tam_doluluk']=doluluk(b,yar)
                shutil.copyfile(yol,os.path.join(kd,f'retro_TAM_{h}.csv')); break
        for yol in sorted(glob.glob(os.path.join(kd,f'{h}_[0-9][0-9][0-9][0-9]UTC_ebayi.json'))):
            try: S=json.load(open(yol,encoding='utf-8'))
            except Exception: continue
            if T.tam_ebayi(S,yar): out['ebayi_tam']=os.path.basename(yol)[len(h)+1:len(h)+5]+' UTC'; break
        iz=json.load(open(os.path.join(kd,'ilk_zaman.json'),encoding='utf-8')).get(h,{}) if os.path.exists(os.path.join(kd,'ilk_zaman.json')) else {}
        out['ilk_yayin']={k:v for k,v in iz.items() if k in ('tjk','ebayi')}
        R[h]=out
    json.dump(R,open(os.path.join(kd,'retro_TAM.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    print(g,json.dumps(R,ensure_ascii=False))
