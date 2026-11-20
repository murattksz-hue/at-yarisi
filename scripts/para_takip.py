"""Para girişi takibi (koşu bazında, gerçek kayıtlar). Koşu bittikten sonra çalışır.
Kullanım: para_takip.py YYYY-AA-GG Hipodrom KosuNo
Kaynak: veri/agf_kayit/<tarih>/<hip>_<HHMM>UTC_ebayi.json görüntüleri ({koşu:{at:[AGF1,AGF2,GANYAN,KOSMAZ]}}), koşu saati veri/plan/<tarih>.json,
sonuç ve kesin ganyan ebayi sonuclar JSON'u. Her at için: sabah AGF, son AGF, koşudan 60/30/10 dk önceki ve son muhtemel ganyan, kesin ganyan, sonuç.
💰 işareti (TEST EDİLMEDİ, bilgi): son 30 dk'da ganyan ≥1,4 kat düştü (son ganyan ≤20). Satırlar veri/para_takip.csv'ye eklenir (tekrar yazılmaz)."""
import sys,os,glob,json,csv,urllib.request
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T,H,NO=sys.argv[1],sys.argv[2],sys.argv[3]
EBK={'ADANA':'Adana','IZMIR':'İzmir','ISTANBUL':'İstanbul','BURSA':'Bursa','ANKARA':'Ankara','SANLIURFA':'Şanlıurfa','ELAZIG':'Elazığ','DIYARBAKIR':'Diyarbakır','KOCAELI':'Kocaeli','ANTALYA':'Antalya'}
KEY={v:k for k,v in EBK.items()}[H]
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
saat=json.load(open(os.path.join(K,'veri','plan',f'{T}.json'),encoding='utf-8'))['kosular'][H][NO]; bas=int(saat[:2])*60+int(saat[3:])
G=[]
for p in sorted(glob.glob(os.path.join(K,'veri','agf_kayit',T,f"{H}_*UTC_ebayi.json"))):
    hm=os.path.basename(p)[len(H)+1:len(H)+5]; m=((int(hm[:2])+3)%24)*60+int(hm[2:])
    if m<bas: G.append((m,json.load(open(p,encoding='utf-8')).get(NO,{})))
if not G: sys.exit('görüntü yok')
r=urllib.request.Request(f"https://ebayi.org/s/d/sonuclar/{T.replace('-','')}/full/{KEY}.json",headers={'User-Agent':'Mozilla/5.0'})
S=json.loads(urllib.request.urlopen(r,timeout=40).read().decode('utf-8'))
kos=next((k for k in S.get('kosular',[]) if str(k.get('NO'))==NO),None)
if not kos or not any(str(a.get('SONUC'))=='1' for a in kos.get('atlar',[])): sys.exit('sonuç yok')
def once(dk,at,i):   # koşudan en az dk dakika önceki son görüntü
    v=[(m,x) for m,x in G if bas-m>=dk and at in x and f(x[at][i])]
    return (f(v[-1][1][at][i]),v[-1][0]) if v else (None,None)
out=os.path.join(K,'veri','para_takip.csv'); var=set()
if os.path.exists(out): var={(r['tarih'],r['hip'],r['kosu'],r['at']) for r in csv.DictReader(open(out,encoding='utf-8'))}
# belirsiz koşu: dondurulmuş tahminde ≥5 aday (oneri_at); sessiz AGF: sabah→son değişim ≤1 puan (AGF ≥%2) – TEST EDİLMEDİ, takip
tf=os.path.join(K,'veri','tahminler',f"{T}_{H}.json"); belirsiz=0
if os.path.exists(tf): belirsiz=int(next((r.get('oneri_at',0) for r in json.load(open(tf,encoding='utf-8')) if r['kosu']==NO),0)>=5)
yeni=[]
for a in kos['atlar']:
    if a.get('KOSMAZ'): continue
    at=a['AD']; agf=[f(x[at][0]) for m,x in G if at in x and f(x[at][0])]
    g60,_=once(60,at,2); g30,_=once(30,at,2); g10,_=once(10,at,2); gs,ms=once(0,at,2)
    isaret=bool(g30 and gs and gs<=20 and g30/gs>=1.4)
    yeni.append(dict(tarih=T,hip=H,kosu=NO,saat=saat,at=at,agf_sabah=agf[0] if agf else '',agf_son=agf[-1] if agf else '',
        g60=g60 or '',g30=g30 or '',g10=g10 or '',g_son=gs or '',g_son_dk=(bas-ms) if ms is not None else '',kesin=f(a.get('GANYAN')) or '',
        sonuc=a.get('SONUC'),para=int(isaret),belirsiz=belirsiz,sessiz=int(bool(agf) and agf[0]>=2 and abs(agf[-1]-agf[0])<=1.0)))
# ⭐ sürpriz adayı sinyali (geçmiş test: 2.047 bahis, %8 kazandı, ganyan getirisi %127; 2024 %126 / 2025 %133 / 2026 %121 – ama KESİN ganyan ve son AGF ile;
# canlıda koşu öncesi SON görüntüyle ölçülüyor): son ganyan ≥10, AGF payı ≥1,3 × ganyan olasılığı, HP ilk 3. TEST EDİLİYOR, olasılığa katılmaz.
HP={a['AD']:f(a.get('HANDIKAP')) or 0 for a in kos['atlar'] if not a.get('KOSMAZ')}; hps={a:i+1 for i,a in enumerate(sorted(HP,key=lambda a:-HP[a]))}
gs_={y['at']:f(y['g_son']) for y in yeni if f(y['g_son'])}; tq=sum(1/g for g in gs_.values()) if gs_ else 0
for y in yeni:
    g=gs_.get(y['at']); a=f(y['agf_son'])
    y['sinyal']=int(bool(g and tq and a and g>=10 and (a/100)>=1.3*(1/g)/tq and hps.get(y['at'],99)<=3))
yaz=[y for y in yeni if (y['tarih'],y['hip'],y['kosu'],y['at']) not in var]
if yaz:
    alan=list(yaz[0])
    if os.path.exists(out):
        eski=list(csv.DictReader(open(out,encoding='utf-8')))
        if eski and set(alan)-set(eski[0]):   # yeni sütun eklendiyse dosya birleşik başlıkla yeniden yazılır
            ea=list(eski[0])+[k for k in alan if k not in eski[0]]; w=csv.DictWriter(open(out,'w',encoding='utf-8',newline=''),fieldnames=ea); w.writeheader(); w.writerows(eski)
        alan=list(csv.DictReader(open(out,encoding='utf-8')).fieldnames or alan)
    ilk=not os.path.exists(out); w=csv.DictWriter(open(out,'a',encoding='utf-8',newline=''),fieldnames=alan,extrasaction='ignore')
    if ilk: w.writeheader()
    w.writerows(yaz)
for y in sorted(yeni,key=lambda y:int(y['sonuc']) if str(y['sonuc']).isdigit() else 99):
    print(f"{'💰' if y['para'] else '  '}{'🤫' if y['sessiz'] else '  '}{'⭐' if y.get('sinyal') else '  '} {y['sonuc']:>2}. {y['at'][:18]:18} AGF %{y['agf_sabah']}→%{y['agf_son']} | gny -60:{y['g60']} -30:{y['g30']} -10:{y['g10']} son:{y['g_son']}({y['g_son_dk']}dk) kesin:{y['kesin']}")
