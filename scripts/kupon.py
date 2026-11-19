"""Çoklu ganyan (5'li/6'lı/7'li) kuponu ve ikili olasılıkları. Kullanım: kupon.py analiz.json [birim_fiyat_TL] [butce_TL]
Olasılıklar analiz3'ün modelinden gelir. Kupon: her adımda (isabet olasılığı artışı / maliyet artışı) en iyi olan at eklenir.
İkili: Harville formülü P(i 1., j 2.) = p_i * p_j / (1 - p_i). (Literatür: Harville sürprizlerin 2.liğini biraz abartır.)"""
import sys,json,math
A=json.load(open(sys.argv[1],encoding='utf-8')); birim=float(sys.argv[2]) if len(sys.argv)>2 else 1.0; butce=float(sys.argv[3]) if len(sys.argv)>3 else 500.0
def birimler(k):   # eküri: tek bahis birimi
    U=[];ek=[a for a in k['atlar'] if a['ekuri']]
    if ek: U.append(dict(ad='+'.join(a['ad'] for a in ek),no='/'.join(a['no'] for a in ek),p=sum(a['p'] for a in ek)))
    U+= [dict(ad=a['ad'],no=a['no'],p=a['p']) for a in k['atlar'] if not a['ekuri']]
    return sorted(U,key=lambda u:-u['p'])
for i,k in enumerate(A):
    for n in k['coklu_ganyan_baslar']:
        ayak=A[i:i+n]
        if len(ayak)<n: continue
        B=[birimler(x) for x in ayak]; sec=[[b[0]] for b in B]
        maliyet=lambda S:birim*math.prod(len(x) for x in S); isabet=lambda S:math.prod(sum(u['p'] for u in x) for x in S)
        while True:
            en=None
            for j in range(n):
                kalan=[u for u in B[j] if u not in sec[j]]
                if not kalan: continue
                T=[x[:] for x in sec]; T[j].append(kalan[0])
                if maliyet(T)>butce: continue
                kaz=(isabet(T)-isabet(sec))/(maliyet(T)-maliyet(sec))
                if en is None or kaz>en[0]: en=(kaz,T)
            if not en: break
            sec=en[1]
        print(f"\n=== {n}'li ganyan ({ayak[0]['kosu']}. koşudan) | birim {birim} TL, bütçe {butce} TL")
        for j,x in enumerate(sec):
            print(f"  {j+1}. ayak ({ayak[j]['kosu']}. koşu): "+', '.join(f"{u['no']} {u['ad']} %{100*u['p']:.0f}" for u in x)+f"  → ayak kapsama %{100*sum(u['p'] for u in x):.0f}")
        print(f"  Kupon: {math.prod(len(x) for x in sec)} kombinasyon = {maliyet(sec):.0f} TL | modele göre isabet olasılığı %{100*isabet(sec):.1f}"
              +("  (AGF'siz model: daha belirsiz)" if any(a['agf_yok'] for a in ayak) else ''))
print("\nİkili / sıralı ikili (Harville, en olası 3):")
for k in A:
    U=birimler(k); C=[]
    for a in U:
        for b in U:
            if a is not b and a['p']<1: C.append((a['p']*b['p']/(1-a['p']),a,b))
    C.sort(key=lambda c:-c[0]); ik={}
    for pr,a,b in C: key=tuple(sorted([a['no'],b['no']])); ik[key]=ik.get(key,0)+pr
    top=sorted(ik.items(),key=lambda kv:-kv[1])[:3]
    print(f"  {k['kosu']}. koşu: sıralı "+'; '.join(f"{a['no']}-{b['no']} %{100*pr:.1f}" for pr,a,b in C[:3])+" | ikili "+'; '.join(f"{'/'.join(kk)} %{100*v:.1f}" for kk,v in top))
