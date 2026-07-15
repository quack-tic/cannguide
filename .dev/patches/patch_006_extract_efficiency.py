#!/usr/bin/env python3
# Patch 1 — Extrakt-Modus: Doppelabzug der Effizienz beheben.
# Im Extract-Modus ist rawMg = g*1000*pExt bereits der fertige Wirkstoffgehalt.
# Die Trägermedium-Effizienz e darf dann NICHT ein zweites Mal abgezogen werden.
# Fix: effektive Effizienz = 100% im Extract-Modus; Summary-Label entsprechend.
import sys, io

PATH = "index.html"
with io.open(PATH, encoding="utf-8") as f:
    src = f.read()

changed = False

# --- 1a: totMg-Berechnung ---
old_tot = "  var totMg = rawMg*(e/100);"
new_tot = (
    "  // Extrakt ist bereits der fertige Wirkstoff (decarbed, gelöst) -> keine Infusions-Effizienz.\n"
    "  var eEff = (calcMode==='extract') ? 100 : e;\n"
    "  var totMg = rawMg*(eEff/100);"
)
if "var eEff = (calcMode==='extract')" in src:
    print("  [skip] 1a: eEff bereits vorhanden.")
elif old_tot in src:
    src = src.replace(old_tot, new_tot, 1)
    changed = True
    print("  [ok]   1a: totMg nutzt jetzt eEff.")
else:
    print("  [WARN] 1a: Ziel 'var totMg = rawMg*(e/100);' nicht gefunden.")

# --- 1b: Summary-Label ---
old_lbl = "cs.innerHTML = desc+'<br>Nach Effizienz ('+e+'%): "
new_lbl = ("var effLabel = (calcMode==='extract') ? 'Extrakt bereits aktiv (100%)' : 'Nach Effizienz ('+eEff+'%)';\n"
           "  cs.innerHTML = desc+'<br>'+effLabel+': ")
if "var effLabel = (calcMode===" in src:
    print("  [skip] 1b: effLabel bereits vorhanden.")
elif old_lbl in src:
    src = src.replace(old_lbl, new_lbl, 1)
    changed = True
    print("  [ok]   1b: Summary-Label nutzt jetzt effLabel.")
else:
    print("  [WARN] 1b: Ziel-Label nicht gefunden.")

if changed:
    with io.open(PATH, "w", encoding="utf-8") as f:
        f.write(src)
    print("Patch 1 geschrieben.")
else:
    print("Patch 1: keine Änderung (idempotent).")
