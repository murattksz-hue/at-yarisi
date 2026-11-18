import sys,re
rows=open(sys.argv[1],encoding='utf-8-sig').read().splitlines()
races=[];cur=None
for l in rows:
    c=l.split(';')
    if re.match(r'^\d+\. Kosu',c[0]):
        cur={'baslik':' '.join(x.strip() for x in c if x.strip()),'atlar':[]};races.append(cur);continue
    if cur and c[0].isdigit() and len(c)>14:
        no,isim,yas,baba,anne,kilo,jok,sah,ant,st,agf,hp,son6,kgs,s20=c[:15]
        m=re.match(r'%([\d.]+)',agf); agfp=float(m.group(1)) if m else 0
        form=re.findall(r'([KÇS])(\d)',son6)
        # son 6: 0 => 10+ / derece yok
        fpts=[ (10-int(p)) if p!='0' else 0 for _,p in form]
        kum=[int(p) for y,p in form if y=='K' and p!='0']
        cur['atlar'].append(dict(no=no,isim=re.sub(r'\s+(KG|K|DB|SK|SKG|GKR|ÖG|BB|YP|KK|TB|SKK|ÖN)\b','',isim).strip(),yas=yas,kilo=kilo,jok=jok,ant=ant,st=st,agf=agfp,hp=int(hp) if hp.isdigit() else 0,son6=son6,kgs=kgs,s20=int(s20) if s20.isdigit() else 0,formort=sum(fpts)/len(fpts) if fpts else 0))
for r in races:
    a=r['atlar']
    if not a: continue
    mhp=max(x['hp'] for x in a) or 1; ms20=max(x['s20'] for x in a) or 1
    for x in a:
        x['skor']=round(40*x['hp']/mhp+30*x['s20']/ms20+30*x['formort']/9,1)
    print('\n=== '+r['baslik'][:110])
    for x in sorted(a,key=lambda x:-x['skor'])[:5]:
        print(f"  #{x['no']:>2} {x['isim'][:18]:18} {x['yas']:8} {x['kilo']:>10} {x['jok']:12} HP{x['hp']:>3} s20:{x['s20']:>2} son6:{x['son6']:14} KGS:{x['kgs']:>3} AGF%{x['agf']:5.1f} SKOR {x['skor']}")
