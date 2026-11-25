"""BİRLEŞİK tahmin puanlama. Kullanım: birlesik_puan.py [YYYY-AA-GG]   (varsayılan bugün)
Girdi: veri/tahminler_birlesik/<tarih>.json (koşudan önce kaydedildi) + ebayi.org sonuç JSON'u (canli_takip.py ile aynı kaynak, koşmaz atlar sayılmaz).
Her kol için: 1. seçim kazandı mı, kazananın log-olasılığı (p yoksa/0 ise 1e-4 tabanı). Çıktı: veri/tahminler_birlesik/<tarih>_puan.md (yeni dosya).
Kollar: birlesik, v9_agfli, v9_agfsiz, piyasa. Küçük örnekte aralık verilmez; ≥300 koşuda bootstrap eklenecek (YAPILACAK #25)."""
import os,sys,json,re,math,subprocess,datetime,collections
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR=datetime.timezone(datetime.timedelta(hours=3))
gun=sys.argv[1] if len(sys.argv)>1 else datetime.datetime.now(TR).date().isoformat()
g=datetime.date.fromisoformat(gun)
EB={'İzmir':'IZMIR','İstanbul':'ISTANBUL','Şanlıurfa':'SANLIURFA','Elazığ':'ELAZIG','Diyarbakır':'DIYARBAKIR','Adana':'ADANA','Bursa':'BURSA','Ankara':'ANKARA','Kocaeli':'KOCAELI','Antalya':'ANTALYA'}
anahtar=lambda s:re.sub(r'\W','',str(s).upper())
S=json.load(open(os.path.join(K,'veri','tahminler_birlesik',f'{gun}.json'),encoding='utf-8'))
ARMS=['birlesik','v9_agfli','v9_agfsiz','piyasa']; PK={'birlesik':'p_birlesik','v9_agfli':'p_v9_agfli','v9_agfsiz':'p_v9_agfsiz','piyasa':'p_piyasa'}
acc={a:dict(n=0,top1=0,ll=0.0) for a in ARMS}; kayit=[]
for hip,H in S['hipodromlar'].items():
    try:
        J=json.loads(subprocess.run(['curl','-sS','--max-time','60','-A','Mozilla/5.0',f"https://ebayi.org/s/d/sonuclar/{g:%Y%m%d}/full/{EB.get(hip,hip.upper())}.json"],capture_output=True).stdout.decode('utf-8'))
    except Exception: continue
    SON={str(k['NO']):{anahtar(a['AD']):int(a['SONUC']) for a in k.get('atlar',[]) if not a.get('KOSMAZ') and str(a.get('SONUC') or '').isdigit()} for k in J.get('kosular',[])}
    for k in H['kosular']:
        r=SON.get(str(k['kosu']));
        if not r or 1 not in r.values(): continue
        win=[a for a in k['atlar'] if r.get(anahtar(a['ad']))==1]
        if len(win)!=1: continue
        w=win[0]; satir=dict(hip=hip,kosu=k['kosu'],kazanan=w['ad'],uyari=bool(H.get('uyari')))
        for a in ARMS:
            ps=[x.get(PK[a]) for x in k['atlar']]
            if any(p is None for p in ps): satir[a]=None; continue
            top=max(k['atlar'],key=lambda x:x[PK[a]]); pw=w[PK[a]]
            satir[a]=(r.get(anahtar(top['ad']))==1,math.log(max(pw,1e-4)))
            acc[a]['n']+=1; acc[a]['top1']+=satir[a][0]; acc[a]['ll']+=satir[a][1]
        kayit.append(satir)
L=[f'# BİRLEŞİK puanlama — {gun}','',f'Biten ve puanlanan koşu: **{len(kayit)}**. Örnek küçük; sıralama kanıt değildir.','','| Kol | Koşu | 1. seçim kazandı | Kazananın ort. log-olasılığı |','|---|---|---|---|']
for a in ARMS:
    d=acc[a]; L.append(f"| {a} | {d['n']} | {d['top1']} ({100*d['top1']/max(d['n'],1):.0f}%) | {d['ll']/max(d['n'],1):.3f} |")
L+=['','## Koşu koşu','','| Hipodrom | Koşu | Kazanan | birlesik | v9 AGF\'li | v9 AGF\'siz | piyasa |','|---|---|---|---|---|---|---|']
for s in kayit: L.append(f"| {s['hip']}{' ⚠' if s['uyari'] else ''} | {s['kosu']} | {s['kazanan'][:16]} | "+' | '.join(('—' if s[a] is None else ('✅' if s[a][0] else '❌')+f' {math.exp(s[a][1])*100:.0f}%') for a in ARMS)+' |')
L+=['','_⚠ = v9 AGF\'li kolu kısmi AGF\'yle dondurulmuş (ayrı değerlendir). Hücre: ilk seçim kazandı mı + kazanana verilen olasılık._']
open(os.path.join(K,'veri','tahminler_birlesik',f'{gun}_puan.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('\n'.join(L[:10]))
