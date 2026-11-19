"""Program HTML'inden her atın soyunu (baba, anne, anne babası) kalıcı kayda ekler. Kullanım: soy_kayit.py program.html [kayit.json]
Kayıt: veri/soy_kayit.json -> 'at adı' -> {baba, anne, anne_babasi, ilk_gorulme}"""
import sys,os,re,json,html,datetime
K=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); J=sys.argv[2] if len(sys.argv)>2 else os.path.join(K,'veri','soy_kayit.json')
D=json.load(open(J,encoding='utf-8')) if os.path.exists(J) else {}
t=open(sys.argv[1],encoding='utf-8').read(); ad=None; yeni=0
txt=lambda x:re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x))).strip()
for k,v in re.findall(r'gunluk-GunlukYarisProgrami-(AtAdi|Baba)"[^>]*>(.*?)</td>',t,flags=re.S):
    if k=='AtAdi':
        m=re.search(r'>\s*([^<]+?)\s*<span',v) or re.search(r'>\s*([^<]+?)\s*</a>',v); ad=m.group(1).strip() if m else None
    elif ad:
        m=re.match(r'(.+?)\s+-\s+(.+?)\s+/\s+(.+)',txt(v))
        if m and ad not in D:
            D[ad]=dict(baba=m.group(1),anne=m.group(2),anne_babasi=m.group(3),ilk_gorulme=datetime.date.today().isoformat()); yeni+=1
json.dump(D,open(J,'w'),ensure_ascii=False)
print(f"soy kaydı: {yeni} yeni at, toplam {len(D)}")
