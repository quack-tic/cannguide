#!/usr/bin/env python3
# Patch 035: Zwei Tour-Bugs behoben.
# 1) resetCalcTour() loeschte den localStorage-Flag VOR showPage('calc') --
#    das triggerte automatisch den Prompt-Dialog UND gleichzeitig per
#    setTimeout den direkten Tour-Start -> zwei Overlays parallel.
# 2) Die SVG-Maske nutzte fill="black" fuer den Ausschnitt. Bei Alpha-basierter
#    mask-image-Interpretation (manche Browser) ist Schwarz genauso undurch-
#    sichtig wie Weiss (Alpha=1) -> kein Ausschnitt sichtbar, alles bleibt
#    milchig. Fix: Ausschnitt bekommt fill-opacity="0" (Alpha=0 UND Luminanz=0),
#    funktioniert damit unabhaengig vom Masking-Modus des Browsers.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

# ─────────────────────────────────────────────────────────────────────────
# 1) resetCalcTour(): kein doppeltes Triggern mehr
# ─────────────────────────────────────────────────────────────────────────
old1 = """window.resetCalcTour = function() {
  try { localStorage.removeItem('cannguide_calc_tour_done'); } catch(e) {}
  showPage('calc');
  setTimeout(function(){ startCalcTour(); }, 80);
};"""

new1 = """window.resetCalcTour = function() {
  showPage('calc');
  setTimeout(function(){ startCalcTour(); }, 80);
};"""

if old1 not in content:
    print("WARNUNG 1: resetCalcTour()-Funktion nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: resetCalcTour() löst nicht mehr zusätzlich den Prompt-Dialog aus.")

# ─────────────────────────────────────────────────────────────────────────
# 2) SVG-Maske alpha/luminanz-sicher machen
# ─────────────────────────────────────────────────────────────────────────
old2 = """    '<rect x="'+x+'" y="'+y+'" width="'+rw+'" height="'+rh+'" rx="14" ry="14" fill="black"/>'+"""
new2 = """    '<rect x="'+x+'" y="'+y+'" width="'+rw+'" height="'+rh+'" rx="14" ry="14" fill="black" fill-opacity="0"/>'+"""

if old2 not in content:
    print("WARNUNG 2: SVG-Masken-Rect nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: SVG-Maske jetzt alpha- UND luminanz-sicher (fill-opacity=0 statt fill=black).")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
