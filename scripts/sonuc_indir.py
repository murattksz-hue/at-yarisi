import urllib.request,urllib.parse,datetime,os,time,sys
out=sys.argv[1]; gun=int(sys.argv[2]); os.makedirs(out,exist_ok=True)
sehirler=['İstanbul','Ankara','İzmir','Bursa','Adana','Kocaeli','Elazığ','Diyarbakır','Şanlıurfa','Antalya']
bugun=datetime.date(2026,11,18); n=0
for d in range(1,gun+1):
    t=bugun-datetime.timedelta(days=d)
    for s in sehirler:
        fn=os.path.join(out,f"{t.isoformat()}_{s}.csv")
        if os.path.exists(fn) or os.path.exists(fn+'.yok'): continue
        u=f"https://medya-cdn.tjk.org/raporftp/TJKPDF/{t.year}/{t.isoformat()}/CSV/GunlukYarisSonuclari/{t.strftime('%d.%m.%Y')}-{urllib.parse.quote(s)}-GunlukYarisSonuclari-TR.csv"
        try:
            b=urllib.request.urlopen(u,timeout=30).read(); open(fn,'wb').write(b); n+=1
        except urllib.error.HTTPError as e:
            open(fn+'.yok','w').write(str(e.code))
        except Exception as e:
            print('hata',u,e,flush=True)
        time.sleep(0.25)
    if d%10==0: print(d,'gün tamam, dosya:',n,flush=True)
print('BİTTİ',n)
