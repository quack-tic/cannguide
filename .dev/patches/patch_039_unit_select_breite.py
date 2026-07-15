#!/usr/bin/env python3
# Patch 039: Regressions-Fix aus Patch 038 -- das neue <select> fuer die
# Einheit (g/kg, ml/l) hatte keine feste Breite und verdraengte das
# eigentliche Zahlen-Eingabefeld. Fix: feste, kompakte Breite fuers Select.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """select.unit-badge{-webkit-appearance:none;appearance:none;font-family:inherit}"""
new1 = """select.unit-badge{-webkit-appearance:none;appearance:none;font-family:inherit;flex:0 0 62px;width:62px}"""

if old1 not in content:
    print("WARNUNG 1: select.unit-badge CSS nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Einheiten-Select hat jetzt feste Breite (62px) — Zahlenfeld bleibt lesbar.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
