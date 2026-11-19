"""Koşudan hemen önce: güncel muhtemel ganyanı (TJK program sayfası, Gny sütunu) çekip DONDURULMUŞ tahminlerle karşılaştırır.
Kullanım: ganyan_kontrol.py GG.AA.YYYY Hipodrom [model: v8|agfsiz|(boş=v6 sabah)]
Değer: ganyan ≥ 1,5 / olasılık (geçmiş testte 1,5× eşiği; 70 bahislik küçük örnek, kanıtlanmış değil).
Not: ganyan son dakikaya kadar değişir; eküri atları tek birimdir (olasılıkları toplanır).
💰 PARA GİRİŞİ: gün içindeki AGF/ganyan kayıtlarına göre (scripts/para_girisi.py); henüz test edilmedi, bilgi amaçlı."""
import sys,os,re,json,subprocess,urllib.parse,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date(); hip=sys.argv[2]; sr=sys.argv[3] if len(sys.argv)>3 else ''
T=json.load(open(os.path.join(K,'veri','tahminler',f"{g.isoformat()}_{hip}{'_'+sr if sr else ''}.json"),encoding='utf-8'))
tq=urllib.parse.quote(g.strftime('%d/%m/%Y'),safe='')
ana=subprocess.run(['curl','-sS','--max-time','90',f"https://www.tjk.org/TR/YarisSever/Info/Page/GunlukYarisProgrami?QueryParameter_Tarih={tq}"],capture_output=True).stdout.decode('utf-8','replace')
SID={a:i for i,a in re.findall(r'data-sehir-id="(\d+)" href="[^"]+">\s*([^<(]+?)\s*[(<]',ana)}
t=subprocess.run(['curl','-sS','--max-time','90',f"https://www.tjk.org/TR/YarisSever/Info/Sehir/GunlukYarisProgrami?SehirId={SID[hip]}&QueryParameter_Tarih={tq}&SehirAdi={urllib.parse.quote(hip)}&Era=today"],capture_output=True).stdout.decode('utf-8','replace')
GNY={};BIT={}
for a,v in zip(re.findall(r'gunluk-GunlukYarisProgrami-AtAdi"[^>]*>(.*?)</td>',t,flags=re.S),re.findall(r'gunluk-GunlukYarisProgrami-Gny"[^>]*>(.*?)</td>',t,flags=re.S)):
    m=re.search(r'>\s*([^<]+?)\s*<span',a) or re.search(r'>\s*([^<]+?)\s*</a>',a); b=re.search(r'koşuyu (\d+)\. olarak',a)
    try: GNY[m.group(1).strip()]=float(re.sub(r'<[^>]+>','',v).strip().replace(',','.'))
    except Exception: pass
    if m and b: BIT[m.group(1).strip()]=int(b.group(1))
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import para_girisi
PG=para_girisi.hesapla(g.isoformat(),hip)
print(f"=== {hip} {g} ganyan kontrolü ({datetime.datetime.now(datetime.timezone.utc):%H:%M} UTC), model: {sr or 'v6 sabah'} ===")
for k in T:
    A=k['atlar']; ekp=sum(a['p'] for a in A if a['ekuri'])
    if any(a['ad'] in BIT for a in A): print(f"  {k['kosu']}. koşu: bitti"); continue
    sat=[]
    # piyasa oturdu mu? (eküri tek birim) normalde toplam(1/ganyan) ~1,25-1,45
    U={}
    for a in A:
        gy=GNY.get(a['ad'])
        if gy and gy>1: U['ek' if a['ekuri'] else a['ad']]=gy
    top=sum(1/v for v in U.values()) if U else 0; otur=1.15<=top<=1.6
    for a in sorted(A,key=lambda a:-a['p'])[:5]:
        pe=ekp if a['ekuri'] else a['p']; gy=GNY.get(a['ad'])
        if not gy or gy<=1: continue
        sat.append(f"{a['no']} {a['ad'][:14]} %{100*a['p']:.0f}{'(eküri %'+format(100*ekp,'.0f')+')' if a['ekuri'] else ''} ganyan {gy:.2f} (eşik {1.5/pe:.1f})"+(' ★GANYAN' if otur and gy>=1.5/pe and pe>=0.05 else '')
                   +(f" 💰PARA GİRİŞİ (AGF %{PG[a['ad']].get('agf_ilk','?')}→%{PG[a['ad']].get('agf_son','?')}, ganyan {PG[a['ad']].get('ganyan_ilk','?')}→{PG[a['ad']].get('ganyan_son','?')})" if PG.get(a['ad'],{}).get('isaret') else ''))
    print(f"  {k['kosu']}. koşu{'' if otur else f' [PİYASA OTURMAMIŞ: toplam {top:.2f}, işaret yok]'}: "+' | '.join(sat))
