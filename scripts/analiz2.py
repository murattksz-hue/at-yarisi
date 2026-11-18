"""Kullanım: analiz2.py program.html program.csv aygir.json [idman.json]
Skor = HP 22 + s20 13 + form 13 + pist uyumu 13 + baba kanı 17 + kısrak babası 8 + galop 14"""
import sys,re,html,json
ph,pc,aj=sys.argv[1:4]; ST=json.load(open(aj,encoding='utf-8'))
import datetime
ID=json.load(open(sys.argv[4],encoding='utf-8')) if len(sys.argv)>4 else {}
def galop(ad,gun):
    d=ID.get(ad)
    if not d: return None,None,'idman yok'
    try: fark=(gun-datetime.datetime.strptime(d['tarih'],'%d.%m.%Y').date()).days
    except: fark=99
    z={int(k):v for k,v in d['zaman'].items()}
    t4=z.get(400) or (z[200]*2.05 if 200 in z else None)
    return t4,fark,f"{d['tur']} {d['pist']} {fark}g önce"+(f" 400m {t4:.1f}sn" if t4 else '')
def txt(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
t=open(ph,encoding='utf-8').read()
ped={}  # at adı -> (baba, anne, kısrak babası, bitiriş)
cells=re.findall(r'gunluk-GunlukYarisProgrami-(AtAdi|Baba)"[^>]*>(.*?)</td>',t,flags=re.S); ad=None
for k,v in cells:
    if k=='AtAdi':
        m=re.search(r'>\s*([^<]+?)\s*<span',v) or re.search(r'>\s*([^<]+?)\s*</a>',v)
        ad=m.group(1).strip() if m else txt(v).split('(')[0].strip()
        b=re.search(r'koşuyu (\d+)\. olarak',v); ped[ad]={'bitis':int(b.group(1)) if b else None}
    elif ad:
        s=txt(v); m=re.match(r'(.+?)\s+-\s+(.+?)\s+/\s+(.+)',s)
        if m: ped[ad].update(baba=m.group(1),anne=m.group(2),kb=m.group(3))
def ae(irk,ayg,key,k=4):
    d=ST.get(irk+'|'+ayg,{}).get(key)
    if not d: return 1.0,0
    return (d['w']+k)/(d['exp']+k), d['n']
def not_(x): return 'A' if x>=1.3 else 'B' if x>=1.05 else 'C' if x>=0.85 else 'D'
races=[];cur=None;gun=None
for l in open(pc,encoding='utf-8-sig').read().splitlines():
    c=l.split(';')
    if gun is None:
        m0=re.search(r'(\d\d)/(\d\d)/(\d{4})',l); gun=datetime.date(int(m0.group(3)),int(m0.group(2)),int(m0.group(1))) if m0 else datetime.date.today()
    if re.match(r'^\d+\. Kosu',c[0]):
        h=l; m=re.search(r'(\d{3,4})m',h); pist=next((p for p in ('Kum','Çim','Sentetik') if p in h),'?')
        mt=int(m.group(1)); b='kisa' if mt<=1400 else ('orta' if mt<=1900 else 'uzun')
        cur=dict(baslik=' '.join(x.strip() for x in c[:6] if x.strip()),pist=pist,bant=b,irk='Arap' if 'Arap' in h else 'İngiliz',atlar=[]);races.append(cur);continue
    if cur and c[0].isdigit() and len(c)>14 and 'Koşmaz' not in c[1]:
        no,isim,yas,baba,anne,kilo,jok=c[:7]; hp,son6,kgs,s20=c[11:15]
        ad=next((a for a in ped if isim.startswith(a)),None); p=ped.get(ad,{})
        form=re.findall(r'([KÇS])(\d)',son6); pc_={'K':'Kum','Ç':'Çim','S':'Sentetik'}
        pts=[(10-int(x)) if x!='0' else 0 for _,x in form]
        pp=[(10-int(x)) if x!='0' else 0 for y,x in form if pc_[y]==cur['pist']]
        bae,bn=ae(cur['irk'],baba.strip(),cur['pist']+'_'+cur['bant']); bg,_=ae(cur['irk'],baba.strip(),'genel')
        kae,_=ae(cur['irk'],p.get('kb',''),'genel')
        cur['atlar'].append(dict(no=no,ad=ad or isim,baba=baba.strip(),kb=p.get('kb','?'),hp=int(hp) if hp.isdigit() else 0,
            s20=int(s20) if s20.isdigit() else 0,form=sum(pts)/len(pts) if pts else 0,pist=(sum(pp)/len(pp)) if pp else (sum(pts)/len(pts)*0.8 if pts else 0),
            bae=bae,bn=bn,bg=bg,kae=kae,bitis=p.get('bitis'),kgs=kgs,g=galop(ad or isim,gun)))
isabet=[0,0,0]
for r in races:
    a=r['atlar']
    if not a: continue
    mx=lambda k:max(x[k] for x in a) or 1
    H,S2,F,P,B,K=mx('hp'),mx('s20'),mx('form'),mx('pist'),mx('bae'),mx('kae')
    t4s=[x['g'][0] for x in a if x['g'][0]]; best=min(t4s) if t4s else None
    for x in a:
        t4,fk,_=x['g']
        hiz=max(0,1-(t4-best)/4) if (t4 and best) else 0.3   # 4 sn geride = 0
        taze=0 if fk is None else 1 if fk<=7 else 0.6 if fk<=14 else 0.3 if fk<=30 else 0
        x['gp']=0.6*hiz+0.4*taze
        x['skor']=round(22*x['hp']/H+13*x['s20']/S2+13*x['form']/F+13*x['pist']/P+17*x['bae']/B+8*x['kae']/K+14*x['gp'],1)
    srt=sorted(a,key=lambda x:-x['skor'])
    print(f"\n=== {r['baslik']}  [{r['irk']}, {r['pist']}, {r['bant']}]")
    for i,x in enumerate(srt[:5]):
        bt=f" → {x['bitis']}." if x['bitis'] else ''
        print(f"  {i+1}) #{x['no']:>2} {x['ad'][:16]:16} baba {x['baba'][:16]:16}({not_(x['bg'])}, pist/mesafe A/E {x['bae']:.2f}, n={x['bn']}) KB {x['kb'][:12]:12}({not_(x['kae'])}) HP{x['hp']:>3} | galop: {x['g'][2]} | SKOR {x['skor']}{bt}")
    w=[x for x in a if x['bitis']==1]
    if w:
        isabet[2]+=1; isabet[0]+=srt[0]['bitis']==1; isabet[1]+=w[0] in srt[:3]
        print(f"  Kazanan: #{w[0]['no']} {w[0]['ad']} (model sırası {srt.index(w[0])+1})")
if isabet[2]: print(f"\nGERİ TEST: {isabet[2]} koşu | 1. seçim kazandı: {isabet[0]} | kazanan ilk 3 seçimde: {isabet[1]}")
