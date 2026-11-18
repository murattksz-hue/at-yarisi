"""Geri test: sonuc/ (sonuç CSV) + program/ (program CSV). Her gün için aygır istatistiği
yalnızca o günden ÖNCEKİ sonuçlardan hesaplanır (sızıntı yok).
v1 = HP40 s20 30 form30 ; v2 = HP25 s20 15 form15 pist15 baba-kanı20 (KB programda yok)."""
import sys,glob,os,re,collections
SD,PD=sys.argv[1:3]
def bant(m): return 'kisa' if m<=1400 else ('orta' if m<=1900 else 'uzun')
def kosular(f,sonuc):
    out=[];cur=None
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]):
            m=re.search(r'(\d{3,4})m',l)
            cur=dict(no=c[0].split('.')[0],irk='Arap' if 'Arap' in l else 'İngiliz',pist=next((p for p in ('Kum','Çim','Sentetik') if p in l),'?'),bant=bant(int(m.group(1))) if m else '?',atlar=[]);out.append(cur);continue
        if cur and c[0].isdigit() and len(c)>13:
            if sonuc:
                try:o=float(c[13].replace(',','.'))
                except:o=0
                cur['atlar'].append(dict(pos=int(c[0]) if c[12].strip() else 99,ad=c[1].split(' ')[0:3],isim=c[1],baba=c[3].strip(),o=o))
            elif len(c)>14 and 'Koşmaz' not in c[1]:
                cur['atlar'].append(dict(agf=float(re.match(r'%([\d.]+)',c[10]).group(1)) if re.match(r'%([\d.]+)',c[10]) else 0,isim=c[1],baba=c[3].strip(),hp=int(c[11]) if c[11].isdigit() else 0,son6=c[12],s20=int(c[14]) if c[14].isdigit() else 0))
    return out
files=sorted(glob.glob(SD+'/*.csv'))
S=collections.defaultdict(lambda:collections.defaultdict(lambda:[0,0,0.0]))
def ekle(r):
    n=len(r['atlar'])
    for x in r['atlar']:
        for k in ('genel',r['pist']+'_'+r['bant']):
            s=S[r['irk']+'|'+x['baba']][k]; s[0]+=1; s[1]+=x['pos']==1; s[2]+=1/n
def ae(irk,b,k):
    s=S.get(irk+'|'+b,{}).get(k); return (s[1]+4)/(s[2]+4) if s else 1.0
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def norm(n):
    t=n.split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
PC={'K':'Kum','Ç':'Çim','S':'Sentetik'}
res={'v3 (v2+AGF)':[0,0,0,0.0],'AGF favorisi':[0,0,0,0.0],'v1':[0,0,0,0.0],'v2':[0,0,0,0.0]}  # koşu, top1, top3, ganyan getirisi (1 TL/koşu)
gunler=sorted(set(os.path.basename(f)[:10] for f in files)); test=gunler[-int(sys.argv[3]):]
for g in gunler:
    gf=[f for f in files if os.path.basename(f).startswith(g)]
    if g in test:
        for f in gf:
            pf=os.path.join(PD,os.path.basename(f))
            if not os.path.exists(pf): continue
            P={r['no']:r for r in kosular(pf,False)}
            for r in kosular(f,True):
                p=P.get(r['no']); w=[x for x in r['atlar'] if x['pos']==1]
                if not p or not w or len(p['atlar'])<4: continue
                a=p['atlar']
                for x in a:
                    fm=re.findall(r'([KÇS])(\d)',x['son6']); pts=[(10-int(q)) if q!='0' else 0 for _,q in fm]
                    pp=[(10-int(q)) if q!='0' else 0 for y,q in fm if PC[y]==p['pist']]
                    x['form']=sum(pts)/len(pts) if pts else 0; x['pf']=sum(pp)/len(pp) if pp else x['form']*0.8
                    x['bae']=ae(p['irk'],x['baba'],p['pist']+'_'+p['bant'])
                mx=lambda k:max(x[k] for x in a) or 1
                for x in a:
                    x['v1']=40*x['hp']/mx('hp')+30*x['s20']/mx('s20')+30*x['form']/mx('form')
                    x['v2']=25*x['hp']/mx('hp')+15*x['s20']/mx('s20')+15*x['form']/mx('form')+15*x['pf']/mx('pf')+20*x['bae']/mx('bae')
                kaz=norm(w[0]['isim'])
                for x in a: x['AGF favorisi']=x['agf']; x['v3 (v2+AGF)']=0.5*x['v2']/mx('v2')+0.5*x['agf']/mx('agf')
                for v in ('AGF favorisi','v1','v2','v3 (v2+AGF)'):
                    srt=sorted(a,key=lambda x:-x[v]); top=[norm(x['isim']) for x in srt]
                    R=res[v]; R[0]+=1; R[1]+=top[0]==kaz; R[2]+=kaz in top[:3]
                    if top[0]==kaz: R[3]+=w[0]['o']
    for f in gf:
        for r in kosular(f,True): ekle(r)
for v,R in res.items():
    if R[0]: print(f"{v}: {R[0]} koşu | 1. seçim kazandı %{100*R[1]/R[0]:.1f} | kazanan ilk 3'te %{100*R[2]/R[0]:.1f} | 1. seçime ganyan getirisi %{100*R[3]/R[0]:.0f} (100=başabaş)")
