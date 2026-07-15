#!/usr/bin/env python3
# Patch T: Rechner-Feinschliff vor der Tour.
# 1) Decarb-Options-Text "Ja - aktives (Total-)THC" / "Ja - bereits aktives THC"
#    -> einheitlich "Ja - aktives Material" (Bluetenmodus und Extraktmodus).
# 2) Label "Gramm pro Portion" -> "Gramm Wirkstofftraeger pro fertige Portion enthalten".
# 3) Konsumfrequenz (Toleranz) wird zur Pflichtauswahl, analog zum Decarb-Toggle.
# 4) Angepasste mg-Zahl im Toleranz-Hinweis wird grell hervorgehoben (Amber-Chip).
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 7

# ─────────────────────────────────────────────────────────────────────────
# 1a) Decarb-Optionstext Bluetenmodus
# ─────────────────────────────────────────────────────────────────────────
old1a = """<option value="yes">Ja – aktives (Total-)THC</option>"""
new1a = """<option value="yes">Ja – aktives Material</option>"""

if old1a not in content:
    print("WARNUNG 1a: Decarb-Options-Text (Blüten) nicht gefunden.")
else:
    content = content.replace(old1a, new1a)
    changes += 1
    print(f"1a/{total}: Blüten-Decarb-Option 'Ja – aktives Material'.")

# ─────────────────────────────────────────────────────────────────────────
# 1b) Decarb-Optionstext Extraktmodus
# ─────────────────────────────────────────────────────────────────────────
old1b = """<option value="yes">Ja – bereits aktives THC</option>"""
new1b = """<option value="yes">Ja – aktives Material</option>"""

if old1b not in content:
    print("WARNUNG 1b: Decarb-Options-Text (Extrakt) nicht gefunden.")
else:
    content = content.replace(old1b, new1b)
    changes += 1
    print(f"1b/{total}: Extrakt-Decarb-Option ebenfalls 'Ja – aktives Material'.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Label "Gramm pro Portion"
# ─────────────────────────────────────────────────────────────────────────
old2 = """<label class="cl">Gramm pro Portion</label>"""
new2 = """<label class="cl">Gramm Wirkstoffträger pro fertige Portion enthalten</label>"""

if old2 not in content:
    print("WARNUNG 2: Label 'Gramm pro Portion' nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Label präzisiert zu 'Gramm Wirkstoffträger pro fertige Portion enthalten'.")

# ─────────────────────────────────────────────────────────────────────────
# 3a) Toleranz-Dropdown: Platzhalter statt Vorauswahl (HTML)
# ─────────────────────────────────────────────────────────────────────────
old3a = """      <select id="tolerance" onchange="calcUpdate()">
        <option value="1.0">— Nicht berücksichtigen —</option>
        <option value="1.0">Gelegentlich (1× / Woche oder weniger)</option>
        <option value="1.3">Regelmässig (2–4× / Woche)</option>
        <option value="1.7">Täglich</option>
        <option value="2.2">Täglich mehrmals</option>
      </select>"""

new3a = """      <select id="tolerance" onchange="calcUpdate()">
        <option value="" selected disabled>— bitte wählen —</option>
        <option value="1.0">Gelegentlich (1× / Woche oder weniger)</option>
        <option value="1.3">Regelmässig (2–4× / Woche)</option>
        <option value="1.7">Täglich</option>
        <option value="2.2">Täglich mehrmals</option>
      </select>"""

if old3a not in content:
    print("WARNUNG 3a: Toleranz-Dropdown nicht (exakt) gefunden.")
else:
    content = content.replace(old3a, new3a)
    changes += 1
    print(f"3a/{total}: Toleranz-Dropdown hat jetzt Pflicht-Platzhalter statt Vorauswahl.")

# ─────────────────────────────────────────────────────────────────────────
# 3b) Validierung: fehlende Toleranz-Auswahl als Fehler behandeln
# ─────────────────────────────────────────────────────────────────────────
old3b = """  var tolFactor = parseFloat(document.getElementById('tolerance').value)||1.0;"""
new3b = """  var tolSel = document.getElementById('tolerance').value;
  var tolFactor = parseFloat(tolSel)||1.0;"""

old3c = """  if((calcMode==='extract'||calcMode==='raw') && decarbSel!=='yes' && decarbSel!=='no') errs.push('Decarboxylierung w\\u00e4hlen (Ja/Nein).');"""
new3c = """  if((calcMode==='extract'||calcMode==='raw') && decarbSel!=='yes' && decarbSel!=='no') errs.push('Decarboxylierung w\\u00e4hlen (Ja/Nein).');
  if(tolSel==='') errs.push('Konsumfrequenz wählen.');"""

if old3b not in content:
    print("WARNUNG 3b: tolFactor-Zeile nicht gefunden.")
else:
    content = content.replace(old3b, new3b)
    changes += 1
    print(f"3b/{total}: tolSel erfasst, um fehlende Auswahl zu erkennen.")

if old3c not in content:
    print("WARNUNG 3c: Decarb-Validierungszeile nicht gefunden — Toleranz-Pflichtfeld nicht ergänzt.")
else:
    content = content.replace(old3c, new3c)
    changes += 1
    print(f"3c/{total}: Fehlende Konsumfrequenz-Auswahl wird jetzt als Eingabefehler angezeigt.")

# ─────────────────────────────────────────────────────────────────────────
# 4) Angepasste mg-Zahl im Toleranz-Hinweis grell hervorheben
# ─────────────────────────────────────────────────────────────────────────
old4 = """    tolTextEl.innerHTML='Bei bestehender Toleranz kann für einen spürbaren Wirkungseintritt mehr nötig sein — erfahrungsgemäss bis ~'+ppTol+' mg. <b>Das ist keine Empfehlung.</b> Höhere Dosen steigern Risiko und Toleranz weiter; eine Konsumpause (T-Break) senkt den Bedarf wieder.';"""

new4 = """    tolTextEl.innerHTML='Bei bestehender Toleranz kann für einen spürbaren Wirkungseintritt mehr nötig sein — erfahrungsgemäss bis <span style="background:var(--amber);color:#1a1200;font-weight:800;font-size:1.15em;padding:1px 8px;border-radius:6px;white-space:nowrap">~'+ppTol+' mg</span>. <b>Das ist keine Empfehlung.</b> Höhere Dosen steigern Risiko und Toleranz weiter; eine Konsumpause (T-Break) senkt den Bedarf wieder.';"""

if old4 not in content:
    print("WARNUNG 4: Toleranz-Text-Zeile nicht gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: mg-Zahl im Toleranz-Hinweis jetzt als greller Amber-Chip hervorgehoben.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Teilschritte angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
