---
name: uyar-push-oncesi
enabled: true
event: bash
pattern: git\s+push
action: warn
---

✅ **Push'tan önce:** tüm betikler sözdizimi kontrolünden geçti mi?
`python3 -I -c "import ast,glob;[ast.parse(open(p,encoding='utf-8').read()) for p in glob.glob('scripts/*.py')]"` ve `python3 -m pytest tests -q`.
(f-string içinde tek tırnak, ör. `A/E'si`, sözdizimini bozar.)
