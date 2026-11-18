"""Kullanım: idman.py program.html cikti.json  -> at adı: son idman bilgisi"""
import sys,re,html,json,time,subprocess
t=open(sys.argv[1],encoding="utf-8").read(); ERA=sys.argv[3] if len(sys.argv)>3 else "today"
kodlar=sorted(set(re.findall(r'tabshipodromSemasi-(\d+)',t)))
MES=[2200,2000,1800,1600,1400,1200,1000,800,600,400,200]
def sn(x):
    m=re.match(r'(\d+)\.(\d+)\.(\d+)',x); return int(m.group(1))*60+int(m.group(2))+int(m.group(3))/100 if m else None
out={}
for k in kodlar:
    u=f"https://www.tjk.org/TR/YarisSever/Info/Karsilastirma/Karsilastirma?KosuKodu={k}&Era={ERA}&KTip=5"
    for deneme in range(3):
        h=subprocess.run(['curl','-sS','--max-time','90',u],capture_output=True).stdout.decode('utf-8','replace'); time.sleep(2)
        if 'At Adı' in h: break
    else: print('alınamadı',k,flush=True)
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>',h,flags=re.S):
        td=[re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>',tr,flags=re.S)]
        if len(td)<18 or not td[0].isdigit(): continue
        z={m:sn(v) for m,v in zip(MES,td[2:13]) if sn(v)}
        out[td[1]]=dict(kosu=k,zaman=z,tarih=td[13],pist=td[14],durum=td[15],tur=td[16],hipodrom=td[17],jokey=td[18] if len(td)>18 else '')
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(kodlar),'koşu,',len(out),'at')
