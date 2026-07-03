#!/usr/bin/env python3
# Patch A — Inhalationsmodus sauber aus dem Rechner entfernen.
# Grund: die mg-genaue "bioverfuegbar"-Angabe beruht auf iEff (Geraete-Abgabe-
# Effizienz), nicht auf systemischer Bioverfuegbarkeit -> ueberschaetzt die
# real aufgenommene Menge um das ~2-3fache. Fuer ein HR-Tool die falsche
# Richtung. Inhalation wird als Rechner-Modus entfernt; Faustregeln wandern
# in den Praeventionsteil (siehe Patch B).
#
# Entfernt: Mode-Button, #inhale-inputs, #inhale-puff-info, #inhale-compare-info,
#           onInhaleMethodChange(), den if(calcMode==='inhale')-Zweig in
#           calcUpdate(), sowie die inhale-Zweige in setCalcMode().
import io, re, sys

PATH = "index.html"
s = io.open(PATH, encoding="utf-8").read()
orig = s
notes = []

def cut_between(text, start_anchor, end_anchor, label):
    """Entfernt text[start..end) inkl. start_anchor, exkl. end_anchor."""
    i = text.find(start_anchor)
    if i == -1:
        notes.append("[skip] %s: Start-Anker weg (bereits entfernt?)." % label)
        return text
    j = text.find(end_anchor, i)
    if j == -1:
        notes.append("[WARN] %s: End-Anker nicht gefunden -> manuell pruefen." % label)
        return text
    notes.append("[ok]   %s entfernt (%d Zeichen)." % (label, j - i))
    return text[:i] + text[j:]

# --- A1: Mode-Button ---
btn = '      <button id="btn-mode-inhale" class="btn" onclick="setCalcMode(\'inhale\')">\U0001F4A8 Inhalation</button>\n'
if btn in s:
    s = s.replace(btn, "", 1); notes.append("[ok]   A1: Mode-Button entfernt.")
else:
    notes.append("[skip] A1: Mode-Button bereits weg.")

# --- A2: #inhale-inputs Block (inkl. Kommentar) ---
s = cut_between(s, "    <!-- Inhalation -->\n", '    <div id="edible-fields">', "A2: #inhale-inputs")

# --- A3: #inhale-puff-info + #inhale-compare-info ---
s = cut_between(s, '  <div id="inhale-puff-info"', "\n</div>\n<!-- CHARGEN -->", "A3: puff+compare-info")

# --- A4: onInhaleMethodChange() ---
s = cut_between(s, "window.onInhaleMethodChange = function() {", "window.calcUpdate = function() {", "A4: onInhaleMethodChange")

# --- A5: if(calcMode==='inhale')-Zweig in calcUpdate ---
s = cut_between(s, "  // \u2500\u2500 INHALATION", "  var cfg = MEDIA_CFG[med]", "A5: calcUpdate inhale-Zweig")

# --- A6: setCalcMode() inhale-Zweige ---
repl = [
    ("  document.getElementById('inhale-inputs').style.display = m==='inhale'?'block':'none';\n", "", "A6a inhale-inputs display"),
    ("if(ef) ef.style.display = m==='inhale'?'none':'block';", "if(ef) ef.style.display = 'block';", "A6b edible-fields immer sichtbar"),
    ("if(cmr) cmr.style.display = m==='inhale'?'none':'grid';", "if(cmr) cmr.style.display = 'grid';", "A6c carrier-medium immer sichtbar"),
    ("  var inhaleInfo = document.getElementById('inhale-puff-info'); if(inhaleInfo) inhaleInfo.style.display = m==='inhale'?'block':'none';\n", "", "A6d puff-info display"),
    ("  var inhaleCompare = document.getElementById('inhale-compare-info'); if(inhaleCompare) inhaleCompare.style.display = m==='inhale'?'block':'none';\n", "", "A6e compare-info display"),
    ("  document.getElementById('btn-mode-inhale').className = 'btn'+(m==='inhale'?' primary':'');\n", "", "A6f button-class"),
]
for old, new, label in repl:
    if old in s:
        s = s.replace(old, new, 1); notes.append("[ok]   %s." % label)
    else:
        notes.append("[skip] %s (bereits erledigt)." % label)

for n in notes:
    print(" ", n)

if s != orig:
    io.open(PATH, "w", encoding="utf-8").write(s)
    print("Patch A geschrieben.")
else:
    print("Patch A: keine Änderung (idempotent).")
