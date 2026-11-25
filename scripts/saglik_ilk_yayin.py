"""Veri sağlık kontrolü (pandera): ilk yayın (ILK_*.csv) AGF'si dolu mu, koşu AGF toplamı ~%100 mü?
Kullanım: saglik_ilk_yayin.py [YYYY-AA-GG ...]   (tarih verilmezse veri/agf_kayit altındaki bütün günler)
Kurulum (yalnızca elle, Actions'a EKLEME): pip install pandera pandas
Kural: ilk yayında atların >=%80'inin AGF'si dolu ve AGF toplamı %90-101. 22.11.2026 testi: 22.11 geçti; 23.11'de 17 koşunun 14'ü, 24.11'de 16'nın 11'i KALDI (kısmi ilk yayın)."""
import re,glob,os,sys
import pandas as pd, pandera.pandas as pa
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def oku(g):
    R=[]
    for p in sorted(glob.glob(os.path.join(K,'veri','agf_kayit',g,'ILK_*.csv'))):
        hip=os.path.basename(p)[4:-4]; k=None
        for l in open(p,encoding='utf-8-sig',errors='replace'):
            m=re.match(r'^(\d+)\. Kosu',l)
            if m: k=int(m.group(1));continue
            pp=l.rstrip('\n').split(';')
            if k and re.match(r'^\d+$',pp[0]) and len(pp)>10 and 'Koşmaz' not in pp[1]:
                v=re.findall(r'%([\d.]+)\(',pp[10]); R.append((g,hip,k,float(v[0]) if v else 0.0))
    d=pd.DataFrame(R,columns=['gun','hip','kosu','agf'])
    if d.empty: return d
    return d.groupby(['gun','hip','kosu']).agg(at=('agf','size'),dolu_oran=('agf',lambda s:(s>0).mean()),toplam=('agf','sum')).reset_index()
SEMA=pa.DataFrameSchema({
    'dolu_oran':pa.Column(float,pa.Check.ge(0.8,error="ilk yayında atların %80'inden azının AGF'si dolu")),
    'toplam':pa.Column(float,pa.Check.in_range(90,101,error='AGF toplamı %90-101 dışında'))},coerce=True)
def main(gunler):
    for g in gunler:
        d=oku(g)
        if d.empty: print(g,': ILK dosyası yok'); continue
        try: SEMA.validate(d,lazy=True); print(f'{g}: GEÇTİ ({len(d)} koşu)')
        except pa.errors.SchemaErrors as e:
            bad=d.loc[e.failure_cases['index'].dropna().astype(int).unique()]
            print(f'{g}: {len(bad)}/{len(d)} koşu KALDI → '+', '.join(f"{r.hip} {r.kosu}. %{r.dolu_oran*100:.0f} dolu" for r in bad.itertuples()))
if __name__=='__main__':
    gun=sys.argv[1:] or sorted(x for x in os.listdir(os.path.join(K,'veri','agf_kayit')) if re.match(r'\d{4}-\d\d-\d\d$',x))
    main(gun)
