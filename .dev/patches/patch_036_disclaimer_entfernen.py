#!/usr/bin/env python3
# Patch 036: Redundanten Hinweis am Ende der Rechner-Seite entfernt.
# Onset-Zeit und der Gewaehr-Vorbehalt (individuelle physiologische/
# psychologische Veranlagung) stehen bereits an ausreichend anderen,
# relevanteren Stellen -- dieser pauschale "Schaetzwerte"-Satz ist zudem
# nicht mehr korrekt, da nicht mehr alle Werte reine Schaetzungen sind.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """  <p class="disclaimer">Schätzwerte. Onset: 30–120 Min — immer abwarten.</p>
"""
new1 = ""

if old1 not in content:
    print("WARNUNG 1: Disclaimer-Zeile nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: 'Schätzwerte. Onset: 30–120 Min'-Vermerk entfernt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
