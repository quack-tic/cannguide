#!/usr/bin/env python3
# Patch 044: Alle bisher als reiner Text genannten Web-Adressen werden zu
# echten <a>-Links -- antippbar, oeffnen in neuem Tab, mit
# event.stopPropagation(), damit der Tap NICHT gleichzeitig den umgebenden
# Akkordeon-Eintrag (.le, onclick=toggleEntry) schliesst.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 6

def link(url, label=None):
    label = label or url
    return ('<a href="https://'+url+'" target="_blank" rel="noopener" '
            'onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">'+label+'</a>')

# ─────────────────────────────────────────────────────────────────────────
# 1) Anlaufstellen: Schweiz
# ─────────────────────────────────────────────────────────────────────────
old1 = """{t:'🇨🇭 Schweiz',b:'Sanität <b>144</b> · Tox Info <b>145</b> · Dargebotene Hand <b>143</b><br>suchtschweiz.ch · infodrog.ch · feel-ok.ch/cannabis'},"""
new1 = ("{t:'🇨🇭 Schweiz',b:'Sanität <b>144</b> · Tox Info <b>145</b> · Dargebotene Hand <b>143</b><br>"
        + link("www.suchtschweiz.ch", "suchtschweiz.ch") + " · "
        + link("www.infodrog.ch", "infodrog.ch") + " · "
        + link("www.feel-ok.ch/cannabis", "feel-ok.ch/cannabis") + "'},")

if old1 not in content:
    print("WARNUNG 1: Schweiz-Anlaufstellen-Eintrag nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Schweiz-Links (suchtschweiz.ch, infodrog.ch, feel-ok.ch) verlinkt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Anlaufstellen: Deutschland
# ─────────────────────────────────────────────────────────────────────────
old2 = """{t:'🇩🇪 Deutschland',b:'Notruf <b>112</b> · Telefonseelsorge <b>0800 111 0 111</b><br>bzga.de · drugcom.de · quittheshit.net<br>CanG (2024): 25g/50g/3 Pflanzen (18+).'},"""
new2 = ("{t:'🇩🇪 Deutschland',b:'Notruf <b>112</b> · Telefonseelsorge <b>0800 111 0 111</b><br>"
        + link("www.bzga.de", "bzga.de") + " · "
        + link("www.drugcom.de", "drugcom.de") + " · "
        + link("www.quittheshit.net", "quittheshit.net")
        + "<br>CanG (2024): 25g/50g/3 Pflanzen (18+).'},")

if old2 not in content:
    print("WARNUNG 2: Deutschland-Anlaufstellen-Eintrag nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Deutschland-Links (bzga.de, drugcom.de, quittheshit.net) verlinkt.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Anlaufstellen: Österreich
# ─────────────────────────────────────────────────────────────────────────
old3 = """{t:'🇦🇹 Österreich',b:'Sanität <b>144</b> · Vergiftung <b>01 406 43 43</b> · Seelsorge <b>142</b><br>suchtvorbeugung.at · gruenerkreis.at'},"""
new3 = ("{t:'🇦🇹 Österreich',b:'Sanität <b>144</b> · Vergiftung <b>01 406 43 43</b> · Seelsorge <b>142</b><br>"
        + link("www.suchtvorbeugung.at", "suchtvorbeugung.at") + " · "
        + link("www.gruenerkreis.at", "gruenerkreis.at") + "'},")

if old3 not in content:
    print("WARNUNG 3: Österreich-Anlaufstellen-Eintrag nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: Österreich-Links (suchtvorbeugung.at, gruenerkreis.at) verlinkt.")

# ─────────────────────────────────────────────────────────────────────────
# 4) Anlaufstellen: International
# ─────────────────────────────────────────────────────────────────────────
old4 = """{t:'🌍 International',b:'TripSit: tripsit.me · DanceSafe: dancesafe.org<br>CUDIT / ASSIST (WHO)'}"""
new4 = ("{t:'🌍 International',b:'TripSit: "
        + link("tripsit.me") + " · DanceSafe: "
        + link("dancesafe.org") + "<br>CUDIT / ASSIST (WHO)'}")

if old4 not in content:
    print("WARNUNG 4: International-Anlaufstellen-Eintrag nicht gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: International-Links (tripsit.me, dancesafe.org) verlinkt.")

# ─────────────────────────────────────────────────────────────────────────
# 5) Sucht & Hilfe: "Hilfe holen" (quittheshit.net)
# ─────────────────────────────────────────────────────────────────────────
old5 = """{t:'Hilfe holen',b:'Kognitive Verhaltenstherapie (CBT) ist bei CUD evidenzbasiert wirksam. Quit the Shit: quittheshit.net — kostenlos, anonym, ohne Anmeldung. Suchtberatung ist vertraulich — kein Strafverfolgungsrisiko. Es braucht keine Abhängigkeitsdiagnose für Beratung; wer unsicher ist, ist willkommen.'}"""
new5 = ("{t:'Hilfe holen',b:'Kognitive Verhaltenstherapie (CBT) ist bei CUD evidenzbasiert wirksam. Quit the Shit: "
        + link("www.quittheshit.net", "quittheshit.net")
        + " — kostenlos, anonym, ohne Anmeldung. Suchtberatung ist vertraulich — kein Strafverfolgungsrisiko. Es braucht keine Abhängigkeitsdiagnose für Beratung; wer unsicher ist, ist willkommen.'}")

if old5 not in content:
    print("WARNUNG 5: 'Hilfe holen'-Eintrag nicht gefunden.")
else:
    content = content.replace(old5, new5)
    changes += 1
    print(f"5/{total}: 'Hilfe holen'-Link (quittheshit.net) verlinkt.")

# ─────────────────────────────────────────────────────────────────────────
# 6) Kontrolle behalten: "Hilfe" (quittheshit.net)
# ─────────────────────────────────────────────────────────────────────────
old6 = """{t:'Hilfe',b:'CBT evidenzbasiert. Quit the Shit: quittheshit.net — kostenlos, anonym.'}"""
new6 = ("{t:'Hilfe',b:'CBT evidenzbasiert. Quit the Shit: "
        + link("www.quittheshit.net", "quittheshit.net") + " — kostenlos, anonym.'}")

if old6 not in content:
    print("WARNUNG 6: 'Hilfe'-Eintrag (Kontrolle behalten) nicht gefunden.")
else:
    content = content.replace(old6, new6)
    changes += 1
    print(f"6/{total}: 'Hilfe'-Link (Kontrolle behalten, quittheshit.net) verlinkt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
