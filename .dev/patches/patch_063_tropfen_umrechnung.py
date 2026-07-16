#!/usr/bin/env python3
# Patch 063: Tropfen als vierte Einheit bei fluessigen Feldern (Traegermenge
# gesamt, Menge pro Portion) ergaenzt -- Standardannahme 20 Tropfen ≈ 1ml
# (uebliche Apotheken-Konvention fuer waessrige Loesungen; bei Tinkturen mit
# geringerer Oberflaechenspannung koennen es real etwas mehr sein, daher als
# Tooltip gekennzeichnet). Damit laesst sich z.B. "Menge pro Portion" direkt
# als "1 Tropfen" statt "0.05 ml" eingeben.
# Zusaetzlich: Hinweis dazu im Tour-Schritt "Traegermenge & Portion" ergaenzt.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

# ─────────────────────────────────────────────────────────────────────────
# 1) setUnitOptions(): Tropfen als vierte Option bei ml-basierten Feldern
# ─────────────────────────────────────────────────────────────────────────
old1 = """function setUnitOptions(id, baseUnit) {
  var el = document.getElementById(id);
  if(!el) return;
  if(baseUnit === 'ml') el.innerHTML = '<option value="1">ml</option><option value="100">dl</option><option value="1000">l</option>';
  else el.innerHTML = '<option value="0.001">mg</option><option value="1">g</option><option value="1000">kg</option>';
  el.value = '1';
}"""

new1 = """function setUnitOptions(id, baseUnit) {
  var el = document.getElementById(id);
  if(!el) return;
  if(baseUnit === 'ml') el.innerHTML = '<option value="1">ml</option><option value="0.05" title="Standardannahme: 20 Tropfen ≈ 1 ml (kann je nach Flüssigkeit/Tropfer leicht abweichen)">Tropfen</option><option value="100">dl</option><option value="1000">l</option>';
  else el.innerHTML = '<option value="0.001">mg</option><option value="1">g</option><option value="1000">kg</option>';
  el.value = '1';
}"""

if old1 not in content:
    print("WARNUNG 1: setUnitOptions() nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: 'Tropfen' als Einheit bei Träger/Portion ergänzt (20 Tropfen ≈ 1ml).")

# ─────────────────────────────────────────────────────────────────────────
# 2) Tour: Hinweis auf die Tropfen-Einheit im Schritt "Trägermenge & Portion"
# ─────────────────────────────────────────────────────────────────────────
old2 = """  {sel:['#carrier','#portion-c'], t:'Trägermenge & Portion', b:'Wie viel hast du insgesamt hergestellt, und wie viele Gramm Wirkstoffträger stecken in einer fertigen Portion? Beides zusammen bestimmt die Dosis pro Stück.'},"""

new2 = """  {sel:['#carrier','#portion-c'], t:'Trägermenge & Portion', b:'Wie viel hast du insgesamt hergestellt, und wie viel steckt in einer fertigen Portion? Beides zusammen bestimmt die Dosis pro Stück. Bei flüssigen Trägern (z.B. Tinktur) kannst du bei der Einheit auch "Tropfen" wählen — praktisch, wenn eine Portion z.B. genau 1 Tropfen sein soll.'},"""

if old2 not in content:
    print("WARNUNG 2: TOUR_STEPS-Eintrag 'Trägermenge & Portion' nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Tour-Hinweis auf 'Tropfen'-Einheit ergänzt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
