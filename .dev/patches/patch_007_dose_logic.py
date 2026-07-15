#!/usr/bin/env python3
# Patch 2 — Dosis-Logik: absolute Startdosen (MacCallum & Russo 2018) statt
# körpergewichtsbasiert, und die beiden Empfehlungs-Boxen gegenseitig ausschliessen.
#
#  #2  bw*0.05*sexF (an ZWEI Stellen) -> feste absolute Werte.
#  #3  r-kg-box (Startdosis) und r-tol-box (Toleranz) dürfen nicht gleichzeitig
#      erscheinen. Neue Regel: Startdosis nur bei tolFactor===1.0,
#      Toleranz-Box nur bei tolFactor>1.0 -> disjunkt.
import io

PATH = "index.html"
with io.open(PATH, encoding="utf-8") as f:
    src = f.read()

changed = False

# --- 2a: Toleranz-Zweig auf absolute tolBase reduzieren (bw-Zweig raus) ---
old_tol = (
    "  var ppTol = 0;\n"
    "  if(tolFactor>1.0) {\n"
    "    if(bw>0) {\n"
    "      var startD = bw * 0.05 * sexF;\n"
    "      ppTol = Math.round(startD * tolFactor * 10) / 10;\n"
    "    } else {\n"
    "      var tolBase = {1.3: 7.5, 1.7: 12, 2.2: 18};\n"
    "      ppTol = tolBase[tolFactor] || 10;\n"
    "    }\n"
    "  }"
)
new_tol = (
    "  var ppTol = 0;\n"
    "  if(tolFactor>1.0) {\n"
    "    // Absolute, gerätunabhängige Richtwerte (nicht koerpergewichtsbasiert).\n"
    "    var tolBase = {1.3: 7.5, 1.7: 12, 2.2: 18};\n"
    "    ppTol = tolBase[tolFactor] || 10;\n"
    "  }"
)
if "if(bw>0) {\n      var startD = bw * 0.05 * sexF;" not in src:
    print("  [skip] 2a: Toleranz-Zweig bereits absolut.")
elif old_tol in src:
    src = src.replace(old_tol, new_tol, 1)
    changed = True
    print("  [ok]   2a: Toleranz-Dosis jetzt absolut.")
else:
    print("  [WARN] 2a: Toleranz-Block nicht exakt gefunden -> manuell pruefen.")

# --- 2b: Startdosis-Box absolut + gegenseitig ausschliessend ---
old_kg = (
    "  if(bw > 0 && kgBox && kgEl) {\n"
    "\n"
    "    var startDose = Math.round(bw * 0.05 * sexF * 10) / 10;\n"
    "    var modDose = Math.round(bw * 0.1 * sexF * 10) / 10;\n"
    "    kgBox.style.display = 'block';\n"
    "    kgEl.innerHTML = '~'+startDose + ' mg <span style=\"font-size:11px;color:var(--text3)\">(bis ~' + modDose + ' mg erfahren)</span>';\n"
    "  } else if(kgBox) {"
)
new_kg = (
    "  // Absolute Startdosis (MacCallum & Russo 2018); nur ohne Toleranz anzeigen,\n"
    "  // damit sie sich nicht mit der Toleranz-Box widerspricht.\n"
    "  if(tolFactor === 1.0 && kgBox && kgEl) {\n"
    "    kgBox.style.display = 'block';\n"
    "    kgEl.innerHTML = '~2.5 mg <span style=\"font-size:11px;color:var(--text3)\">(vorsichtig bis ~5 mg, langsam titrieren)</span>';\n"
    "  } else if(kgBox) {"
)
if "kgEl.innerHTML = '~2.5 mg" in src:
    print("  [skip] 2b: Startdosis-Box bereits absolut.")
elif old_kg in src:
    src = src.replace(old_kg, new_kg, 1)
    changed = True
    print("  [ok]   2b: Startdosis-Box absolut + exklusiv.")
else:
    print("  [WARN] 2b: kg-Box-Block nicht exakt gefunden -> manuell pruefen.")

if changed:
    with io.open(PATH, "w", encoding="utf-8") as f:
        f.write(src)
    print("Patch 2 geschrieben.")
else:
    print("Patch 2: keine Änderung (idempotent).")
