#!/usr/bin/env python3
# Patch C — Aufraeumen nach Dosis-Umstellung auf absolute Werte.
# Koerpergewicht-Feld, Sex-Toggle und sex-info beeinflussen die Empfehlung
# nicht mehr (Dosierung ist absolut). Die sex-info behauptet sogar noch einen
# "Startdosis-Faktor -15%", der faktisch nicht mehr greift -> irrefuehrend.
# Entfernt: HTML-Koerperdaten-Block, setSex(), currentSex, tote bw/sexF-Zeilen.
import io

PATH = "index.html"
s = io.open(PATH, encoding="utf-8").read()
orig = s
notes = []

def cut_between(text, start_anchor, end_anchor, label):
    i = text.find(start_anchor)
    if i == -1:
        notes.append("[skip] %s: bereits entfernt." % label); return text
    j = text.find(end_anchor, i)
    if j == -1:
        notes.append("[WARN] %s: End-Anker fehlt -> manuell pruefen." % label); return text
    notes.append("[ok]   %s entfernt (%d Zeichen)." % (label, j - i))
    return text[:i] + text[j:]

# --- C1: HTML Koerperdaten-Block (Sex-Toggle + sex-info + bodyweight) ---
s = cut_between(s, "    <!-- K\u00f6rperdaten -->\n", "    <!-- Terpene -->", "C1: Koerperdaten-Block")

# --- C2: currentSex-Deklaration ---
if "var currentSex = null;\n" in s:
    s = s.replace("var currentSex = null;\n", "", 1); notes.append("[ok]   C2: currentSex entfernt.")
else:
    notes.append("[skip] C2: currentSex bereits weg.")

# --- C3: setSex()-Funktion ---
s = cut_between(s, "window.setSex = function(s) {", "window.toggleLang = function() {", "C3: setSex()")

# --- C4: tote bw/sexF-Zeilen in calcUpdate ---
dead = ("  var bw = parseFloat(document.getElementById('bodyweight').value) || 0;\n"
        "  var sexF = currentSex==='f' ? 0.85 : currentSex==='m' ? 1.0 : 0.92;\n")
if dead in s:
    s = s.replace(dead, "", 1); notes.append("[ok]   C4: tote bw/sexF-Zeilen entfernt.")
else:
    notes.append("[skip] C4: bw/sexF bereits weg.")

for n in notes: print(" ", n)
if s != orig:
    io.open(PATH, "w", encoding="utf-8").write(s)
    print("Patch C geschrieben.")
else:
    print("Patch C: keine Änderung (idempotent).")
