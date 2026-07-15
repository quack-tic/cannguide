#!/usr/bin/env python3
# Patch P: Neue Reihenfolge der 4 Praevention-Regeln:
# Position 1 = alte Regel 4 (Informationen suchen)
# Position 2 = alte Regel 3 (Umfeld beachten)
# Position 3 = alte Regel 1 (Niedrig starten)
# Position 4 = alte Regel 2 (Geduld haben)
# Nummern-Badges werden entsprechend korrekt auf 1-4 neu gesetzt.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """    +'<div class="pp-rule"><span class="n">1</span><div><b>Niedrig starten.</b> <span class="tx">Erste Erfahrung max. 2.5–5&nbsp;mg THC pro Konsumeinheit.</span></div></div>'
    +'<div class="pp-rule"><span class="n">2</span><div><b>Geduld haben.</b> <span class="tx">Wirkung erst nach 30–120&nbsp;Min. Niemals nachlegen, weil „nichts passiert“.</span></div></div>'
    +'<div class="pp-rule"><span class="n">3</span><div><b>Umfeld beachten.</b> <span class="tx">Vertraute Umgebung, kein Alkohol, keine Medikamente, nicht am Steuer, nie Konsumieren in anwesenheit von Minderjährigen.</span></div></div>'
    +'<div class="pp-rule"><span class="n">4</span><div><b>Informationen suchen.</b> <span class="tx">Vertraue deinen Instinkten, aber informiere dich über Wirkung, Dauer und Kontraindikationen wie z.B Medikamente oder Vorerkrankungen.</span></div></div>'"""

new1 = """    +'<div class="pp-rule"><span class="n">1</span><div><b>Informationen suchen.</b> <span class="tx">Vertraue deinen Instinkten, aber informiere dich über Wirkung, Dauer und Kontraindikationen wie z.B Medikamente oder Vorerkrankungen.</span></div></div>'
    +'<div class="pp-rule"><span class="n">2</span><div><b>Umfeld beachten.</b> <span class="tx">Vertraute Umgebung, kein Alkohol, keine Medikamente, nicht am Steuer, nie Konsumieren in anwesenheit von Minderjährigen.</span></div></div>'
    +'<div class="pp-rule"><span class="n">3</span><div><b>Niedrig starten.</b> <span class="tx">Erste Erfahrung max. 2.5–5&nbsp;mg THC pro Konsumeinheit.</span></div></div>'
    +'<div class="pp-rule"><span class="n">4</span><div><b>Geduld haben.</b> <span class="tx">Wirkung erst nach 30–120&nbsp;Min. Niemals nachlegen, weil „nichts passiert“.</span></div></div>'"""

if old1 not in content:
    print("WARNUNG 1: Regel-Block nicht (exakt) gefunden — evtl. seit letztem Abgleich verändert.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Regeln neu angeordnet: 1=Informationen suchen, 2=Umfeld beachten, 3=Niedrig starten, 4=Geduld haben.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen, evtl. hat sich der Text seit dem letzten Fetch geändert!")
