#!/usr/bin/env python3
# Patch 4: Kryptisches Label "Extrakt bereits aktiv (100%)" ersetzen
import sys

with open('index.html', encoding='utf-8') as f:
    html = f.read()

old = "'Extrakt bereits aktiv (100%)'"
new = "'Vollst\\u00e4ndige Einarbeitung (~100% Transfer, kein Pflanzenmaterial-Verlust)'"
if new in html:
    print('  [skip] 4: Label bereits ersetzt.')
elif old in html:
    html = html.replace(old, new, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('  [ok]   4: Label ersetzt.')
else:
    sys.exit('  [FAIL] 4: Altes Label nicht gefunden — Pattern prüfen!')
print('Patch 4 geschrieben.')
