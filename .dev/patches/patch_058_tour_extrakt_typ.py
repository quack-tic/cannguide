#!/usr/bin/env python3
# Patch 058: Neuer Tour-Schritt "Extrakt-Typ" zwischen "Eingesetzte
# Wirkstoffmenge" und "Wirkstoffgehalt" eingefuegt. Im Bluetenmodus ist
# #extract-type unsichtbar -- der bereits bestehende Ueberspring-Mechanismus
# (Patch 057) blendet den Schritt dort automatisch aus, ohne Sonderfall-Logik.
# Zusaetzlich: praeziserer Wortlaut im "Wirkstoffgehalt"-Schritt --
# "sinnvoller Startwert" -> "fuer diese Methode typischer Durchschnittswert".
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

old1 = """  {sel:['#ig'], t:'① Eingesetzte Wirkstoffmenge', b:'Wie viel Gramm Blüten oder Extrakt setzt du ein? Wichtig: Das ist die Menge des Cannabis-Ausgangsmaterials — NICHT die Menge deines Trägermediums (Butter, Öl etc.), die kommt gleich in Block ②.'},
  {sel:['#potency','#potency-ext'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest — beeinflusst die ganze Rechnung stark. Ohne Test: eher höher schätzen als tiefer — eine Unterschätzung führt leicht zu ungewolltem Nachdosieren und Greening Out. Im Extrakt-Modus wählt "Extrakt-Typ" automatisch einen sinnvollen Startwert.'},"""

new1 = """  {sel:['#ig'], t:'① Eingesetzte Wirkstoffmenge', b:'Wie viel Gramm Blüten oder Extrakt setzt du ein? Wichtig: Das ist die Menge des Cannabis-Ausgangsmaterials — NICHT die Menge deines Trägermediums (Butter, Öl etc.), die kommt gleich in Block ②.'},
  {sel:['#extract-type'], t:'Extrakt-Typ', b:'Wähle die Art deines Extrakts (z.B. BHO, Rosin, RSO, Live Resin) — dieser Schritt erscheint nur im Extrakt-Modus. Die Auswahl setzt automatisch einen für diese Methode typischen Durchschnittswert beim Wirkstoffgehalt, den du im nächsten Schritt bei Bedarf noch anpassen kannst.'},
  {sel:['#potency','#potency-ext'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest — beeinflusst die ganze Rechnung stark. Ohne Test: eher höher schätzen als tiefer — eine Unterschätzung führt leicht zu ungewolltem Nachdosieren und Greening Out.'},"""

if old1 not in content:
    print("WARNUNG 1: TOUR_STEPS-Abschnitt nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Neuer Schritt 'Extrakt-Typ' eingefügt, Wirkstoffgehalt-Text präzisiert.")

# ─────────────────────────────────────────────────────────────────────────
# 2) startCalcTour(): erzwingt nicht mehr den Bluetenmodus -- die Tour
#    respektiert jetzt den Modus, der beim Start bereits aktiv ist
# ─────────────────────────────────────────────────────────────────────────
old2 = """window.startCalcTour = function() {
  setCalcMode('raw');
  calcUpdate();
  tourIdx = 0;"""
new2 = """window.startCalcTour = function() {
  calcUpdate();
  tourIdx = 0;"""

if old2 not in content:
    print("WARNUNG 2: startCalcTour() nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: startCalcTour() erzwingt den Modus nicht mehr — respektiert den aktuell aktiven Modus.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
