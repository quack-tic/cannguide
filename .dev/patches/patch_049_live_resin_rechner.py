#!/usr/bin/env python3
# Patch 049: Live Resin als eigene, waehlbare Extrakt-Kategorien im Rechner
# ergaenzt (bisher nur Lexikon-Begriff, keine Rechner-Option). Drei Varianten
# je nach Herstellungsweg, mit von Adrian gegengeprueften Potenz-Bereichen:
#   - BHO Live Resin: 65-85% (Butan-Extraktion aus frisch gefrorenem Material)
#   - Live Rosin / Live Bubble Hash: 50-85% (loesungsmittelfrei, obere Grenze
#     angehoben fuer High-End Full-Melt-Qualitaeten)
#   - Live Dry Sift: 35-65% (Trockensieb aus gefrorenem Material)
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

# ─────────────────────────────────────────────────────────────────────────
# 1) Dropdown: neue Optgroup "Live-Extrakte (frisch gefroren)"
# ─────────────────────────────────────────────────────────────────────────
old1 = """<optgroup label="Lösungsmittelfrei"><option value="rosin">Rosin (60–80%)</option><option value="thca_k">THCA-Kristalle (95–99%)</option></optgroup>"""
new1 = """<optgroup label="Lösungsmittelfrei"><option value="rosin">Rosin (60–80%)</option><option value="thca_k">THCA-Kristalle (95–99%)</option></optgroup>
            <optgroup label="Live-Extrakte (frisch gefroren)"><option value="live_bho">Live Resin – BHO (65–85%)</option><option value="live_rosin">Live Rosin / Live Bubble Hash (50–85%)</option><option value="live_sift">Live Dry Sift (35–65%)</option></optgroup>"""

if old1 not in content:
    print("WARNUNG 1: Extrakt-Typ-Dropdown nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Neue Optgroup 'Live-Extrakte' (3 Varianten) im Dropdown ergänzt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) EXTRACT_CFG: Potenz-Bereiche für die 3 neuen Typen
# ─────────────────────────────────────────────────────────────────────────
old2 = """  kief:   {min:30,max:60,def:45,hint:'Kief / Pollen: 30–60%.'},"""
new2 = """  kief:   {min:30,max:60,def:45,hint:'Kief / Pollen: 30–60%.'},
  live_bho:   {min:65,max:85,def:75,hint:'Live Resin (BHO): Butan-Extraktion aus frisch gefrorenem Material, 65–85%.'},
  live_rosin: {min:50,max:85,def:70,hint:'Live Rosin / Live Bubble Hash: lösungsmittelfrei aus gefrorenem Material, 50–85%.'},
  live_sift:  {min:35,max:65,def:50,hint:'Live Dry Sift: Trockensieb aus gefrorenem Material, 35–65%.'},"""

if old2 not in content:
    print("WARNUNG 2: EXTRACT_CFG (kief-Eintrag) nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: EXTRACT_CFG um 3 Live-Extrakt-Varianten ergänzt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
