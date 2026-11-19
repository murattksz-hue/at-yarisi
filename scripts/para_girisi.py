"""Para girişi takibi: bir atın piyasa olasılığının gün içinde nasıl değiştiği (gerçek kayıtlar: veri/agf_kayit/).
Kullanım: para_girisi.py GG.AA.YYYY Hipodrom
Ganyan: ilk ve son kayıttaki 1/ganyan (eküri ayrımı yapılmaz; aynı ganyanı paylaşırlar). AGF: ilk dolu ve son kayıt.
İşaret 💰: ganyandan türeyen olasılık ≥1,5 kat arttı ya da AGF payı ≥1,5 kat arttı (ve son olasılık ≥%5).
NOT: Bu sinyal henüz test edilmedi; olasılığa katılmaz, bilgi olarak gösterilir."""
import sys,os,re,glob,json,datetime
TAGS={'KG','K','DB','SK','SKG','GKR','ÖG','BB','YP','KK','TB','SKK','ÖN','GK','SGKR','KUL','BH','DS'}
def ad_(n):
    t=n.replace('(Koşmaz)','').split()
    while len(t)>1 and t[-1] in TAGS: t.pop()
    return ' '.join(t)
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def hesapla(tarih_iso,hip):
    kd=os.path.join(K,'veri','agf_kayit',tarih_iso); out={}
    G=sorted(glob.glob(os.path.join(kd,f"{hip}_*UTC_ganyan.json")))
    if len(G)>=2:
        g0,g1=json.load(open(G[0],encoding='utf-8')),json.load(open(G[-1],encoding='utf-8'))
        for a in g1:
            if g0.get(a,0)>1 and g1[a]>1: out.setdefault(a,{}).update(ganyan_ilk=g0[a],ganyan_son=g1[a],ganyan_kat=round(g0[a]/g1[a],2),ganyan_saat=(os.path.basename(G[0])[len(hip)+1:len(hip)+5],os.path.basename(G[-1])[len(hip)+1:len(hip)+5]))
    C=sorted(f for f in glob.glob(os.path.join(kd,f"{hip}_*UTC.csv")))
    def agf(f):
        D={}
        for l in open(f,encoding='utf-8-sig'):
            c=l.split(';')
            if re.match(r'^\d+$',c[0]) and len(c)>10:
                m=re.match(r'%([\d.]+)',c[10])
                if m: D[ad_(c[1])]=float(m.group(1))
        return D
    dolu=[f for f in C if agf(f)]
    if len(dolu)>=2:
        a0,a1=agf(dolu[0]),agf(dolu[-1])
        for k in a1:
            if a0.get(k,0)>0: out.setdefault(k,{}).update(agf_ilk=a0[k],agf_son=a1[k],agf_kat=round(a1[k]/a0[k],2))
    for a,v in out.items():
        v['isaret']=(v.get('ganyan_kat',1)>=1.5 and v.get('ganyan_son',99)<=20) or (v.get('agf_kat',1)>=1.5 and v.get('agf_son',0)>=5)
    return out
if __name__=='__main__':
    g=datetime.datetime.strptime(sys.argv[1],'%d.%m.%Y').date(); R=hesapla(g.isoformat(),sys.argv[2])
    for a,v in sorted(R.items(),key=lambda kv:-kv[1].get('ganyan_kat',kv[1].get('agf_kat',1))):
        if v['isaret']: print(f"💰 {a}: ganyan {v.get('ganyan_ilk','?')}→{v.get('ganyan_son','?')} (x{v.get('ganyan_kat','?')}) | AGF %{v.get('agf_ilk','?')}→%{v.get('agf_son','?')}")
    print(f"{sum(v['isaret'] for v in R.values())} at işaretli / {len(R)} at")
