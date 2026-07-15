#!/usr/bin/env python3
# Patch N: "Prävention" als UI-Label (Nav-Tab, Startseiten-Kachel, Methoden-Button)
# durch "Know before you go" ersetzt. Betrifft NICHT den Untertitel oder den
# Fliesstext (dort bleibt "Prävention" als normales Wort stehen).
# Behebt zugleich das Flackern im Nav-Tab beim Laden: die I18N-Variable, die
# den Text nach dem initialen HTML ueberschreibt, wird auf denselben Wert gesetzt.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 4

# ─────────────────────────────────────────────────────────────────────────
# 1) Startseiten-Kachel (CannGuide-Box)
# ─────────────────────────────────────────────────────────────────────────
old1 = """      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">⛨ <b>Prävention</b><br><span style="color:var(--text3)">DACH Anlaufstellen</span></div>"""
new1 = """      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">⛨ <b>Know before you go</b><br><span style="color:var(--text3)">DACH Anlaufstellen</span></div>"""

if old1 not in content:
    print("WARNUNG 1: Startseiten-Kachel nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Startseiten-Kachel 'Prävention' -> 'Know before you go'.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Methoden-Seite: Button unten
# ─────────────────────────────────────────────────────────────────────────
old2 = """    <button class="btn" onclick="showPage('safety')" style="background:#4a1d6e;border-color:#7b2fc4;color:#e0aaff">⛨ Prävention</button>"""
new2 = """    <button class="btn" onclick="showPage('safety')" style="background:#4a1d6e;border-color:#7b2fc4;color:#e0aaff">⛨ Know before you go</button>"""

if old2 not in content:
    print("WARNUNG 2: Methoden-Button nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Methoden-Button 'Prävention' -> 'Know before you go'.")

# ─────────────────────────────────────────────────────────────────────────
# 3) I18N: prevention/prevention2 -- behebt das Flackern im Nav-Tab
#    (Startwert im HTML und der per JS nachgeladene Wert stimmen jetzt ueberein)
# ─────────────────────────────────────────────────────────────────────────
old3 = """    charges:'Chargen', prevention:'Prävention', design:'Design',"""
new3 = """    charges:'Chargen', prevention:'Know before you go', design:'Design',"""

old3b = """    newCharge:'+ Neue Charge', dosCalc:'∑ Dosierungsrechner', prevention2:'⛨ Prävention',"""
new3b = """    newCharge:'+ Neue Charge', dosCalc:'∑ Dosierungsrechner', prevention2:'⛨ Know before you go',"""

if old3 not in content or old3b not in content:
    print("WARNUNG 3: I18N.de prevention/prevention2 nicht (vollständig) gefunden.")
else:
    content = content.replace(old3, new3).replace(old3b, new3b)
    changes += 1
    print(f"3/{total}: I18N (DE) prevention/prevention2 -> 'Know before you go' — Flackern im Tab behoben.")

# ─────────────────────────────────────────────────────────────────────────
# 4) I18N: englische Version zur Konsistenz mitgezogen
# ─────────────────────────────────────────────────────────────────────────
old4 = """    charges:'Batches', prevention:'Prevention', design:'Design',"""
new4 = """    charges:'Batches', prevention:'Know before you go', design:'Design',"""

old4b = """    newCharge:'+ New Batch', dosCalc:'∑ Dosage Calculator', prevention2:'⛨ Prevention',"""
new4b = """    newCharge:'+ New Batch', dosCalc:'∑ Dosage Calculator', prevention2:'⛨ Know before you go',"""

if old4 not in content or old4b not in content:
    print("WARNUNG 4: I18N.en prevention/prevention2 nicht (vollständig) gefunden.")
else:
    content = content.replace(old4, new4).replace(old4b, new4b)
    changes += 1
    print(f"4/{total}: I18N (EN) prevention/prevention2 ebenfalls angeglichen.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
