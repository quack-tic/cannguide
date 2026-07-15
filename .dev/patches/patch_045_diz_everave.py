#!/usr/bin/env python3
# Patch 045: Ergaenzt DIZ (Drogeninformationszentrum Stadt Zuerich, ueber
# Saferparty.ch als Landingpage) und das Eve & Rave Forum unter der
# Schweizer Anlaufstelle. Setzt Patch 044 (klickbare Links) voraus.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """{t:'🇨🇭 Schweiz',b:'Sanität <b>144</b> · Tox Info <b>145</b> · Dargebotene Hand <b>143</b><br><a href="https://www.suchtschweiz.ch" target="_blank" rel="noopener" onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">suchtschweiz.ch</a> · <a href="https://www.infodrog.ch" target="_blank" rel="noopener" onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">infodrog.ch</a> · <a href="https://www.feel-ok.ch/cannabis" target="_blank" rel="noopener" onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">feel-ok.ch/cannabis</a>'},"""

new1 = """{t:'🇨🇭 Schweiz',b:'Sanität <b>144</b> · Tox Info <b>145</b> · Dargebotene Hand <b>143</b><br><a href="https://www.suchtschweiz.ch" target="_blank" rel="noopener" onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">suchtschweiz.ch</a> · <a href="https://www.infodrog.ch" target="_blank" rel="noopener" onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">infodrog.ch</a> · <a href="https://www.feel-ok.ch/cannabis" target="_blank" rel="noopener" onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">feel-ok.ch/cannabis</a><br>DIZ (Drogeninformationszentrum Zürich): <a href="https://www.saferparty.ch/angebote/beratung-und-therapieangebote" target="_blank" rel="noopener" onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">saferparty.ch</a> · <a href="https://forum.eve-rave.ch/" target="_blank" rel="noopener" onclick="event.stopPropagation()" style="color:inherit;text-decoration:underline">Eve & Rave Forum</a>'},"""

if old1 not in content:
    print("WARNUNG 1: Schweiz-Anlaufstellen-Eintrag nicht (exakt) gefunden — evtl. Patch 044 noch nicht angewendet?")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: DIZ/Saferparty.ch und Eve & Rave Forum unter Schweiz ergänzt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — Reihenfolge prüfen (Patch 044 muss vorher gelaufen sein)!")
