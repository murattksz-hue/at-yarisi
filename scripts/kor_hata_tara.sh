#!/usr/bin/env bash
# Kör hata yutma taraması (ast-grep, yalnızca okur): pip install ast-grep-cli
# Kullanım: bash scripts/kor_hata_tara.sh
cd "$(dirname "$0")/.." || exit 1
echo "== çıplak except =="; ast-grep run -l python -p $'try:\n    $$$A\nexcept:\n    $$$B' scripts | grep -c '^scripts'
echo "== except Exception (dosya başına) =="
ast-grep scan --inline-rules $'id: x\nlanguage: python\nrule:\n  kind: except_clause\n  has:\n    kind: identifier\n    regex: ^Exception$\n    stopBy: neighbor' scripts --json=compact | python3 -c "
import json,sys,collections
c=collections.Counter(x['file'] for x in json.load(sys.stdin))
for f,n in c.most_common(): print(n,f)"
echo "== subprocess.run check'siz =="
ast-grep run -l python -p 'subprocess.run($$$A)' scripts --json=compact | python3 -c "
import json,sys,collections
c=collections.Counter(x['file'] for x in json.load(sys.stdin) if 'check=' not in x['text'])
for f,n in c.most_common(): print(n,f)"
echo "== open() encoding'siz (Türkçe karakter riski; ikili 'rb'/'wb' hariç) =="
{ ast-grep run -l python -p 'open($F)' scripts --json=compact; ast-grep run -l python -p 'open($F,$M)' scripts --json=compact; } | python3 -c "
import json,sys,collections
c=collections.Counter()
for blk in sys.stdin.read().replace(']\n[',']\0[').split('\0'):
    for x in json.loads(blk or '[]'):
        if 'encoding' not in x['text'] and not any(q in x['text'] for q in ('\"rb\"',\"'rb'\",'\"wb\"',\"'wb'\")): c[x['file']]+=1
for f,n in c.most_common(10): print(n,f)"
echo "== json.load(open(...)) dosyayı kapatmıyor =="; ast-grep run -l python -p 'json.load(open($F))' scripts | grep '^scripts' | cut -d: -f1 | sort | uniq -c
echo "== curl --max-time'sız =="; grep -n curl scripts/*.py | grep -v max-time | head
