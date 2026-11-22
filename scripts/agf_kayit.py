"""AGF anlık görüntüsü. Kullanım: agf_kayit.py [GG.AA.YYYY]
O günün Türkiye hipodromlarının program CSV'sini (AGF sütunu) çeker; AGF bir önceki görüntüden farklıysa
veri/agf_kayit/<tarih>/<hipodrom>_<SSDD>UTC.csv olarak saklar. AGF'nin ilk dolu olduğu görüntü ayrıca
veri/agf_kayit/<tarih>/ILK_<hipodrom>.csv olarak saklanır (kullanıcı gözlemi: sabah ilk AGF daha isabetli olabilir; test edilecek)."""
import sys,os,re,glob,subprocess,urllib.parse,datetime,hashlib
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date() if len(sys.argv)>1 else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date()
TR={'İstanbul','Ankara','İzmir','Bursa','Adana','Kocaeli','Elazığ','Diyarbakır','Şanlıurfa','Antalya'}
tq=urllib.parse.quote(g.strftime('%d/%m/%Y'),safe='')
ana=subprocess.run(['curl','-sS','--max-time','90',f"https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisProgrami?QueryParameter_Tarih={tq}"],capture_output=True).stdout.decode('utf-8','replace')
SIDS={a:i for i,a in re.findall(r'data-sehir-id="(\d+)" href="[^"]+">\s*([^<(]+?)\s*[(<]',ana) if a in TR}; hips=list(SIDS)
kd=os.path.join(K,'veri','agf_kayit',g.isoformat()); os.makedirs(kd,exist_ok=True); saat=datetime.datetime.now(datetime.timezone.utc).strftime('%H%M')
def _iz(h,kaynak,saat):   # ilk_zaman.json: {hipodrom:{tjk:'HHMM UTC', ebayi:'HHMM UTC'}}
    import json as _j; f=os.path.join(kd,'ilk_zaman.json'); D=_j.load(open(f,encoding='utf-8')) if os.path.exists(f) else {}
    D.setdefault(h,{}).setdefault(kaynak,saat+' UTC'); _j.dump(D,open(f,'w',encoding='utf-8'),ensure_ascii=False)
def agf_kismi(b):   # yalnızca at satırlarının AGF sütunu (değişim karşılaştırması için)
    return [l.split(';')[10] for l in b.decode('utf-8-sig','replace').splitlines() if re.match(r'^\d+;',l) and len(l.split(';'))>10]
for h in hips:
    u=f"https://medya-cdn.tjk.org/raporftp/TJKPDF/{g.year}/{g.isoformat()}/CSV/GunlukYarisProgrami/{g.strftime('%d.%m.%Y')}-{urllib.parse.quote(h)}-GunlukYarisProgrami-TR.csv?t={int(datetime.datetime.now().timestamp())}"   # ?t=: CDN önbelleğini (max-age=600, 10 dk'ya kadar eski) atlatır; 22.11.2026'da doğrulandı
    b=subprocess.run(['curl','-sS','-f','--max-time','90',u],capture_output=True).stdout
    if not b: print(h,': CSV yok'); continue
    # ganyan (Gny) anlık görüntüsü: program HTML'inden, her seferinde saklanır (para girişi takibi için)
    import json,html as H_
    era='today' if g==datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))).date() else 'tomorrow'
    ht=subprocess.run(['curl','-sS','--max-time','90',f"https://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisProgrami?SehirId={SIDS[h]}&QueryParameter_Tarih={tq}&SehirAdi={urllib.parse.quote(h)}&Era={era}"],capture_output=True).stdout.decode('utf-8','replace')
    GN={}
    for a_,v_ in zip(re.findall(r'gunluk-GunlukYarisProgrami-AtAdi"[^>]*>(.*?)</td>',ht,flags=re.S),re.findall(r'gunluk-GunlukYarisProgrami-Gny"[^>]*>(.*?)</td>',ht,flags=re.S)):
        m_=re.search(r'>\s*([^<]+?)\s*<span',a_) or re.search(r'>\s*([^<]+?)\s*</a>',a_)
        try: GN[m_.group(1).strip()]=float(re.sub(r'<[^>]+>','',v_).strip().replace(',','.'))
        except Exception: pass
    if GN: json.dump(GN,open(os.path.join(kd,f"{h}_{saat}UTC_ganyan.json"),'w'),ensure_ascii=False)
    a=agf_kismi(b); dolu=sum(bool(re.match(r'%[\d.]+',x)) for x in a)
    onceki=sorted(f for f in glob.glob(os.path.join(kd,f"{h}_*UTC.csv")))
    if onceki and agf_kismi(open(onceki[-1],'rb').read())==a: print(f"{h}: AGF değişmemiş ({dolu}/{len(a)} at dolu)"); continue
    open(os.path.join(kd,f"{h}_{saat}UTC.csv"),'wb').write(b)
    ilk=os.path.join(kd,f"ILK_{h}.csv")
    if dolu>0 and not os.path.exists(ilk): open(ilk,'wb').write(b); print(f"{h}: İLK AGF kaydedildi ({saat} UTC, {dolu}/{len(a)} at)"); _iz(h,'tjk',saat)
    else: print(f"{h}: yeni görüntü {saat} UTC ({dolu}/{len(a)} at dolu)")
# ebayi.org (TJK resmî bayisi) anlık görüntüsü: AGF1, AGF2, canlı ganyan ve koşmaz bilgisi tek dosyada (TJK sayfası gecikirse yedek kaynak)
import json
EBK={'IZMIR':'İzmir','ISTANBUL':'İstanbul','SANLIURFA':'Şanlıurfa','ELAZIG':'Elazığ','DIYARBAKIR':'Diyarbakır','ADANA':'Adana','BURSA':'Bursa','ANKARA':'Ankara','KOCAELI':'Kocaeli','ANTALYA':'Antalya'}
def _eb(p):
    try: return json.loads(subprocess.run(['curl','-sS','-f','--max-time','60','-A','Mozilla/5.0','https://ebayi.org/s/d/'+p],capture_output=True).stdout.decode('utf-8'))
    except Exception: return None
for y in (_eb(f"program/{g:%Y%m%d}/yarislar.json") or []):
    if y.get('KEY') not in EBK: continue
    J=_eb(f"program/{g:%Y%m%d}/full/{y['KEY']}.json")
    if not J: continue
    S={str(k['NO']):{a['AD'].strip():[a.get('AGF1'),a.get('AGF2'),a.get('GANYAN'),bool(a.get('KOSMAZ'))] for a in k.get('atlar',[])} for k in J.get('kosular',[])}
    json.dump(S,open(os.path.join(kd,f"{EBK[y['KEY']]}_{saat}UTC_ebayi.json"),'w',encoding='utf-8'),ensure_ascii=False)
    # ebayi'de AGF'nin ilk göründüğü görüntü (TJK ILK ile hangisi önce yayınlıyor karşılaştırması)
    ie=os.path.join(kd,f"ILK_{EBK[y['KEY']]}_ebayi.json")
    if not os.path.exists(ie) and any(v[0] for A in S.values() for v in A.values()):
        json.dump(S,open(ie,'w',encoding='utf-8'),ensure_ascii=False); print(f"{EBK[y['KEY']]}: ebayi İLK AGF kaydedildi ({saat} UTC)"); _iz(EBK[y['KEY']],'ebayi',saat)
    print(f"{EBK[y['KEY']]}: ebayi görüntüsü {saat} UTC ({sum(len(v) for v in S.values())} at)")
# ebayi MUHTEMELLER (herkese açık CDN, sayfanın kendi okuduğu dosyalar): her koşunun anlık muhtemel ganyanı ve koşu durumu.
# checksum: vhs-medya.ebayi.org/muhtemeller/s/YYYY/AA/GG/checksum.json → runs{HIP-NO:[kısa,tam]} ; tam dosya: vhs-medya-cdn.../s/YYYY/AA/GG/HIP-NO-full-<run>.json
def _mh(u):
    try: return json.loads(subprocess.run(['curl','-sS','-f','--max-time','60','-A','Mozilla/5.0',u],capture_output=True).stdout.decode('utf-8'))
    except Exception: return None
_ck=_mh(f"https://vhs-medya.ebayi.org/muhtemeller/s/{g:%Y/%m/%d}/checksum.json")
if _ck and _ck.get('runs'):
    MH={}
    for key,(kisa,tam) in _ck['runs'].items():
        hk,no=key.rsplit('-',1)
        if hk not in EBK: continue
        J=_mh(f"https://vhs-medya-cdn.ebayi.org/muhtemeller/s/{g:%Y/%m/%d}/{key}-full-{tam}.json")
        m=((J or {}).get('data') or {}).get('muhtemeller') or {}
        gb=next((b for b in m.get('bahisler',[]) if b.get('B')=='GANYAN'),None)
        if gb: MH.setdefault(EBK[hk],{})[no]=dict(durum=m.get('DURUM'),ts=m.get('timestamp'),ganyan={x['S1']:x.get('G') for x in gb.get('muhtemeller',[])},ekuri=[x['S1'] for x in gb.get('muhtemeller',[]) if x.get('E')])
    for h_,v_ in MH.items():
        json.dump(v_,open(os.path.join(kd,f"{h_}_{saat}UTC_muhtemel.json"),'w',encoding='utf-8'),ensure_ascii=False)
        print(f"{h_}: ebayi muhtemel ganyan {saat} UTC ({len(v_)} koşu)")
