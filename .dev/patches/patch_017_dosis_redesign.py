#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Patch E — Ergebnis-Block neu:
#  * Einstiegsdosis IMMER sichtbar (Grundempfehlung, absolut n. MacCallum & Russo).
#    Klar als aufgenommenes Delta-9-THC beschriftet (oral wirksam als 11-OH).
#    Variante 2: keine Sex-Eingabe, Hinweis "empfindliche Personen tiefer".
#  * Toleranz-Box wird von "Empf. Dosis" zu einem praeventiven HINWEIS umgebaut:
#    zeigt zusaetzlich (nicht ersetzend) den moeglichen Bereich, explizit
#    "keine Empfehlung". Beides gleichzeitig sichtbar.
import io

PATH = "index.html"
s = io.open(PATH, encoding="utf-8").read()
orig = s
notes = []
DASH = "\u2014"  # em dash

def repl(old, new, label):
    global s
    if old in s:
        s = s.replace(old, new, 1); notes.append("[ok]   %s." % label)
    elif new.split(">")[0] in s and old not in s:
        notes.append("[skip] %s (bereits erledigt)." % label)
    else:
        notes.append("[WARN] %s: Ziel nicht gefunden -> manuell pruefen." % label)

# --- E1: HTML r-tol-box -> praeventiver Hinweis-Block (full width) ---
repl(
    '    <div class="rm" id="r-tol-box" style="display:none"><div class="rl">Empf. Dosis bei Toleranz (Delta-9)</div><div class="rv am" id="r-tol">' + DASH + '</div></div>',
    '    <div id="r-tol-box" style="display:none;grid-column:1/-1;background:var(--warn-bg);border:1px solid var(--warn);border-radius:var(--radius);padding:10px 12px;font-size:var(--fs-sm);color:var(--warn);line-height:1.65">\u26a0\ufe0f <b>Hinweis bei angegebener Toleranz</b> (<span id="r-tol-lvl">' + DASH + '</span>)<br><span id="r-tol-text">' + DASH + '</span></div>',
    "E1: r-tol-box HTML -> Hinweis"
)

# --- E2: HTML r-kg-box Label ---
repl(
    '<div class="rl">Empf. Startdosis (Delta-9)</div>',
    '<div class="rl">Empf. Einstiegsdosis (Delta-9, oral)</div>',
    "E2: r-kg-box Label"
)

# --- E3: JS r-tol Befuellung ---
repl(
    "  var tolEl=document.getElementById('r-tol');\n"
    "  if(tolFactor>1.0&&tolEl) tolEl.textContent='~'+ppTol.toFixed(1)+' mg';",
    "  var tolTextEl=document.getElementById('r-tol-text');\n"
    "  var tolLvlEl=document.getElementById('r-tol-lvl');\n"
    "  if(tolFactor>1.0 && tolTextEl) {\n"
    "    var _tolSel=document.getElementById('tolerance');\n"
    "    if(tolLvlEl) tolLvlEl.textContent=_tolSel.options[_tolSel.selectedIndex].text;\n"
    "    tolTextEl.innerHTML='Bei bestehender Toleranz kann f\u00fcr einen sp\u00fcrbaren Wirkungseintritt mehr n\u00f6tig sein \u2014 erfahrungsgem\u00e4ss bis ~'+ppTol+' mg. <b>Das ist keine Empfehlung.</b> H\u00f6here Dosen steigern Risiko und Toleranz weiter; eine Konsumpause (T-Break) senkt den Bedarf wieder.';\n"
    "  }",
    "E3: r-tol Befuellung"
)

# --- E4: JS kg-Block -> immer sichtbar, Delta-9/11-OH beschriftet ---
repl(
    "  // Absolute Startdosis (MacCallum & Russo 2018); nur ohne Toleranz anzeigen,\n"
    "  // damit sie sich nicht mit der Toleranz-Box widerspricht.\n"
    "  if(tolFactor === 1.0 && kgBox && kgEl) {\n"
    "    kgBox.style.display = 'block';\n"
    "    kgEl.innerHTML = '~2.5 mg <span style=\"font-size:11px;color:var(--text3)\">(vorsichtig bis ~5 mg, langsam titrieren)</span>';\n"
    "  } else if(kgBox) {\n"
    "    kgBox.style.display = 'none';\n"
    "  }",
    "  // Einstiegsdosis (MacCallum & Russo 2018): absolut, immer sichtbar als Grundempfehlung.\n"
    "  if(kgBox && kgEl) {\n"
    "    kgBox.style.display = 'block';\n"
    "    kgEl.innerHTML = '~2.5 mg <span style=\"font-size:11px;color:var(--text3)\">Delta-9-THC aufgenommen \u00b7 oral wirksam als 11-OH \u00b7 bis ~5 mg langsam titrieren<br>empfindliche Personen (tendenziell \u2640) tiefer ansetzen</span>';\n"
    "  }",
    "E4: kg-Block immer sichtbar"
)

for n in notes: print(" ", n)
if s != orig:
    io.open(PATH, "w", encoding="utf-8").write(s)
    print("Patch E geschrieben.")
else:
    print("Patch E: keine Änderung (idempotent).")
