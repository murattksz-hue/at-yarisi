import glob,os,urllib.parse,subprocess,time,datetime,sys
sd,pd,gun=sys.argv[1],sys.argv[2],int(sys.argv[3]); os.makedirs(pd,exist_ok=True)
lim=(datetime.date(2026,11,18)-datetime.timedelta(days=gun)).isoformat(); n=0
for f in sorted(glob.glob(sd+'/*.csv'),reverse=True):
    b=os.path.basename(f); g,s=b[:10],b[11:-4]
    if g<lim: continue
    out=os.path.join(pd,b)
    if os.path.exists(out): continue
    d=datetime.date.fromisoformat(g)
    u=f"https://medya-cdn.tjk.org/raporftp/TJKPDF/{d.year}/{g}/CSV/GunlukYarisProgrami/{d.strftime('%d.%m.%Y')}-{urllib.parse.quote(s)}-GunlukYarisProgrami-TR.csv"
    r=subprocess.run(['curl','-sS','-f','--max-time','60','-o',out,u]); n+=r.returncode==0; time.sleep(0.3)
    if n%50==0 and r.returncode==0: print(n,flush=True)
print('BİTTİ',n,flush=True)
