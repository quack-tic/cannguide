#!/usr/bin/env python3
# Patch 062: Alle 6 Intensitaets-Empfehlungstexte ueberarbeitet.
# Vorher: teils sehr knapp/telegrammstil ("Nur erfahrene Konsumenten!" ohne
# "fuer", "Standard fuer Erfahrene.", "Portionen teilen.") -- schwer
# zugaenglich fuer materiefremde Laien. Jetzt: vollstaendige, klare Saetze.
# Bei "Sehr stark"/"Extrem" ausserdem konkrete, gleichwertige Handlungs-
# optionen (mehr Traegermenge, mehr Portionen, weniger Wirkstoff) statt nur
# "teilen", unterstuetzend statt belehrend formuliert.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 3

old1 = """  if(ppMg<2.5) { tag='<span class="tag tg">Schwellendosis (&lt;2.5mg)</span>'; rec='Kaum spürbar. Mikrodosierung. Ideal zum Einstieg.'; }
  else if(ppMg<5) { tag='<span class="tag tg">Niedrig (2.5–5mg)</span>'; rec='Einsteiger-Bereich. Gut kontrollierbar.'; }
  else if(ppMg<10) { tag='<span class="tag tg">Mittel (5–10mg)</span>'; rec='Standard für Erfahrene.';}
  else if(ppMg<20) { tag='<span class="tag ta">Stark (10–20mg)</span>'; rec='Nur erfahrene Konsumenten!'; }
  else if(ppMg<35) { tag='<span class="tag tr">Sehr stark (20–35mg)</span>'; rec='Portionen teilen.'; }
  else { tag='<span class="tag tr">Extrem (&gt;35mg)</span>'; rec='Portionen teilen — und Rezept überdenken: vermutlich zu viel Wirkstoff fürs Vorhaben eingesetzt.'; }"""

new1 = """  if(ppMg<2.5) { tag='<span class="tag tg">Schwellendosis (&lt;2.5mg)</span>'; rec='Kaum spürbar. Diese Menge eignet sich für eine Mikrodosierung oder als vorsichtigen ersten Test.'; }
  else if(ppMg<5) { tag='<span class="tag tg">Niedrig (2.5–5mg)</span>'; rec='Ein guter Einsteiger-Bereich — die Wirkung lässt sich hier gut einschätzen und kontrollieren.'; }
  else if(ppMg<10) { tag='<span class="tag tg">Mittel (5–10mg)</span>'; rec='Eine übliche Dosis für Personen mit etwas Konsumerfahrung.';}
  else if(ppMg<20) { tag='<span class="tag ta">Stark (10–20mg)</span>'; rec='Diese Menge eignet sich nur für erfahrene Konsumentinnen und Konsumenten.'; }
  else if(ppMg<35) { tag='<span class="tag tr">Sehr stark (20–35mg)</span>'; rec='Portionen teilen ist hier sinnvoll. Optional fürs nächste Mal: mehr Trägermenge, mehr Portionen oder weniger Wirkstoff verwenden.'; }
  else { tag='<span class="tag tr">Extrem (&gt;35mg)</span>'; rec='Portionen unbedingt teilen. Fürs nächste Mal: mehr Trägermenge verwenden, mehr Portionen daraus machen oder weniger Wirkstoff einsetzen — alles einfache Wege zu einer leichter steuerbaren Dosis.'; }"""

if old1 not in content:
    print("WARNUNG 1: Empfehlungstexte nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Alle 6 Empfehlungstexte zu vollständigen, laienverständlichen Sätzen ausgebaut.")

# ─────────────────────────────────────────────────────────────────────────
# 2) "Eingesetzte Wirkstoffmenge" (#ig) bekommt eine eigene, kombinierte
#    Einheiten-Auswahl (mg/g/kg UND ml/dl/l gleichzeitig) statt an das
#    Traeger-Medium gekoppelt zu sein. So laesst sich z.B. eine Masse
#    (0.5g FECO) unabhaengig von einem in ml gemessenen Traeger (Tinktur)
#    eingeben.
# ─────────────────────────────────────────────────────────────────────────
old2 = """window.onMediumChange = function() {
  var med = document.getElementById('cm').value;
  var cfg = MEDIA_CFG[med]||{unit:'g',eff:80,hint:''};
  setUnitOptions('carrier-unit', cfg.unit);
  setUnitOptions('portion-unit', cfg.unit);
  setUnitOptions('input-unit-label', cfg.unit);
  document.getElementById('eff').value = cfg.eff;
  document.getElementById('eo').textContent = cfg.eff;
  document.getElementById('eff-hint').textContent = cfg.hint;
  calcUpdate();
};"""

new2 = """function setIgUnitOptions() {
  var el = document.getElementById('input-unit-label');
  if(!el) return;
  var cur = el.value;
  el.innerHTML = '<option value="0.001">mg</option><option value="1">g</option><option value="1000">kg</option><option value="1">ml</option><option value="100">dl</option><option value="1000">l</option>';
  if(cur) el.value = cur;
}
window.onMediumChange = function() {
  var med = document.getElementById('cm').value;
  var cfg = MEDIA_CFG[med]||{unit:'g',eff:80,hint:''};
  setUnitOptions('carrier-unit', cfg.unit);
  setUnitOptions('portion-unit', cfg.unit);
  document.getElementById('eff').value = cfg.eff;
  document.getElementById('eo').textContent = cfg.eff;
  document.getElementById('eff-hint').textContent = cfg.hint;
  calcUpdate();
};"""

if old2 not in content:
    print("WARNUNG 2: onMediumChange() nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: 'Eingesetzte Wirkstoffmenge' bekommt eigene, kombinierte Einheiten-Auswahl (mg/g/kg/ml/dl/l).")

# ─────────────────────────────────────────────────────────────────────────
# 3) Einmalig beim Laden aufrufen (nicht bei jedem Mediumwechsel, damit die
#    Auswahl des Nutzers unabhaengig vom Medium erhalten bleibt)
# ─────────────────────────────────────────────────────────────────────────
old3 = """  onMediumChange();"""
new3 = """  setIgUnitOptions();
  onMediumChange();"""

if old3 not in content:
    print("WARNUNG 3: onMediumChange()-Init-Aufruf nicht gefunden.")
else:
    content = content.replace(old3, new3, 1)
    changes += 1
    print(f"3/{total}: Einheiten-Auswahl für Wirkstoffmenge wird einmalig beim Laden initialisiert.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
