#!/usr/bin/env python3
# Patch 053: "Frauen" -> "Personen weiblichen Geschlechts" -- praeziser
# (es geht um biologisches Geschlecht, nicht Gender) und inklusiver
# formuliert.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """    kgEl.innerHTML = '~2.5 mg <span style="font-size:11px;color:var(--text3)">Delta-9-THC aufgenommen · oral wirksam als 11-OH · bis ~5 mg langsam steigern<br>empfindliche Personen (tendenziell Frauen) tiefer ansetzen</span>';"""

new1 = """    kgEl.innerHTML = '~2.5 mg <span style="font-size:11px;color:var(--text3)">Delta-9-THC aufgenommen · oral wirksam als 11-OH · bis ~5 mg langsam steigern<br>empfindliche Personen (tendenziell weiblichen Geschlechts) tiefer ansetzen</span>';"""

if old1 not in content:
    print("WARNUNG 1: Startdosis-Hinweiszeile nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: 'Frauen' -> 'weiblichen Geschlechts' präzisiert.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
