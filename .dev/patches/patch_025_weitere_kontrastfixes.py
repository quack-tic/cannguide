#!/usr/bin/env python3
# Patch M: Weitere Stellen mit "fest-dunkler Hintergrund + moduswechselnde
# Textfarbe (var(--text2))" behoben -- selbes Bugmuster wie Patch J/L.
# Betroffen: Notfallnummern-Box, Praevention-Einleitungstext + Regel-Beschreibungen,
# Mythos-Zelle (linke, dunkle Seite von "Mythos vs. Fakt").
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 3

# ─────────────────────────────────────────────────────────────────────────
# 1) Notfallnummern-Box: die drei Telefonnummern-Zeilen bekommen feste,
#    zum fest-dunklen Warn-Hintergrund passende Farbe
# ─────────────────────────────────────────────────────────────────────────
old1 = """  h+='<div class="notfall-box"><b style="color:var(--warn)">🆘 Notfallnummern</b><br>'
    +'<span style="color:var(--text2)">🇨🇭 CH: <b>144</b> · <b>145</b> Tox Info · <b>143</b> Dargebotene Hand</span><br>'
    +'<span style="color:var(--text2)">🇩🇪 DE: <b>112</b> · <b>0800 111 0 111</b> Telefonseelsorge</span><br>'
    +'<span style="color:var(--text2)">🇦🇹 AT: <b>144</b> · <b>142</b> Seelsorge · <b>01 406 43 43</b> Vergiftung</span></div>';"""

new1 = """  h+='<div class="notfall-box"><b style="color:var(--warn)">🆘 Notfallnummern</b><br>'
    +'<span style="color:rgba(255,255,255,.75)">🇨🇭 CH: <b>144</b> · <b>145</b> Tox Info · <b>143</b> Dargebotene Hand</span><br>'
    +'<span style="color:rgba(255,255,255,.75)">🇩🇪 DE: <b>112</b> · <b>0800 111 0 111</b> Telefonseelsorge</span><br>'
    +'<span style="color:rgba(255,255,255,.75)">🇦🇹 AT: <b>144</b> · <b>142</b> Seelsorge · <b>01 406 43 43</b> Vergiftung</span></div>';"""

if old1 not in content:
    print("WARNUNG 1: Notfallnummern-Block nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Notfallnummern-Zeilen bekommen feste helle Farbe — lesbar unabhängig vom Hell/Dunkel-Modus.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Praevention-Box: Einleitungstext (.lede) und Regel-Beschreibungen (.tx)
# ─────────────────────────────────────────────────────────────────────────
old2 = """.pp-hero .lede{font-size:var(--fs-sm);color:var(--text2);line-height:1.6;margin-bottom:1.1rem;max-width:50ch}"""
new2 = """.pp-hero .lede{font-size:var(--fs-sm);color:var(--pp-text);opacity:.75;line-height:1.6;margin-bottom:1.1rem;max-width:50ch}"""

old2b = """.pp-rule .tx{font-size:var(--fs-sm);color:var(--text2);line-height:1.45}"""
new2b = """.pp-rule .tx{font-size:var(--fs-sm);color:var(--pp-text);opacity:.75;line-height:1.45}"""

if old2 not in content or old2b not in content:
    print("WARNUNG 2: .pp-hero .lede / .pp-rule .tx CSS nicht (vollständig) gefunden.")
else:
    content = content.replace(old2, new2).replace(old2b, new2b)
    changes += 1
    print(f"2/{total}: Prävention-Einleitungstext & Regel-Beschreibungen jetzt fest hell lesbar.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Mythos-Zelle (dunkle Seite): Fliesstext bekommt feste helle Farbe
# ─────────────────────────────────────────────────────────────────────────
old3 = """.myth-cell.m p{color:var(--text2)}"""
new3 = """.myth-cell.m p{color:rgba(255,255,255,.75)}"""

if old3 not in content:
    print("WARNUNG 3: .myth-cell.m p CSS nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: Mythos-Fliesstext (dunkle Zelle) jetzt fest hell lesbar.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
