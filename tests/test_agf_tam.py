"""agf_tam testleri: altılı koşu tespiti ve TAM (dolu) AGF kararı. Çalıştır: python3 -m pytest tests -q   (pip install pytest)"""
import os,sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'scripts'))
import agf_tam as T

def csv(kosular,altili_basla=(1,)):
    """kosular: {no: [(ad, agf1)]}; TJK program CSV'sine benzer metin."""
    L=['Test;(1. Yarış Günü);25/11/2026']
    for no,atlar in kosular.items():
        L.append(f'{no}. Kosu :   14.30;Handikap;4 Yaşlı;kg;1400m;Kum;;;;Rekor')
        L.append('At No;At İsmi;Yaş;Baba;Anne;Kilo;Jokey;Sahip;Antrenör;St;AGF;H')
        for i,(ad,agf) in enumerate(atlar,1):
            L.append(f'{i};{ad};3y d e;B;A;58;J;S;T;{i};%{agf}({i})  %0({i});60')
        if no in altili_basla: L.append("[(1)X,] eküridir.%d. 6'LI GANYAN Bu koşudan başlar;1. ÇİFTE Bu koşudan başlar" % (altili_basla.index(no)+1))
    return '\n'.join(L).encode('utf-8')
def yarislar(dolu=True,n=6):
    return {k:[(f'AT{k}{j}',(20.0 if dolu or j==0 else 0)) for j in range(5)] for k in range(1,n+1)}

def test_altili_6_koşu():
    assert T.altili_yarislar(csv(yarislar(),(1,)))==[1,2,3,4,5,6]
def test_iki_altili_birlesir():
    assert T.altili_yarislar(csv(yarislar(n=9),(1,4)))==[1,2,3,4,5,6,7,8,9]
def test_isaret_yoksa_none():
    assert T.altili_yarislar(csv(yarislar(),()))  is None
def test_dolu_tam():
    b=csv(yarislar(dolu=True),(1,)); assert T.tam_tjk(b,T.altili_yarislar(b))
def test_kismi_tam_degil():
    b=csv(yarislar(dolu=False),(1,)); assert not T.tam_tjk(b,T.altili_yarislar(b))   # her koşuda 5 attan yalnızca 1'i dolu
def test_bos_agf_tam_degil():
    K=yarislar(dolu=False); K={k:[(a,0) for a,_ in v] for k,v in K.items()}
    b=csv(K,(1,)); assert not T.tam_tjk(b,T.altili_yarislar(b))
def test_bir_koşu_eksikse_tam_degil():
    K=yarislar(dolu=True); K[3]=[(a,(20.0 if j==0 else 0)) for j,(a,_) in enumerate(K[3])]
    b=csv(K,(1,)); assert not T.tam_tjk(b,T.altili_yarislar(b))
def test_isaretsiz_yedek_kural():       # işaret yoksa AGF'si olan en az 6 koşu ve hepsi dolu olmalı
    b=csv(yarislar(dolu=True),()); assert T.tam_tjk(b,None)
    b5=csv(yarislar(dolu=True,n=5),()); assert not T.tam_tjk(b5,None)
def test_ebayi_tam_ve_kosmaz():
    S={str(k):{f'AT{j}':[('20.5' if True else None),None,'3,0',False] for j in range(5)} for k in range(1,7)}
    S['1']['KOŞMAZ']=[None,None,None,True]                      # koşmaz at sayılmaz
    assert T.tam_ebayi(S,[1,2,3,4,5,6])
    S['2']={f'AT{j}':[(None if j else '20.5'),None,'3,0',False] for j in range(5)}
    assert not T.tam_ebayi(S,[1,2,3,4,5,6])

# --- 26.11: TAM sonrası bekleme ve en son dolu görüntü ---
import datetime,json
def _kd(tmp_path,tjk_tam='0610 UTC',ebayi_tam='0606 UTC'):
    json.dump({'X':{'tjk_tam':tjk_tam,'ebayi_tam':ebayi_tam}},open(tmp_path/'ilk_zaman.json','w'))
    return str(tmp_path)
def test_olgun_bekleme(tmp_path):
    kd=_kd(tmp_path); u=lambda h,m:datetime.datetime(2026,11,26,h,m)
    assert not T.olgun(kd,'X',u(6,24)) and T.olgun(kd,'X',u(6,25))   # geç olan kaynak (06:10) + 15 dk
def test_olgun_saat_yoksa_bekleme_yok(tmp_path):
    assert T.olgun(str(tmp_path),'X',datetime.datetime(2026,11,26,6,0))
def test_en_son_tam_dolu_olani_secer(tmp_path):
    kd=str(tmp_path)
    (tmp_path/'X_0610UTC.csv').write_bytes(csv(yarislar(dolu=True),(1,)))
    (tmp_path/'X_0620UTC.csv').write_bytes(csv(yarislar(dolu=True),(1,)))
    (tmp_path/'X_0630UTC.csv').write_bytes(csv(yarislar(dolu=False),(1,)))   # titreyen/kısmi görüntü atlanmalı
    assert os.path.basename(T.en_son_tam_csv(kd,'X'))=='X_0620UTC.csv'
def test_en_son_tam_yoksa_none(tmp_path):
    assert T.en_son_tam_csv(str(tmp_path),'X') is None
