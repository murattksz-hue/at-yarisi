"""Günlük analiz (v4). Kullanım: analiz3.py program.html program.csv model.json profil.json hipodrom [idman.json]
Olasılık = grup (ırk x zemin x mesafe) özel koşullu logit; galop küçük ek düzeltme (geri test edilmedi)."""
import sys,re,html,json,math,datetime
import numpy as np
ph,pc,mj,pj,HIP=sys.argv[1:6]; M=json.load(open(mj,encoding='utf-8')); PR=json.load(open(pj,encoding='utf-8'))
ID=json.load(open(sys.argv[6],encoding='utf-8')) if len(sys.argv)>6 else {}
def bant(m): return 'kisa' if m<=1400 else ('orta' if m<=1900 else 'uzun')
def kova(s): return '1-3' if s<=3 else '4-6' if s<=6 else '7-9' if s<=9 else '10+'
def txt(x): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
def ae(D,k,pr=4): s=D.get(k,[0,0.0]); return (s[0]+pr)/(s[1]+pr)
t=open(ph,encoding='utf-8').read(); ped={}; ad=None
for k,v in re.findall(r'gunluk-GunlukYarisProgrami-(AtAdi|Baba)"[^>]*>(.*?)</td>',t,flags=re.S):
    if k=='AtAdi':
        m=re.search(r'>\s*([^<]+?)\s*<span',v) or re.search(r'>\s*([^<]+?)\s*</a>',v); ad=m.group(1).strip() if m else txt(v).split('(')[0].strip()
        b=re.search(r'koşuyu (\d+)\. olarak',v); ped[ad]={'bitis':int(b.group(1)) if b else None}
    elif ad:
        m=re.match(r'(.+?)\s+-\s+(.+?)\s+/\s+(.+)',txt(v))
        if m: ped[ad]['kb']=m.group(3)
PC={'K':'Kum','Ç':'Çim','S':'Sentetik'}; races=[];cur=None;gun=None
for l in open(pc,encoding='utf-8-sig').read().splitlines():
    c=l.split(';')
    if gun is None:
        m0=re.search(r'(\d\d)/(\d\d)/(\d{4})',l); gun=datetime.date(int(m0.group(3)),int(m0.group(2)),int(m0.group(1))) if m0 else datetime.date.today()
    if re.match(r'^\d+\. Kosu',c[0]):
        m=re.search(r'(\d{3,4})m',l); pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?')
        cur=dict(bas=' '.join(x.strip() for x in c[:6] if x.strip()),irk='Arap' if 'Arap' in l else 'İngiliz',pist=pist,bant=bant(int(m.group(1))),h=[]);races.append(cur);continue
    if cur and c[0].isdigit() and len(c)>14 and 'Koşmaz' not in c[1]:
        ag=re.match(r'%([\d.]+)',c[10]); y=re.match(r'(\d+)y',c[2]); kg=re.match(r'([\d,]+)',c[5]); st=re.match(r'(\d+)',c[9])
        isim=c[1]; a=next((k for k in sorted(ped,key=len,reverse=True) if isim.startswith(k)),isim)
        cur['h'].append(dict(no=c[0],ad=a,baba=c[3].strip(),hp=int(c[11]) if c[11].isdigit() else 0,son6=c[12],kgs=int(c[13]) if c[13].isdigit() else 0,
            s20=int(c[14]) if c[14].isdigit() else 0,agf=float(ag.group(1)) if ag else 0.5,yas=int(y.group(1)) if y else 4,kg=float(kg.group(1).replace(',','.')) if kg else 57,
            ap=' AP' in c[6],st=int(st.group(1)) if st else 0,jok=c[6],kb=ped.get(a,{}).get('kb','?'),bitis=ped.get(a,{}).get('bitis')))
def galop(ad):
    d=ID.get(ad)
    if not d: return None,None,'idman yok'
    try: fk=(gun-datetime.datetime.strptime(d['tarih'],'%d.%m.%Y').date()).days
    except: fk=99
    z={int(k):v for k,v in d['zaman'].items()}; t4=z.get(400) or (z[200]*2.05 if 200 in z else None)
    return t4,fk,f"{d['tur']} {d['pist']} {fk}g"+(f" 400m {t4:.1f}" if t4 else '')
not_=lambda x:'A' if x>=1.3 else 'B' if x>=1.05 else 'C' if x>=0.85 else 'D'
sk=[0,0,0]
for r in races:
    h=r['h']
    if len(h)<2: continue
    seg=f"{r['irk']}|{r['pist']}|{r['bant']}"; W=np.array(M['grup'].get(seg,M['genel']))
    X=[]
    for x in h:
        fm=re.findall(r'([KÇS])(\d)',x['son6']); pts=[(10-int(q)) if q!='0' else 0 for _,q in fm]
        pp=[(10-int(q)) if q!='0' else 0 for y,q in fm if PC[y]==r['pist']]
        form=sum(pts)/len(pts) if pts else 3; pf=sum(pp)/len(pp) if pp else form*0.8
        x['bae']=ae(M['aygir'],f"{r['irk']}|{x['baba']}|{r['pist']}_{r['bant']}"); x['bg']=ae(M['aygir'],f"{r['irk']}|{x['baba']}|genel"); x['kbg']=ae(M['aygir'],f"{r['irk']}|{x['kb']}|genel")
        x['ku']=ae(M['kulvar'],f"{HIP}|{r['pist']}|{r['bant']}|{kova(x['st'])}",pr=10)
        X.append([x['hp'],x['s20'],form,pf,math.log(x['bae']),math.log(x['ku']),math.log(max(x['agf'],0.3)),float(x['kgs']>60),float(x['ap']),x['yas'],x['kg']])
    X=np.array(X,float); sd=X.std(0); sd[sd==0]=1; Z=(X-X.mean(0))/sd; Z[:,6]=X[:,6]-X[:,6].mean()
    u=Z@W
    g=[galop(x['ad']) for x in h]; t4=[a for a,_,_ in g if a]; best=min(t4) if t4 else None
    gp=np.array([0.6*(max(0,1-(a-best)/4) if a and best else 0.3)+0.4*(0 if fk is None else 1 if fk<=7 else .6 if fk<=14 else .3 if fk<=30 else 0) for a,fk,_ in g])
    u=u+0.5*(gp-gp.mean())   # galop düzeltmesi (küçük)
    p=np.exp(u-u.max()); p/=p.sum(); q=np.array([x['agf'] for x in h]); q=q/q.sum()
    pro=PR['segment'].get(seg,{}); a_=pro.get('ae',{}); ic=a_.get('start 1-3',{}).get('piyasa_ae')
    print(f"\n=== {r['bas']}  [{seg}]")
    print(f"    Grup profili: favori %{pro.get('favori_kazanma','?')} kazanıyor, ort. {pro.get('ort_alan','?')} at; iç kulvar (1-3) piyasaya göre {ic}")
    srt=np.argsort(-p)
    for i in srt[:5]:
        x=h[i]; deger=p[i]/q[i] if q[i] else 0; isaret=' ★DEĞER' if deger>=1.3 and p[i]>=0.08 else ''
        bt=f" → {x['bitis']}." if x['bitis'] else ''
        print(f"  #{x['no']:>2} {x['ad'][:16]:16} olasılık %{100*p[i]:4.1f} (adil oran {1/p[i]:5.1f}) AGF %{100*q[i]:4.1f}{isaret} | baba {x['baba'][:13]} {not_(x['bg'])}/{x['bae']:.2f} KB {x['kb'][:11]} {not_(x['kbg'])} | st {x['st']} | {g[i][2]}{bt}")
    kaz=[i for i,x in enumerate(h) if x['bitis']==1]
    if kaz: sk[2]+=1; sk[0]+=srt[0]==kaz[0]; sk[1]+=kaz[0] in srt[:3]
if sk[2]: print(f"\nBugün biten koşular: {sk[2]} | 1. seçim kazandı {sk[0]} | kazanan ilk 3'te {sk[1]}")
