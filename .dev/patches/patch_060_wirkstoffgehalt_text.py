#!/usr/bin/env python3
# Patch 060: Logikfehler im "Wirkstoffgehalt"-Tourschritt korrigiert.
# Eine unterschaetzte Potenz fuehrt NICHT zu ungewolltem Nachdosieren
# (das ist ein separates Problem, verursacht durch die Onset-Verzoegerung
# bei Edibles). Sie fuehrt direkt dazu, dass die tatsaechlich aufgenommene
# Wirkstoffmenge in der EINEN Portion hoeher ist als angenommen -- also
# eine unerwartet starke Wirkung/Greening Out durch die erste Portion
# selbst, nicht durch Nachlegen.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """  {sel:['#potency','#potency-ext'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest — beeinflusst die ganze Rechnung stark. Ohne Test: eher höher schätzen als tiefer — eine Unterschätzung führt leicht zu ungewolltem Nachdosieren und Greening Out.'},"""

new1 = """  {sel:['#potency','#potency-ext'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest — beeinflusst die ganze Rechnung stark. Ohne Test: eher höher schätzen als tiefer — eine Unterschätzung führt dazu, dass die tatsächlich aufgenommene Menge schon in der ersten Portion höher ist als angenommen, mit dem Risiko einer unerwartet starken Wirkung bis hin zu Greening Out.'},"""

if old1 not in content:
    print("WARNUNG 1: TOUR_STEPS-Eintrag 'Wirkstoffgehalt' nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Kausalkette korrigiert — Unterschätzung führt direkt zu Überwirkung, nicht zu Nachdosieren.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
