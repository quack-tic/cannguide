#!/usr/bin/env python3
# Patch J: 1) Prävention-Box (.pp-hero h2, .pp-rule b) bekommt feste Textfarbe
#             (var(--pp-text)) statt globaler --text -- behebt Kontrastbruch im Hellmodus.
#          2) Bibliothekstexte (.le-body) von --text3 (zu blass, für Meta gedacht)
#             auf --text2 angehoben -- betrifft ALLE Bibliotheks-Eintraege, nicht nur
#             die Vertiefungsartikel.
#          3) Tab-Label "Vertiefung" -> "Vertiefungsartikel" (einheitlich mit Ueberschrift).
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 3

# ─────────────────────────────────────────────────────────────────────────
# 1) Praevention-Box: h2-Titel und Regel-Labels bekommen feste, zum
#    fest-dunklen Lila-Hintergrund passende Farbe (unabhaengig vom Hell/Dunkel-Modus)
# ─────────────────────────────────────────────────────────────────────────
old1 = """.pp-hero h2{font-size:20px;font-weight:600;line-height:1.22;margin-bottom:.5rem;letter-spacing:-0.01em}"""
new1 = """.pp-hero h2{font-size:20px;font-weight:600;line-height:1.22;margin-bottom:.5rem;letter-spacing:-0.01em;color:var(--pp-text)}"""

old1b = """.pp-rule b{font-size:var(--fs);font-weight:600}"""
new1b = """.pp-rule b{font-size:var(--fs);font-weight:600;color:var(--pp-text)}"""

if old1 not in content or old1b not in content:
    print("WARNUNG 1: pp-hero/pp-rule CSS nicht (vollständig) gefunden.")
else:
    content = content.replace(old1, new1).replace(old1b, new1b)
    changes += 1
    print(f"1/{total}: Prävention-Box: Titel & Regel-Labels haben jetzt feste Farbe (var(--pp-text)) — kein Kontrastbruch mehr im Hellmodus.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Bibliothekstexte lesbarer: --text3 (zu blass, fuer Meta gedacht) -> --text2
# ─────────────────────────────────────────────────────────────────────────
old2 = """.le-body{font-size:var(--fs);color:var(--text3);line-height:1.75;display:none;padding-top:8px}"""
new2 = """.le-body{font-size:var(--fs);color:var(--text2);line-height:1.75;display:none;padding-top:8px}"""

if old2 not in content:
    print("WARNUNG 2: .le-body CSS nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Bibliothekstexte (.le-body) von --text3 auf --text2 angehoben — betrifft alle Einträge, nicht nur Vertiefungsartikel.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Tab-Label vereinheitlichen: "Vertiefung" -> "Vertiefungsartikel"
# ─────────────────────────────────────────────────────────────────────────
old3 = """artikel:'📰 Vertiefung'};"""
new3 = """artikel:'📰 Vertiefungsartikel'};"""

if old3 not in content:
    print("WARNUNG 3: Tab-Label 'Vertiefung' nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: Tab-Label vereinheitlicht zu 'Vertiefungsartikel'.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
