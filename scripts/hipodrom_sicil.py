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
def _fl(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
H=collections.defaultdict(list)   # ad -> [(tarih,hip,mesafe,pist,sonuc,kosan)]
for fn in sorted(glob.glob(os.path.join(K,'veri','at_gecmisi','*','*.csv.gz'))):
    for r in csv.DictReader(io.TextIOWrapper(gzip.open(fn),encoding='utf-8')):
        ad=r['at'].strip()
        if ad in adlar and r['tarih']<GUN:
            s=r['sonuc'].strip()
            H[ad].append((r['tarih'],r['hip'],r['mesafe'],(r['pist'] or '').strip(),int(s) if s.isdigit() else None,r['kosan'],(r['jokey'] or '').strip(),_fl(r['kilo']),_fl(r['hp'])))
# mesafe tipi (mesafe_tipi.py çıktısı; yoksa tip alanları boş kalır)
try:
    _TT=json.load(open(os.path.join(K,'veri','mesafe_profil','at_tipi.json'),encoding='utf-8'))
    _BT={r['baba']:r['tip'] for r in csv.DictReader(open(os.path.join(K,'veri','mesafe_profil','baba_tipi.csv'),encoding='utf-8'))}
    _AT={r['anne_babasi']:r['tip'] for r in csv.DictReader(open(os.path.join(K,'veri','mesafe_profil','annebaba_tipi.csv'),encoding='utf-8'))}
except Exception: _TT={}; _BT={}; _AT={}
JS={}; JM={}   # JM: hip -> ad -> {'bugun':[start,gal,ilk3] (bugünkü mesafe ±200 m, her hipodrom), 'uzun':[...] (>=1900 m), 'kisa':[...] (<=1500 m)}
import re
L=[f'# Hipodrom sicili — {GUN}','','Her atın bu hipodromdaki geçmişi (start / galibiyet / ilk 3). Kaynak at_gecmisi 2020+, ad eşleşmesi. Aynı adlı farklı at olabilir. Yorum değil kayıt.','']
for hip,J in hiplar.items():
    L+=[f'## {hip}','']
    for r in J:
        baslik=r.get('baslik','').split('Kosu :')[-1].strip()[:90]
        L+=[f"### {r['kosu']}. koşu — {baslik}",'','| At | Bu hip. start | Galibiyet | İlk 3 | Oran | Son bu hipodromda | Bu hipodromda en iyi mesafe | Bugünkü mesafe ±200 m (start/gal/ilk3) | Uzun ≥1900 m | Kısa ≤1500 m |','|---|---|---|---|---|---|---|---|---|---|']
        for a in r['atlar']:
            ad=a['ad'].strip(); h=[x for x in H.get(ad,[]) if x[1]==hip]; h.sort()
            _m=re.search(r'(\d{3,4})\s*m\b',r.get('baslik','')); _md=int(_m.group(1)) if _m else None; _all=H.get(ad,[])
            _st=lambda L:[sum(1 for x in L if x[4]),sum(1 for x in L if x[4]==1),sum(1 for x in L if x[4] and x[4]<=3)]
            _t=_TT.get(ad,{}); JM.setdefault(hip,{}).setdefault(ad,{}).update({'tip':_t.get('tip'),'baba':_t.get('baba'),'baba_tip':_BT.get(_t.get('baba')),'annebaba':_t.get('annebaba'),'annebaba_tip':_AT.get(_t.get('annebaba')),'mesafe':_md,'bugun':_st([x for x in _all if _md and abs(int(x[2] or 0)-_md)<=200]),'uzun':_st([x for x in _all if int(x[2] or 0)>=1900]),'kisa':_st([x for x in _all if int(x[2] or 0)<=1500])})
            n=len(h); w=sum(1 for x in h if x[4]==1); t=sum(1 for x in h if x[4] and x[4]<=3)
            JS.setdefault(hip,{})[ad]=[sum(1 for x in h if x[4]),w,t]   # start (sonuçlu), galibiyet, ilk 3
            son=f"{h[-1][0]} {h[-1][2]} m {h[-1][4]}." if h else '-'
            iyi=''
            if h:
                m=collections.Counter(x[2] for x in h if x[4] and x[4]<=3)
                iyi=', '.join(f'{k} m ({v}x ilk3)' for k,v in m.most_common(2))
            _j=JM[hip][ad]; _f=lambda v:'/'.join(map(str,v)) if v[0] else '-'
            L.append(f"| {ad} | {n} | {w} | {t} | {('%'+str(round(100*w/n))) if n else '-'} | {son} | {iyi or '-'} | {_f(_j['bugun'])} | {_f(_j['uzun'])} | {_f(_j['kisa'])} |")
        L.append('')
# ---- analiz listesi verisi (kullanıcı listesi 28.11): zemin sicili, zemin geçişi, kilo, mesafe değişimi, jokey, HP/grup dengesi
def _temiz(x): return re.sub(r'\s+',' ',x).strip()
def _prog(hip):
    fs=sorted(glob.glob(os.path.join(K,'veri','agf_kayit',GUN,f'{hip}_[0-9][0-9][0-9][0-9]UTC.csv')))
    fn=fs[-1] if fs else os.path.join(K,'veri','agf_kayit',GUN,f'TAM_{hip}.csv')
    out={}; race=None
    try: satir=open(fn,encoding='utf-8-sig').read().splitlines()
    except Exception: return out
    for l in satir:
        m=re.match(r'(\d+)\. Kosu\s*:\s*([\d.]+);(.*)',l)
        if m:
            race=m.group(1); pz=re.search(r';\s*(Kum|Çim|Sentetik)\s*;',l); ms=re.search(r'(\d{3,4})\s*m\b',l)
            out[race]={'zemin':pz.group(1) if pz else None,'mesafe':int(ms.group(1)) if ms else None,'atlar':{}}; continue
        c=l.split(';')
        if race and c[0].isdigit() and len(c)>11:
            kg=re.match(r'[\d,.]+',c[5]); hp=re.match(r'\d+',c[11])
            out[race]['atlar'][c[0]]={'jokey':_temiz(c[6]),'kilo':_fl(kg.group(0)) if kg else None,'hp':float(hp.group(0)) if hp else None,'st':c[9]}
    return out
def _jk_key(n):   # program 'M.UYAR AP' ile sonuç 'MERT UYAR' aynı jokey: soyad + ilk harf
    t=re.sub(r'\bAP\b','',n.upper().replace('.',' ')).split()
    return (t[-1],t[0][0]) if t else None
JA={}
for hip,J in hiplar.items():
    PR=_prog(hip)
    for r in J:
        P=PR.get(str(r['kosu']),{'zemin':None,'mesafe':None,'atlar':{}})
        _hpl=[v['hp'] for v in P['atlar'].values() if v['hp']]; _kll=[v['kilo'] for v in P['atlar'].values() if v['kilo']]
        _ort=sum(_hpl)/len(_hpl) if _hpl else None; _std=(sum((x-_ort)**2 for x in _hpl)/len(_hpl))**0.5 if _hpl else None
        grup={'hp_ort':round(_ort,1) if _ort else None,'hp_std':round(_std,1) if _std is not None else None,'hp_aralik':[min(_hpl),max(_hpl)] if _hpl else None,'kilo_aralik':[min(_kll),max(_kll)] if _kll else None,'zemin':P['zemin'],'mesafe':P['mesafe'],'at_sayisi':len(r['atlar'])}
        for a in r['atlar']:
            ad=a['ad'].strip(); pg=P['atlar'].get(str(a.get('no')),{}); _all=sorted(H.get(ad,[]))
            zs={z:[sum(1 for x in _all if x[3]==z and x[4]),sum(1 for x in _all if x[3]==z and x[4]==1),sum(1 for x in _all if x[3]==z and x[4] and x[4]<=3)] for z in ('Kum','Çim','Sentetik')}
            oran=lambda v:(v[2]/v[0]) if v[0]>=3 else None
            ok={z:oran(v) for z,v in zs.items() if oran(v) is not None}
            if len(ok)>=2 and sorted(ok.values())[-1]-sorted(ok.values())[-2]>=0.15: tercih=max(ok,key=ok.get)+' seven'
            elif len(ok)==1: tercih=(next(iter(ok))+' seven') if next(iter(ok.values()))>=0.5 else 'belirsiz'
            elif len(ok)>=2: tercih='karma'
            else: tercih='veri yetersiz'
            son=_all[-1] if _all else None; bz=P['zemin']
            if not son: gecis='ilk koşu (geçmiş yok)'
            elif zs.get(bz,[0])[0]==0 and bz: gecis=f"{son[3] or '?'}→{bz} (bu zeminde İLK KEZ)"
            elif son[3] and bz and son[3]!=bz: gecis=f"{son[3]}→{bz}"
            else: gecis='aynı zemin'
            md=P['mesafe']; sm=int(son[2] or 0) if son else None
            mdeg=None if (not son or not md or not sm) else md-sm
            jk=pg.get('jokey'); onceki_jk=son[6] if son else None
            hpn=pg.get('hp'); kln=pg.get('kilo')
            hp_sira=(1+sum(1 for v in P['atlar'].values() if v['hp'] and hpn and v['hp']>hpn)) if hpn else None
            kl_sira=(1+sum(1 for v in P['atlar'].values() if v['kilo'] and kln and v['kilo']>kln)) if kln else None
            JA.setdefault(hip,{}).setdefault(str(r['kosu']),{'grup':grup,'atlar':{}})['atlar'][ad]={
                'zemin_sicil':zs,'zemin_tercih':tercih,'zemin_gecis':gecis,'son_zemin':son[3] if son else None,
                'son':({'tarih':son[0],'hip':son[1],'mesafe':sm,'zemin':son[3],'sira':son[4],'kosan':son[5],'jokey':onceki_jk,'kilo':son[7],'hp':son[8]} if son else None),
                'mesafe_degisim':mdeg,'jokey':jk,'onceki_jokey':onceki_jk,'jokey_degisti':(None if not jk or not onceki_jk else _jk_key(jk)!=_jk_key(onceki_jk)),
                'apranti':bool(jk and re.search(r'\bAP\b',jk)),'kilo':kln,'kilo_sira':kl_sira,'kilo_fark_son':(round(kln-son[7],1) if kln and son and son[7] else None),
                'hp':hpn,'hp_sira':hp_sira,'hp_fark_ort':(round(hpn-_ort,1) if hpn and _ort else None),'hp_fark_son':(round(hpn-son[8],1) if hpn and son and son[8] else None)}
os.makedirs(os.path.join(K,'veri','hipodrom_sicil'),exist_ok=True)
json.dump(JS,open(os.path.join(K,'veri','hipodrom_sicil',f'{GUN}.json'),'w',encoding='utf-8'),ensure_ascii=False)
json.dump(JM,open(os.path.join(K,'veri','hipodrom_sicil',f'{GUN}_mesafe.json'),'w',encoding='utf-8'),ensure_ascii=False)
json.dump(JA,open(os.path.join(K,'veri','hipodrom_sicil',f'{GUN}_analiz.json'),'w',encoding='utf-8'),ensure_ascii=False)
open(os.path.join(K,'veri','hipodrom_sicil',f'{GUN}.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('yazıldı veri/hipodrom_sicil/%s.md | %d hipodrom, %d at'%(GUN,len(hiplar),len(adlar)))
