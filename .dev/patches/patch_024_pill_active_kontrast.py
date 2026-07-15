#!/usr/bin/env python3
# Patch L: .pill.on (aktive "Bereiche"-Kachel in Praevention) bekommt feste
# Textfarbe (var(--pp-text)) fuer Label und Beschreibung -- selbes Bugmuster
# wie die Praevention-Hero-Box aus Patch J, hier aber uebersehen.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """.pill .lbl{font-size:var(--fs);font-weight:600}
.pill .dsc{font-size:var(--fs-sm);color:var(--text2);margin-top:2px;line-height:1.4}"""

new1 = """.pill .lbl{font-size:var(--fs);font-weight:600}
.pill .dsc{font-size:var(--fs-sm);color:var(--text2);margin-top:2px;line-height:1.4}
.pill.on .lbl{color:var(--pp-text)}
.pill.on .dsc{color:var(--pp-text);opacity:.75}"""

if old1 not in content:
    print("WARNUNG 1: .pill .lbl/.dsc CSS nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: .pill.on Label & Beschreibung bekommen feste Farbe (var(--pp-text)) — kein Kontrastbruch mehr im Hellmodus.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
