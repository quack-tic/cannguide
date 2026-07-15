#!/usr/bin/env python3
# Patch 054: Die beiden Charts "Dosis über Zeit" und "Medien-Verteilung" in
# der Chargenverwaltung standen als starres 2-Spalten-Grid (grid-template-
# columns:1fr 1fr) ohne Media Query. Auf schmalen Bildschirmen (Handy)
# passte das nicht in den Viewport, wodurch der Browser die ganze Seite
# verkleinert dargestellt hat, statt die Karten untereinander zu stapeln.
# Fix: eigene Klasse mit Media Query (Breakpoint 520px, konsistent mit dem
# bereits vorhandenen .ref-grid-Breakpoint) -- unter 520px wird aus dem
# 2-Spalten-Grid ein 1-Spalten-Grid (Karten stapeln sich).
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

# ─────────────────────────────────────────────────────────────────────────
# 1) CSS: Klasse + Media Query ergaenzen
# ─────────────────────────────────────────────────────────────────────────
old1 = """@media(max-width:520px){.ref-grid{grid-template-columns:1fr 1fr}}"""
new1 = """@media(max-width:520px){.ref-grid{grid-template-columns:1fr 1fr}}
.dash-charts-row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px}
@media(max-width:520px){.dash-charts-row{grid-template-columns:1fr}}"""

if old1 not in content:
    print("WARNUNG 1: Bestehende .ref-grid Media-Query-Zeile nicht gefunden — Einfügepunkt fehlt.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: CSS-Klasse '.dash-charts-row' mit Mobile-Breakpoint (520px) ergänzt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) HTML: inline grid-style durch die neue Klasse ersetzen
# ─────────────────────────────────────────────────────────────────────────
old2 = """    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
      <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1rem">
        <div style="font-size:var(--fs-xs);color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.625rem">Dosis über Zeit</div>
        <div style="position:relative;height:160px;width:100%"><canvas id="chart-dose"></canvas></div>
      </div>
      <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1rem">
        <div style="font-size:var(--fs-xs);color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.625rem">Medien-Verteilung</div>
        <div style="position:relative;height:160px;width:100%"><canvas id="chart-medium"></canvas></div>
      </div>
    </div>"""

new2 = """    <div class="dash-charts-row">
      <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1rem">
        <div style="font-size:var(--fs-xs);color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.625rem">Dosis über Zeit</div>
        <div style="position:relative;height:160px;width:100%"><canvas id="chart-dose"></canvas></div>
      </div>
      <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1rem">
        <div style="font-size:var(--fs-xs);color:var(--text3);text-transform:uppercase;letter-spacing:.06em;margin-bottom:.625rem">Medien-Verteilung</div>
        <div style="position:relative;height:160px;width:100%"><canvas id="chart-medium"></canvas></div>
      </div>
    </div>"""

if old2 not in content:
    print("WARNUNG 2: Chart-Grid-Block nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Chart-Grid nutzt jetzt die responsive Klasse statt starrem Inline-Grid.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
