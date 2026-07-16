#!/usr/bin/env python3
# Patch 061: Intensitaetsskala komplett neu gestaffelt.
# Vorher war "Mittel" mit 10mg Spannweite (5-15mg) unverhaeltnismaessig breit
# im Vergleich zu den 2.5mg-Stufen darunter -- das liess 15mg faelschlich
# "noch moderat" wirken. Neue, gleichmaessigere Stufung:
#   <2.5mg       Schwellendosis
#   2.5-5mg      Niedrig
#   5-10mg       Mittel        (vorher 5-15mg)
#   10-20mg      Stark         (vorher 15-25mg)
#   20-35mg      Sehr stark    (vorher >25mg)
#   >35mg        Extrem        (NEU) -- Empfehlung: Portionen teilen UND
#                Rezept ueberdenken (zu viel Wirkstoff fuers Vorhaben)
# Alle abgeleiteten Schwellenwerte (Pulsieren, Rahmenfarben) wurden auf die
# neue Skala angepasst (rot ab 20mg statt 25mg, amber ab 10mg statt 15mg).
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

# ─────────────────────────────────────────────────────────────────────────
# 1) Stufen-Logik (tag/rec) neu gefasst
# ─────────────────────────────────────────────────────────────────────────
old1 = """  var tag='', rec='';
  if(ppMg<2.5) { tag='<span class="tag tg">Schwellendosis (&lt;2.5mg)</span>'; rec='Kaum spürbar. Mikrodosierung. Ideal zum Einstieg.'; }
  else if(ppMg<5) { tag='<span class="tag tg">Niedrig (2.5–5mg)</span>'; rec='Einsteiger-Bereich. Gut kontrollierbar.'; }
  else if(ppMg<15) { tag='<span class="tag tg">Mittel (5–15mg)</span>'; rec='Standard für Erfahrene.';}
  else if(ppMg<25) { tag='<span class="tag ta">Stark (15–25mg)</span>'; rec='Nur erfahrene Konsumenten!'; }
  else { tag='<span class="tag tr">Sehr stark (&gt;25mg)</span>'; rec='Portionen teilen.'; }
  document.getElementById('r-int').innerHTML = tag;
  var portionBox = document.getElementById('r-portion').closest('.rm');
  if(portionBox) portionBox.classList.toggle('pulse-warn', ppMg >= 25);"""

new1 = """  var tag='', rec='';
  if(ppMg<2.5) { tag='<span class="tag tg">Schwellendosis (&lt;2.5mg)</span>'; rec='Kaum spürbar. Mikrodosierung. Ideal zum Einstieg.'; }
  else if(ppMg<5) { tag='<span class="tag tg">Niedrig (2.5–5mg)</span>'; rec='Einsteiger-Bereich. Gut kontrollierbar.'; }
  else if(ppMg<10) { tag='<span class="tag tg">Mittel (5–10mg)</span>'; rec='Standard für Erfahrene.';}
  else if(ppMg<20) { tag='<span class="tag ta">Stark (10–20mg)</span>'; rec='Nur erfahrene Konsumenten!'; }
  else if(ppMg<35) { tag='<span class="tag tr">Sehr stark (20–35mg)</span>'; rec='Portionen teilen.'; }
  else { tag='<span class="tag tr">Extrem (&gt;35mg)</span>'; rec='Portionen teilen — und Rezept überdenken: vermutlich zu viel Wirkstoff fürs Vorhaben eingesetzt.'; }
  document.getElementById('r-int').innerHTML = tag;
  var portionBox = document.getElementById('r-portion').closest('.rm');
  if(portionBox) portionBox.classList.toggle('pulse-warn', ppMg >= 20);"""

if old1 not in content:
    print("WARNUNG 1: Intensitäts-Stufen-Logik nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Intensitätsskala neu gestaffelt (6 Stufen), 'Extrem' (>35mg) neu mit Rezept-Hinweis.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Schweregrad-Rahmenfarbe & Pulsieren (Intensität/Empfehlung-Karte) auf
#    neue Schwellenwerte angepasst
# ─────────────────────────────────────────────────────────────────────────
old2 = """  var severityColor = ppMg>=25 ? 'var(--warn)' : ppMg>=15 ? 'var(--amber)' : 'var(--accent)';
  var intBox = document.getElementById('r-int').closest('.rm');
  var recBox = document.getElementById('r-rec').closest('.rm');
  [intBox, recBox].forEach(function(box){
    if(!box) return;
    box.classList.remove('pulse-warn');
    if(ppMg>=25) { box.classList.add('pulse-warn'); }
    else { box.style.borderColor = severityColor; }
  });"""

new2 = """  var severityColor = ppMg>=20 ? 'var(--warn)' : ppMg>=10 ? 'var(--amber)' : 'var(--accent)';
  var intBox = document.getElementById('r-int').closest('.rm');
  var recBox = document.getElementById('r-rec').closest('.rm');
  [intBox, recBox].forEach(function(box){
    if(!box) return;
    box.classList.remove('pulse-warn');
    if(ppMg>=20) { box.classList.add('pulse-warn'); }
    else { box.style.borderColor = severityColor; }
  });"""

if old2 not in content:
    print("WARNUNG 2: Schweregrad-Rahmenfarben-Logik nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Rahmenfarbe/Pulsieren-Schwellenwerte auf neue Skala angepasst (rot ab 20mg, amber ab 10mg).")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
