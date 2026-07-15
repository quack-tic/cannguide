#!/usr/bin/env python3
# Patch 052 (zusammengefuehrt): Startdosis-Hinweis verstaendlicher gemacht.
# 1) "langsam titrieren" -> "langsam steigern" (Fachbegriff durch
#    allgemeinverstaendliche Formulierung ersetzt)
# 2) "(tendenziell ♀)" -> "(tendenziell weiblichen Geschlechts)" -- das
#    Unicode-Symbol rendert auf manchen Geraeten kaum sichtbar, und es geht
#    um biologisches Geschlecht (nicht Gender) -- ausgeschrieben eindeutig.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """    kgEl.innerHTML = '~2.5 mg <span style="font-size:11px;color:var(--text3)">Delta-9-THC aufgenommen · oral wirksam als 11-OH · bis ~5 mg langsam titrieren<br>empfindliche Personen (tendenziell ♀) tiefer ansetzen</span>';"""

new1 = """    kgEl.innerHTML = '~2.5 mg <span style="font-size:11px;color:var(--text3)">Delta-9-THC aufgenommen · oral wirksam als 11-OH · bis ~5 mg langsam steigern<br>empfindliche Personen (tendenziell weiblichen Geschlechts) tiefer ansetzen</span>';"""

if old1 not in content:
    print("WARNUNG 1: Startdosis-Hinweiszeile nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: 'titrieren' -> 'steigern', '♀' -> 'weiblichen Geschlechts' ausgeschrieben.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
