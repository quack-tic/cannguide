#!/usr/bin/env python3
# Patch B (optional) — Faustregeln zur Inhalations-Dosis in den Praeventionsteil.
# Rettet die brauchbare mg/Zug-Orientierung aus der entfernten #inhale-puff-info
# als neuen Eintrag in SAFETY.lunge ("Konsum & Lunge"). BEWUSST als Faustregel
# formuliert, nicht als mg-genaue Rechnung.
#
# HINWEIS: Der Text ist aus bestehendem App-Inhalt uebernommen (deine Stimme),
# aber bitte vor dem Commit gegenlesen -> HR-Inhalt liegt bei dir.
import io

PATH = "index.html"
s = io.open(PATH, encoding="utf-8").read()

anchor = "  lunge:{cat:'Konsum & Lunge',icon:'\U0001F4A8',items:[\n"
new_item = (
    "    {t:'Faustregeln \u2013 Dosis pro Zug',b:'Beim Inhalieren l\u00e4sst sich die aufgenommene Menge "
    "<b>nicht mg-genau berechnen</b> \u2013 sie h\u00e4ngt von Zugtechnik, Ger\u00e4t und Material ab. "
    "Als grobe Orientierung enth\u00e4lt ein Zug bei Bl\u00fcten ~0.5\u20132\u00a0mg THC, beim Vaporizer ~1\u20134\u00a0mg, "
    "beim Dab ~3\u201310\u00a0mg. Einordnung der Wirkung: unter ~1.5\u00a0mg = Schwellendosis (kaum sp\u00fcrbar), "
    "~1.5\u20134\u00a0mg = niedrig und gut kontrollierbar, ~4\u20138\u00a0mg = mittel, ab ~8\u00a0mg = stark (nur Erfahrene), "
    "ab ~15\u00a0mg = Extrembereich. <b>Ein Zug, dann warten:</b> Onset 30\u201390\u00a0Sek \u2013 nach dem ersten Zug "
    "einsch\u00e4tzen, bevor nachgelegt wird. L\u00e4ngeres Luftanhalten bringt kein zus\u00e4tzliches THC.'},\n"
)

if "Faustregeln \u2013 Dosis pro Zug" in s:
    print("  [skip] B: Faustregel-Eintrag bereits vorhanden.")
elif anchor in s:
    s = s.replace(anchor, anchor + new_item, 1)
    io.open(PATH, "w", encoding="utf-8").write(s)
    print("  [ok]   B: Faustregel-Eintrag in SAFETY.lunge eingefügt.")
    print("Patch B geschrieben.")
else:
    print("  [WARN] B: Anker 'lunge:{...}' nicht gefunden -> manuell pruefen.")
