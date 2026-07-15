#!/usr/bin/env python3
# Patch 046: Alle Telefonnummern (Notfallnummern, Anlaufstellen) werden zu
# echten tel:-Links. Auf dem Handy fragt das Betriebssystem dann direkt,
# ob angerufen werden soll. event.stopPropagation() verhindert, dass ein
# Tap zusaetzlich den umgebenden Akkordeon-Eintrag schliesst.
#
# Voraussetzung: Patch 044/045 (klickbare Web-Links, DIZ/Eve & Rave) sind
# bereits angewendet.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 5

def tel(number, display=None):
    display = display or number
    href = number.replace(' ', '')
    return ('<a href="tel:'+href+'" onclick="event.stopPropagation()" '
            'style="color:inherit;text-decoration:underline">'+display+'</a>')

# ─────────────────────────────────────────────────────────────────────────
# 1) Anlaufstellen: Schweiz (144, 145, 143)
# ─────────────────────────────────────────────────────────────────────────
old1 = """{t:'🇨🇭 Schweiz',b:'Sanität <b>144</b> · Tox Info <b>145</b> · Dargebotene Hand <b>143</b><br>"""
new1 = ("{t:'🇨🇭 Schweiz',b:'Sanität <b>" + tel("144") + "</b> · Tox Info <b>" + tel("145")
        + "</b> · Dargebotene Hand <b>" + tel("143") + "</b><br>")

if old1 not in content:
    print("WARNUNG 1: Schweiz-Anlaufstellen-Nummern nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Schweiz-Nummern (144, 145, 143) klickbar.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Anlaufstellen: Deutschland (112, 0800 111 0 111)
# ─────────────────────────────────────────────────────────────────────────
old2 = """{t:'🇩🇪 Deutschland',b:'Notruf <b>112</b> · Telefonseelsorge <b>0800 111 0 111</b><br>"""
new2 = ("{t:'🇩🇪 Deutschland',b:'Notruf <b>" + tel("112") + "</b> · Telefonseelsorge <b>"
        + tel("08001110111", "0800 111 0 111") + "</b><br>")

if old2 not in content:
    print("WARNUNG 2: Deutschland-Anlaufstellen-Nummern nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Deutschland-Nummern (112, 0800 111 0 111) klickbar.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Anlaufstellen: Österreich (144, 01 406 43 43, 142)
# ─────────────────────────────────────────────────────────────────────────
old3 = """{t:'🇦🇹 Österreich',b:'Sanität <b>144</b> · Vergiftung <b>01 406 43 43</b> · Seelsorge <b>142</b><br>"""
new3 = ("{t:'🇦🇹 Österreich',b:'Sanität <b>" + tel("144") + "</b> · Vergiftung <b>"
        + tel("014064343", "01 406 43 43") + "</b> · Seelsorge <b>" + tel("142") + "</b><br>")

if old3 not in content:
    print("WARNUNG 3: Österreich-Anlaufstellen-Nummern nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: Österreich-Nummern (144, 01 406 43 43, 142) klickbar.")

# ─────────────────────────────────────────────────────────────────────────
# 4) Notfallnummern-Box (immer sichtbar, renderSafety): CH/DE/AT
# ─────────────────────────────────────────────────────────────────────────
old4 = """    +'<span style="color:rgba(255,255,255,.75)">🇨🇭 CH: <b>144</b> · <b>145</b> Tox Info · <b>143</b> Dargebotene Hand</span><br>'
    +'<span style="color:rgba(255,255,255,.75)">🇩🇪 DE: <b>112</b> · <b>0800 111 0 111</b> Telefonseelsorge</span><br>'
    +'<span style="color:rgba(255,255,255,.75)">🇦🇹 AT: <b>144</b> · <b>142</b> Seelsorge · <b>01 406 43 43</b> Vergiftung</span></div>';"""

new4 = ("    +'<span style=\"color:rgba(255,255,255,.75)\">🇨🇭 CH: <b>" + tel("144") + "</b> · <b>" + tel("145")
        + "</b> Tox Info · <b>" + tel("143") + "</b> Dargebotene Hand</span><br>'\n"
        "    +'<span style=\"color:rgba(255,255,255,.75)\">🇩🇪 DE: <b>" + tel("112") + "</b> · <b>"
        + tel("08001110111", "0800 111 0 111") + "</b> Telefonseelsorge</span><br>'\n"
        "    +'<span style=\"color:rgba(255,255,255,.75)\">🇦🇹 AT: <b>" + tel("144") + "</b> · <b>" + tel("142")
        + "</b> Seelsorge · <b>" + tel("014064343", "01 406 43 43") + "</b> Vergiftung</span></div>';")

if old4 not in content:
    print("WARNUNG 4: Notfallnummern-Box nicht (exakt) gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: Notfallnummern-Box (immer sichtbar) — alle Nummern klickbar.")

# ─────────────────────────────────────────────────────────────────────────
# 5) CSS: sicherstellen, dass tel:-Links auch farblich zum jeweiligen
#    umgebenden Textblock passen (color:inherit ist schon inline gesetzt,
#    hier nur eine leichte Hover-Optik ergaenzt)
# ─────────────────────────────────────────────────────────────────────────
old5 = """</style>"""
new5 = """a[href^="tel:"]:active{opacity:.7}
</style>"""

if old5 not in content:
    print("WARNUNG 5: </style>-Ende nicht gefunden.")
else:
    content = content.replace(old5, new5, 1)
    changes += 1
    print(f"5/{total}: Kleine Tap-Feedback-Optik für tel:-Links ergänzt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
