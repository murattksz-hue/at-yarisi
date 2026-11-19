"""Canlı test: koşudan ÖNCE dondurulmuş tahminleri (veri/tahminler/) gerçek sonuçla karşılaştırır.
Kullanım: canli_takip.py GG.AA.YYYY Hipodrom
Sonuç kaynağı: TJK günlük program sayfası ("X. olarak bitirmiştir"). Biten koşular veri/canli_takip.csv'ye yazılır (aynı koşu bir kez)."""
import sys,os,re,json,subprocess,urllib.parse,datetime,math,csv
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date(); hip=sys.argv[2]; SURUM=sys.argv[3] if len(sys.argv)>3 else ''
T=json.load(open(os.path.join(K,'veri','tahminler',f"{g.isoformat()}_{hip}{'_'+SURUM if SURUM else ''}.json"),encoding='utf-8'))
era='today' if g==datetime.date.today() else 'past'
tq=urllib.parse.quote(g.strftime('%d/%m/%Y'),safe='')
ana=subprocess.run(['curl','-sS','--max-time','90',f"https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisProgrami?QueryParameter_Tarih={tq}"],capture_output=True).stdout.decode('utf-8','replace')
SID={a:int(i) for i,a in re.findall(r'data-sehir-id="(\d+)" href="[^"]+">\s*([^<(]+?)\s*[(<]',ana)}
if hip not in SID: sys.exit(f"{hip} için TJK sayfasında yarış bulunamadı")
u=f"https://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisProgrami?SehirId={SID[hip]}&QueryParameter_Tarih={urllib.parse.quote(g.strftime('%d/%m/%Y'),safe='')}&SehirAdi={urllib.parse.quote(hip)}&Era={era}"
t=subprocess.run(['curl','-sS','--max-time','90',u],capture_output=True).stdout.decode('utf-8','replace')
bitis={}
for v in re.findall(r'gunluk-GunlukYarisProgrami-AtAdi"[^>]*>(.*?)</td>',t,flags=re.S):
    m=re.search(r'>\s*([^<]+?)\s*<span',v); b=re.search(r'koşuyu (\d+)\. olarak',v)
    if m and b: bitis[m.group(1).strip()]=int(b.group(1))
LOG=os.path.join(K,'veri',f"canli_takip{'_'+SURUM if SURUM else ''}.csv"); eski=set()
if os.path.exists(LOG): eski={(r['tarih'],r['hipodrom'],r['kosu']) for r in csv.DictReader(open(LOG,encoding='utf-8'))}
yeni=[]; print(f"=== {hip} {g} canlı takip {SURUM or 'v6 (sabah)'} ({datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC) ===")
for k in T:
    A=[dict(a,bitis=bitis.get(a['ad'])) for a in k['atlar']]
    if not any(a['bitis']==1 for a in A): print(f"  {k['kosu']}. koşu: henüz sonuç yok"); continue
    srt=sorted(A,key=lambda a:-a['p']); kaz=next(a for a in A if a['bitis']==1)
    # eküri: birim olarak
    ekp=sum(a['p'] for a in A if a['ekuri']); kaz_p=ekp if kaz['ekuri'] else kaz['p']
    agf_var=not k['agf_yok']; fav=max(A,key=lambda a:a['agf']) if agf_var else None
    kaz_agf=(sum(a['agf'] for a in A if a['ekuri']) if kaz['ekuri'] else kaz['agf']) if agf_var else None
    deg=[a for a in A if agf_var and a['agf']>0 and a['p']/a['agf']>=1.5 and a['p']>=0.05]
    sat=dict(tarih=g.isoformat(),hipodrom=hip,kosu=k['kosu'],model_1=srt[0]['ad'],model_1_p=round(srt[0]['p'],3),model_1_bitis=srt[0]['bitis'],
        kazanan=kaz['ad'],kazanan_model_sira=srt.index(kaz)+1,kazanan_p=round(kaz_p,3),kazanan_agf=round(kaz_agf,3) if kaz_agf is not None else '',
        agf_favori=fav['ad'] if fav else '',agf_favori_bitis=fav['bitis'] if fav else '',
        deger_atlar=';'.join(f"{a['ad']}:{a['bitis']}" for a in deg),log_model=round(math.log(max(kaz_p,1e-6)),4),log_agf=round(math.log(max(kaz_agf,1e-6)),4) if kaz_agf else '')
    print(f"  {k['kosu']}. koşu: kazanan {kaz['ad']} (model sırası {sat['kazanan_model_sira']}, model %{100*kaz_p:.0f}"+(f", AGF %{100*kaz_agf:.0f}" if kaz_agf is not None else '')+
          f") | model 1. adayı {srt[0]['ad']} → {srt[0]['bitis']}."+(f" | AGF favorisi {fav['ad']} → {fav['bitis']}." if fav else '')+(f" | ★DEĞER: {sat['deger_atlar']}" if deg else ''))
    if (sat['tarih'],sat['hipodrom'],sat['kosu']) not in eski: yeni.append(sat)
if yeni:
    ilk=not os.path.exists(LOG)
    with open(LOG,'a',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(yeni[0].keys()))
        if ilk: w.writeheader()
        w.writerows(yeni)
# kümülatif özet
if os.path.exists(LOG):
    R=list(csv.DictReader(open(LOG,encoding='utf-8'))); n=len(R)
    m1=sum(r['model_1_bitis']=='1' for r in R); m3=sum(int(r['kazanan_model_sira'])<=3 for r in R)
    A_=[r for r in R if r['agf_favori']]; af=sum(r['agf_favori_bitis']=='1' for r in A_)
    LL=[(float(r['log_model']),float(r['log_agf'])) for r in R if r['log_agf']!='']
    D=[x for r in R for x in r['deger_atlar'].split(';') if x]
    print(f"\nKÜMÜLATİF ({n} koşu): model 1. adayı kazandı {m1} (%{100*m1/n:.0f}), kazanan ilk 3'te {m3} (%{100*m3/n:.0f})"
          +(f" | AGF favorisi kazandı {af}/{len(A_)} (%{100*af/len(A_):.0f})" if A_ else '')
          +(f" | ort. log-olasılık model {sum(a for a,_ in LL)/len(LL):.3f} vs AGF {sum(b for _,b in LL)/len(LL):.3f}" if LL else '')
          +(f" | ★DEĞER: {len(D)} at, kazanan {sum(x.endswith(':1') for x in D)}" if D else ''))

v8=os.path.join(K,'veri','tahminler',f"{g.isoformat()}_{hip}_v8.json")
if not SURUM and os.path.exists(v8):
    print(); subprocess.run([sys.executable,'-I',os.path.abspath(__file__),sys.argv[1],hip,'v8'])
