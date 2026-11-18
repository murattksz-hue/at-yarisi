"""Jokey piyasa A/E'si kalıcı mı? İlk yarı (eski 90 gün) ile ikinci yarı karşılaştırılır."""
import sys,glob,os,re,collections
A=[collections.defaultdict(lambda:[0,0.0,0]) for _ in range(2)]
fs=sorted(glob.glob(sys.argv[1]+'/*.csv')); orta=sorted(set(os.path.basename(f)[:10] for f in fs)); orta=orta[len(orta)//2]
for f in fs:
    yari=int(os.path.basename(f)[:10]>=orta); cur=None; rs=[]
    for l in open(f,encoding='utf-8-sig').read().splitlines():
        c=l.split(';')
        if re.match(r'^\d+\. Kosu',c[0]): cur=[]; rs.append(cur); continue
        if cur is not None and c[0].isdigit() and len(c)>13:
            try:o=float(c[13].replace(',','.'))
            except:o=0
            cur.append((int(c[0]) if c[12].strip() else 99,o,c[6].replace(' AP','').strip()))
    for h in rs:
        oo=[x for x in h if x[1]>1]; tot=sum(1/x[1] for x in oo) or 1
        if len(h)<4: continue
        for pos,o,j in h:
            if o>1: a=A[yari][j]; a[0]+=pos==1; a[1]+=(1/o)/tot; a[2]+=1
ort=[j for j in A[0] if A[0][j][2]>=80 and A[1][j][2]>=80]
import statistics
x=[A[0][j][0]/A[0][j][1] for j in ort]; y=[A[1][j][0]/A[1][j][1] for j in ort]
print('jokey sayısı',len(ort),'| ilk yarı A/E ile ikinci yarı A/E korelasyonu:',round(statistics.correlation(x,y),2))
iyi=[j for j in ort if A[0][j][0]/A[0][j][1]>=1.2]; kotu=[j for j in ort if A[0][j][0]/A[0][j][1]<=0.8]
for ad,g in (('ilk yarıda iyi (>=1.2)',iyi),('ilk yarıda kötü (<=0.8)',kotu)):
    w=sum(A[1][j][0] for j in g); e=sum(A[1][j][1] for j in g)
    print(f"{ad}: {len(g)} jokey -> ikinci yarıda toplam piyasa A/E {w/e:.2f}")
