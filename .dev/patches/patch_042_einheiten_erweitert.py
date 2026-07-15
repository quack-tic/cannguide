#!/usr/bin/env python3
# Patch 042: Einheiten-Umschalter erweitert von 2 auf 3 Stufen:
# Feste Medien: mg / g / kg (statt nur g / kg)
# Fluessige Medien: ml / dl / l (statt nur ml / l)
# Basiseinheit fuer die interne Berechnung bleibt unveraendert g bzw. ml --
# nur die Multiplikatoren aendern sich (mg=0.001, g=1, kg=1000 bzw.
# ml=1, dl=100, l=1000).
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """function setUnitOptions(id, baseUnit) {
  var el = document.getElementById(id);
  if(!el) return;
  if(baseUnit === 'ml') el.innerHTML = '<option value="1">ml</option><option value="1000">l</option>';
  else el.innerHTML = '<option value="1">g</option><option value="1000">kg</option>';
  el.value = '1';
}"""

new1 = """function setUnitOptions(id, baseUnit) {
  var el = document.getElementById(id);
  if(!el) return;
  if(baseUnit === 'ml') el.innerHTML = '<option value="1">ml</option><option value="100">dl</option><option value="1000">l</option>';
  else el.innerHTML = '<option value="0.001">mg</option><option value="1">g</option><option value="1000">kg</option>';
  el.value = '1';
}"""

if old1 not in content:
    print("WARNUNG 1: setUnitOptions() nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Einheiten-Umschalter erweitert (mg/g/kg bzw. ml/dl/l).")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
