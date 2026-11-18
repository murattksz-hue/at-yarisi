"""Hipodrom hava verisi (Open-Meteo, anahtarsız). Kullanım:
  hava.py gecmis BASLANGIC BITIS cikti.json   -> günlük yağış/sıcaklık/nem/rüzgar arşivi
  hava.py tahmin GG.AA.YYYY                    -> o gün için tahmin (hipodrom başına)
Islaklık = o günün yağışı + önceki günün yağışının yarısı (mm)."""
import sys,json,subprocess,urllib.parse,datetime
HIP={'İstanbul':(40.985,28.875),'Ankara':(39.955,32.735),'İzmir':(38.390,27.150),'Bursa':(40.215,29.000),'Adana':(36.990,35.260),
     'Kocaeli':(40.730,30.020),'Elazığ':(38.665,39.220),'Diyarbakır':(37.905,40.200),'Şanlıurfa':(37.170,38.790),'Antalya':(36.930,30.800)}
D='precipitation_sum,temperature_2m_max,relative_humidity_2m_mean,wind_speed_10m_max'
def get(u):
    import time
    for i in range(6):
        b=subprocess.run(['curl','-sS','--max-time','60',u],capture_output=True).stdout
        try: return json.loads(b)
        except Exception: time.sleep(3*(i+1))
    raise SystemExit('hava verisi alınamadı: '+u)
def kategori(isl): return 'kuru' if isl<1 else ('hafif' if isl<5 else 'ıslak')
if sys.argv[1]=='gecmis':
    import time,os
    bas,bit,out=sys.argv[2:5]; R=json.load(open(out)) if os.path.exists(out) else {}
    for h,(la,lo) in HIP.items():
        if f"{bit}_{h}" in R and f"{bas}_{h}" in R: continue
        time.sleep(2); d=get(f"https://archive-api.open-meteo.com/v1/archive?latitude={la}&longitude={lo}&start_date={bas}&end_date={bit}&daily={D}&timezone=Europe%2FIstanbul")['daily']
        for i,t in enumerate(d['time']):
            y=d['precipitation_sum'][i] or 0; yo=(d['precipitation_sum'][i-1] or 0) if i else 0
            R[f"{t}_{h}"]=dict(yagis=y,islaklik=round(y+0.5*yo,1),sicaklik=d['temperature_2m_max'][i],nem=d['relative_humidity_2m_mean'][i],ruzgar=d['wind_speed_10m_max'][i])
    json.dump(R,open(out,'w'),ensure_ascii=False); print(len(R),'gün-hipodrom kaydı')
else:
    g=datetime.datetime.strptime(sys.argv[2],'%d.%m.%Y').date(); o=g-datetime.timedelta(days=1)
    for h,(la,lo) in HIP.items():
        if len(sys.argv)>3 and h not in sys.argv[3:]: continue
        b=subprocess.run(['curl','-sS','--max-time','60',f"https://api.open-meteo.com/v1/forecast?latitude={la}&longitude={lo}&start_date={o}&end_date={g}&daily={D}&timezone=Europe%2FIstanbul"],capture_output=True).stdout
        try:
            d=json.loads(b)['daily']; y,yo,sc,nm,rz=d['precipitation_sum'][1],d['precipitation_sum'][0],d['temperature_2m_max'][1],d['relative_humidity_2m_mean'][1],d['wind_speed_10m_max'][1]; kay='open-meteo'
        except Exception:   # yedek: wttr.in
            w={x['date']:x for x in get(f"https://wttr.in/{la},{lo}?format=j1")['weather']}
            f=lambda t,k:sum(float(hh[k]) for hh in w[str(t)]['hourly']) if str(t) in w else 0
            y,yo=f(g,'precipMM'),f(o,'precipMM'); sc=float(w[str(g)]['maxtempC']) if str(g) in w else None
            nm=f(g,'humidity')/8 if str(g) in w else None; rz=max(float(hh['windspeedKmph']) for hh in w[str(g)]['hourly']) if str(g) in w else None; kay='wttr.in'
        isl=(y or 0)+0.5*(yo or 0)
        print(json.dumps(dict(hipodrom=h,tarih=str(g),yagis=round(y or 0,1),onceki_gun=round(yo or 0,1),islaklik=round(isl,1),kategori=kategori(isl),
            sicaklik=sc,nem=round(nm) if nm else None,ruzgar=rz,kaynak=kay),ensure_ascii=False))
