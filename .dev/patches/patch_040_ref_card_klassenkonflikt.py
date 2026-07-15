#!/usr/bin/env python3
# Patch 040: Klassennamen-Kollision behoben.
# Die generische Klasse ".tg" (fuer Dosierungs-Intensitaets-Tags im Rechner,
# z.B. <span class="tag tg">Niedrig</span>) kollidierte mit der gleichnamigen
# Klasse in den Wirkstoffe-Kacheln (<div class="tg">Psychoaktiv · Rausch</div>).
# Da CSS pro Eigenschaft kaskadiert, rutschte "background:var(--accent-bg)"
# aus der generischen Regel durch, obwohl ".ref-card .tg" spezifischer ist --
# das erzeugte einen unbeabsichtigten dunklen Kasten hinter dem Beschreibungs-
# text auf der Startseite, in jedem Browser und Modus.
# Fix: Die Wirkstoffe-Kachel-Klasse wird von "tg" auf "desc" umbenannt, damit
# sie nicht mehr mit der Dosierungs-Tag-Klasse kollidiert.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 5

# ─────────────────────────────────────────────────────────────────────────
# 1) CSS-Selektor umbenennen
# ─────────────────────────────────────────────────────────────────────────
old1 = """.ref-card .tg{font-size:var(--fs-xs);color:var(--text3)}"""
new1 = """.ref-card .desc{font-size:var(--fs-xs);color:var(--text3)}"""

if old1 not in content:
    print("WARNUNG 1: .ref-card .tg CSS nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: CSS-Selektor .ref-card .tg -> .ref-card .desc umbenannt.")

# ─────────────────────────────────────────────────────────────────────────
# 2-5) HTML: die 4 Wirkstoffe-Kacheln (THC, CBD, CBN, CBG) bekommen die
#      neue Klasse statt der kollidierenden "tg"
# ─────────────────────────────────────────────────────────────────────────
pairs = [
    ('<div class="k">THC</div><div class="nm">Δ9-THC</div><div class="tg">Psychoaktiv · Rausch</div>',
     '<div class="k">THC</div><div class="nm">Δ9-THC</div><div class="desc">Psychoaktiv · Rausch</div>'),
    ('<div class="k">CBD</div><div class="nm">Cannabidiol</div><div class="tg">Nicht berauschend</div>',
     '<div class="k">CBD</div><div class="nm">Cannabidiol</div><div class="desc">Nicht berauschend</div>'),
    ('<div class="k">CBN</div><div class="nm">Cannabinol</div><div class="tg">Schwach sedierend</div>',
     '<div class="k">CBN</div><div class="nm">Cannabinol</div><div class="desc">Schwach sedierend</div>'),
    ('<div class="k">CBG</div><div class="nm">Cannabigerol</div><div class="tg">Vorstufe (Mutter)</div>',
     '<div class="k">CBG</div><div class="nm">Cannabigerol</div><div class="desc">Vorstufe (Mutter)</div>'),
]

for i, (old, new) in enumerate(pairs, start=2):
    if old not in content:
        print(f"WARNUNG {i}: Wirkstoffe-Kachel #{i-1} nicht (exakt) gefunden.")
    else:
        content = content.replace(old, new)
        changes += 1
        print(f"{i}/{total}: Wirkstoffe-Kachel #{i-1} auf Klasse 'desc' umgestellt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
