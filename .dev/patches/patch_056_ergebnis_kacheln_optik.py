#!/usr/bin/env python3
# Patch 056: Drei Verbesserungen an der Ergebnisanzeige.
# 1) .rm-Karten zentrieren ihren Inhalt jetzt vertikal (flex) -- behebt die
#    "Riesenkachel fuer kleinen Inhalt"-Optik bei der Intensitaets-Karte,
#    die durch CSS-Grid-Stretch auf die Hoehe der Einstiegsdosis-Karte
#    gezogen wird.
# 2) Intensitaets- UND Empfehlungs-Karte bekommen jetzt einen farbigen Rahmen
#    passend zum Schweregrad (gruen/amber/rot), analog zur bereits
#    bestehenden Portion-Karte -- konsistente visuelle Sprache.
# 3) Bei "Sehr stark" (>25mg) pulsiert jetzt auch die Intensitaets- und die
#    Empfehlungs-Karte (nicht nur die Portion-Karte wie bisher).
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

# ─────────────────────────────────────────────────────────────────────────
# 1) CSS: .rm-Karten vertikal zentrieren
# ─────────────────────────────────────────────────────────────────────────
old1 = """.rm{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:.875rem}"""
new1 = """.rm{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:.875rem;display:flex;flex-direction:column;justify-content:center}"""

if old1 not in content:
    print("WARNUNG 1: .rm CSS nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: .rm-Karten zentrieren ihren Inhalt jetzt vertikal.")

# ─────────────────────────────────────────────────────────────────────────
# 2) JS: Intensitaets- und Empfehlungs-Karte bekommen Rahmenfarbe + Pulsieren
#    nach Schweregrad
# ─────────────────────────────────────────────────────────────────────────
old2 = """  document.getElementById('r-int').innerHTML = tag;
  var portionBox = document.getElementById('r-portion').closest('.rm');
  if(portionBox) portionBox.classList.toggle('pulse-warn', ppMg >= 25);
  document.getElementById('r-rec').textContent = rec;"""

new2 = """  document.getElementById('r-int').innerHTML = tag;
  var portionBox = document.getElementById('r-portion').closest('.rm');
  if(portionBox) portionBox.classList.toggle('pulse-warn', ppMg >= 25);
  document.getElementById('r-rec').textContent = rec;

  var severityColor = ppMg>=25 ? 'var(--warn)' : ppMg>=15 ? 'var(--amber)' : 'var(--accent)';
  var intBox = document.getElementById('r-int').closest('.rm');
  var recBox = document.getElementById('r-rec').closest('.rm');
  [intBox, recBox].forEach(function(box){
    if(!box) return;
    box.classList.remove('pulse-warn');
    if(ppMg>=25) { box.classList.add('pulse-warn'); }
    else { box.style.borderColor = severityColor; }
  });"""

if old2 not in content:
    print("WARNUNG 2: Intensität/Empfehlung-Zuweisungsblock nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Intensitäts- & Empfehlungs-Karte bekommen Schweregrad-Farbe + Pulsieren bei 'Sehr stark'.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
