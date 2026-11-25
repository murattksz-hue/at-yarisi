"""Gerçek kayıtlar üzerinde biçim/sağlık testleri (ayrıştırıcı ve kaynak biçimi değişirse hemen fark edilsin). Çalıştır: python3 -m pytest tests -q
Kayıt yoksa test atlanır. Kurallar: eBayi JSON satırı [agf1, agf2, ganyan, koşmaz]; koşuda 3-20 at; TAM kayıtta AGF toplamı %85-101; ganyan 1-1000 ya da boş (999.99 yer tutucu kabul)."""
import os,sys,glob,json,re
import pytest
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(K,'scripts'))
import agf_tam as T
EB=sorted(glob.glob(os.path.join(K,'veri','agf_kayit','2026-*','*UTC_ebayi.json')))[-40:]
TAM=sorted(glob.glob(os.path.join(K,'veri','agf_kayit','2026-*','TAM_*_ebayi.json')))[-10:]
TJK=sorted(glob.glob(os.path.join(K,'veri','agf_kayit','2026-*','TAM_*.csv')))[-10:]
def f(v):
    try: return float(str(v).replace(',','.'))
    except Exception: return None
@pytest.mark.skipif(not EB,reason='kayıt yok')
@pytest.mark.parametrize('yol',EB)
def test_ebayi_bicim(yol):
    d=json.load(open(yol,encoding='utf-8'))
    assert d
    for no,atlar in d.items():
        assert no.isdigit() and 3<=len(atlar)<=20,(yol,no,len(atlar))
        for ad,v in atlar.items():
            assert len(v)==4 and isinstance(v[3],bool),(yol,no,ad,v)
            g=f(v[2]); assert g is None or 1<=g<=1000,(yol,no,ad,g)
@pytest.mark.skipif(not TAM,reason='TAM kayıt yok')
@pytest.mark.parametrize('yol',TAM)
def test_tam_ebayi_toplam(yol):
    d=json.load(open(yol,encoding='utf-8')); yar=T.altili_yarislar_ebayi(d) if hasattr(T,'altili_yarislar_ebayi') else None
    assert T.tam_ebayi(d,yar)
    for no,atlar in d.items():
        s=sum(f(v[0]) or 0 for v in atlar.values())
        if s>0: assert 85<=s<=101,(yol,no,s)
@pytest.mark.skipif(not TJK,reason='TAM TJK kayıt yok')
@pytest.mark.parametrize('yol',TJK)
def test_tam_tjk_altili(yol):
    b=open(yol,'rb').read(); yar=T.altili_yarislar(b)
    assert yar and len(yar)>=6
    assert T.tam_tjk(b,yar)
