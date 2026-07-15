#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Patch D — (A) Kief/Pollen als unverarbeitetes Bluetenmaterial aus der
# "Loesungsmittelfrei"-Gruppe in eine eigene optgroup ziehen (Kief entsteht
# durch blosses Sieben, keine Herstellung). (B) Modus "Rohmaterial" -> "Blueten"
# umbenennen, inkl. der internen "Material"-Labels im Roh-Zweig.
import io

PATH = "index.html"
s = io.open(PATH, encoding="utf-8").read()
orig = s
notes = []

def repl(old, new, label):
    global s
    if old in s:
        s = s.replace(old, new, 1); notes.append("[ok]   %s." % label)
    elif new in s:
        notes.append("[skip] %s (bereits erledigt)." % label)
    else:
        notes.append("[WARN] %s: Ziel nicht gefunden -> manuell pruefen." % label)

# --- A: Kief eigene optgroup ---
repl(
    '<optgroup label="L\u00f6sungsmittelfrei"><option value="rosin">Rosin (60\u201380%)</option>'
    '<option value="kief">Kief / Pollen (30\u201360%)</option>'
    '<option value="thca_k">THCA-Kristalle (95\u201399%)</option></optgroup>',
    '<optgroup label="Bl\u00fctenmaterial (unverarbeitet)">'
    '<option value="kief">Kief / Pollen (30\u201360%)</option></optgroup>\n'
    '            <optgroup label="L\u00f6sungsmittelfrei"><option value="rosin">Rosin (60\u201380%)</option>'
    '<option value="thca_k">THCA-Kristalle (95\u201399%)</option></optgroup>',
    "A: Kief in eigene optgroup"
)

# --- B: Rohmaterial -> Blueten ---
repl("Rohmaterial & Extrakte", "Bl\u00fcten & Extrakte", "B1: Dashboard-Untertitel")
repl("\U0001F33F Rohmaterial", "\U0001F33F Bl\u00fcten", "B2: Mode-Button")
repl("<!-- Rohmaterial -->", "<!-- Bl\u00fcten -->", "B3: HTML-Kommentar")
repl("Wirkstoffgehalt Material:", "Wirkstoffgehalt Bl\u00fcten:", "B4: Slider-Label")
repl("g+'g Material \u00d7 '", "g+'g Bl\u00fcten \u00d7 '", "B5: Rechen-Beschreibung")
repl("g+'g Material ('", "g+'g Bl\u00fcten ('", "B6: Ergebnis-Zusammenfassung")

for n in notes: print(" ", n)
if s != orig:
    io.open(PATH, "w", encoding="utf-8").write(s)
    print("Patch D geschrieben.")
else:
    print("Patch D: keine Änderung (idempotent).")
