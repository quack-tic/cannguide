#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Patch G — Navigation Landing/Rechner -> Lexikon-KATEGORIE (nicht Einzeleintrag,
# daher nicht bruechig; Deep-Links per [[link:ID]] kommen spaeter).
#  G1 Helper gotoLexCat(cat): setzt activeLibCat und oeffnet Bibliothek.
#  G2 Grosse Landing-Kacheln (THC/CBD/CBN/CBG) -> Kategorie 'cannabinoide'.
#  G3 Passende Text-Links (kchips + Leselisten) -> 'cannabinoide' / 'dekarb'.
#  G4 "Mehr im Lexikon"-Button in 11-OH-Box (-> cannabinoide) und Toleranz-Box (-> risiken).
import io

PATH = "index.html"
s = io.open(PATH, encoding="utf-8").read()
orig = s
notes = []

def repl(old, new, label, count=1):
    global s
    if old in s:
        n = s.count(old) if count == -1 else count
        s = s.replace(old, new, n)
        notes.append("[ok]   %s (%dx)." % (label, n))
    elif new.split('onclick')[0] in s and old not in s:
        notes.append("[skip] %s (bereits erledigt)." % label)
    else:
        notes.append("[WARN] %s: Ziel nicht gefunden -> pruefen." % label)

# --- G1: Helper ---
hookline = "window.setLibCat = function(k) { activeLibCat=k; renderLib(); };"
helper = hookline + "\nwindow.gotoLexCat = function(c){ activeLibCat = c; showPage('library'); };"
if "window.gotoLexCat" in s:
    notes.append("[skip] G1: Helper bereits vorhanden.")
elif hookline in s:
    s = s.replace(hookline, helper, 1); notes.append("[ok]   G1: gotoLexCat-Helper.")
else:
    notes.append("[WARN] G1: setLibCat-Anker fehlt -> pruefen.")

# --- G2: 4 grosse Kacheln -> cannabinoide (alle ref-card identisch) ---
repl('<div class="ref-card" onclick="showPage(\'library\')">',
     '<div class="ref-card" onclick="gotoLexCat(\'cannabinoide\')">',
     "G2: grosse Kacheln", count=-1)

# --- G3: Text-Links ---
repl('<span class="kchip" onclick="showPage(\'library\')"><b>\u2197</b> THC vs. CBD</span>',
     '<span class="kchip" onclick="gotoLexCat(\'cannabinoide\')"><b>\u2197</b> THC vs. CBD</span>',
     "G3a: kchip THC vs. CBD")
repl('<span class="kchip" onclick="showPage(\'library\')"><b>\u2197</b> Decarboxylierung</span>',
     '<span class="kchip" onclick="gotoLexCat(\'dekarb\')"><b>\u2197</b> Decarboxylierung</span>',
     "G3b: kchip Decarboxylierung")
repl('<div class="read" onclick="showPage(\'library\')"><span class="rank">02</span>',
     '<div class="read" onclick="gotoLexCat(\'cannabinoide\')"><span class="rank">02</span>',
     "G3c: Leseliste 02")
repl('<div class="read" onclick="showPage(\'library\')"><span class="rank">03</span>',
     '<div class="read" onclick="gotoLexCat(\'dekarb\')"><span class="rank">03</span>',
     "G3d: Leseliste 03")

# --- G4a: Button in 11-OH-Box ---
repl(
    "      <b>Immer mit der kleinstm\u00f6glichen Portion starten und mindestens 2h warten.</b>\n    </div>",
    "      <b>Immer mit der kleinstm\u00f6glichen Portion starten und mindestens 2h warten.</b><br>\n"
    "      <span onclick=\"gotoLexCat('cannabinoide')\" style=\"display:inline-block;margin-top:8px;cursor:pointer;font-size:var(--fs-xs);color:#e07070;border:1px solid #c0392b;border-radius:20px;padding:3px 10px\">\U0001F4D6 Mehr im Lexikon: 11-OH-THC \u2192</span>\n    </div>",
    "G4a: Button 11-OH-Box"
)

# --- G4b: Button in Toleranz-Box ---
repl(
    '<span id="r-tol-text">\u2014</span></div>',
    '<span id="r-tol-text">\u2014</span><br><span onclick="gotoLexCat(\'risiken\')" style="display:inline-block;margin-top:6px;cursor:pointer;font-size:var(--fs-xs);color:var(--warn);border:1px solid var(--warn);border-radius:20px;padding:3px 10px">\U0001F4D6 Mehr: Toleranz \u2192</span></div>',
    "G4b: Button Toleranz-Box"
)

for n in notes: print(" ", n)
if s != orig:
    io.open(PATH, "w", encoding="utf-8").write(s)
    print("Patch G geschrieben.")
else:
    print("Patch G: keine Änderung (idempotent).")
