#!/usr/bin/env python3
# Patch 055: Der kleine Erklaertext unter der Startdosis-Zahl war ein
# inline <span> innerhalb desselben .rv-Elements wie die grosse 21px-Zahl.
# Ohne eigene Zeilenhoehe vermischten sich die Zeilenboxen der 21px- und
# 11px-Schrift beim Zeilenumbruch -- das erzeugte ein unruhiges,
# ungleichmaessiges Erscheinungsbild ("Buchstaben weit auseinander,
# komische Absaetze"). Fix: eigener Block (<div>) mit fester, kompakter
# Zeilenhoehe, komplett getrennt von der grossen Zahl.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """    kgEl.innerHTML = '~2.5 mg <span style="font-size:11px;color:var(--text3)">Delta-9-THC aufgenommen · oral wirksam als 11-OH · bis ~5 mg langsam steigern<br>empfindliche Personen (tendenziell weiblichen Geschlechts) tiefer ansetzen</span>';"""

new1 = """    kgEl.innerHTML = '~2.5 mg<div style="display:block;font-size:11px;font-weight:400;color:var(--text3);line-height:1.5;margin-top:4px">Delta-9-THC aufgenommen · oral wirksam als 11-OH · bis ~5 mg langsam steigern<br>empfindliche Personen (tendenziell weiblichen Geschlechts) tiefer ansetzen</div>';"""

if old1 not in content:
    print("WARNUNG 1: Startdosis-Hinweiszeile nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Erklärtext als eigenen Block mit fester Zeilenhöhe abgesetzt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
