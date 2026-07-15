#!/usr/bin/env python3
# Patch 038: Rechner-Erweiterungen.
# 1) Einheiten-Umschalter (g<->kg bzw. ml<->l) fuer die drei Mengenfelder
#    (Eingesetzte Wirkstoffmenge, Traegermenge gesamt, Menge pro Portion).
#    Interne Berechnung bleibt in der Basiseinheit (g/ml); die Eingabe wird
#    beim Auslesen mit dem gewaehlten Multiplikator (1 oder 1000) umgerechnet.
# 2) Label "...pro fertige Portion enthalten" wird jetzt dynamisch je Medium
#    formuliert (z.B. "Angereicherte Butter pro fertige Portion"), analog zum
#    bereits bestehenden dynamischen Traegermenge-Label.
# 3) saveToCharge() beruecksichtigt die gewaehlten Einheiten korrekt (Anzeige-
#    text UND Portionen-Berechnung), damit gespeicherte Chargen nicht durch
#    falsch angenommene Einheiten verzerrt werden.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 9

# ─────────────────────────────────────────────────────────────────────────
# 1) MEDIA_CFG: portion-Label je Medium ergaenzen
# ─────────────────────────────────────────────────────────────────────────
old1 = """var MEDIA_CFG = {
  butter:    {unit:'g',  eff:78, hint:'Butter ~78%', carrier:'Buttermenge gesamt'},
  ghee:      {unit:'g',  eff:88, hint:'Ghee ~88% — reines Butterfett', carrier:'Ghee-Menge gesamt'},
  kokosoel:  {unit:'g',  eff:90, hint:'Kokosöl nativ ~90%', carrier:'Kokosöl gesamt'},
  kokosfett: {unit:'g',  eff:88, hint:'Kokosfett raffiniert ~88%', carrier:'Kokosfett gesamt'},
  mct:       {unit:'ml', eff:85, hint:'MCT-Öl ~85%', carrier:'MCT-Öl gesamt'},
  olivenoel: {unit:'ml', eff:75, hint:'Olivenöl ~75%', carrier:'Olivenöl gesamt'},
  glycerin:  {unit:'ml', eff:55, hint:'Glycerin ~55%', carrier:'Glycerin gesamt'},
  tinktur:   {unit:'ml', eff:92, hint:'Ethanol ~92%', carrier:'Ethanol gesamt'},
  gummies:   {unit:'g',  eff:80, hint:'Gummies', carrier:'Gummimasse gesamt'},
  hard_candy:{unit:'g',  eff:82, hint:'Hard Candy', carrier:'Zuckermasse gesamt'},
  baked:     {unit:'g',  eff:75, hint:'Backwaren', carrier:'Teigmasse gesamt'},
  kapseln:   {unit:'ml', eff:88, hint:'Kapseln', carrier:'Trägeröl gesamt'}
};"""

new1 = """var MEDIA_CFG = {
  butter:    {unit:'g',  eff:78, hint:'Butter ~78%', carrier:'Buttermenge gesamt', portion:'Angereicherte Butter pro fertige Portion'},
  ghee:      {unit:'g',  eff:88, hint:'Ghee ~88% — reines Butterfett', carrier:'Ghee-Menge gesamt', portion:'Angereichertes Ghee pro fertige Portion'},
  kokosoel:  {unit:'g',  eff:90, hint:'Kokosöl nativ ~90%', carrier:'Kokosöl gesamt', portion:'Angereichertes Kokosöl pro fertige Portion'},
  kokosfett: {unit:'g',  eff:88, hint:'Kokosfett raffiniert ~88%', carrier:'Kokosfett gesamt', portion:'Angereichertes Kokosfett pro fertige Portion'},
  mct:       {unit:'ml', eff:85, hint:'MCT-Öl ~85%', carrier:'MCT-Öl gesamt', portion:'Angereichertes MCT-Öl pro fertige Portion'},
  olivenoel: {unit:'ml', eff:75, hint:'Olivenöl ~75%', carrier:'Olivenöl gesamt', portion:'Angereichertes Olivenöl pro fertige Portion'},
  glycerin:  {unit:'ml', eff:55, hint:'Glycerin ~55%', carrier:'Glycerin gesamt', portion:'Angereichertes Glycerin pro fertige Portion'},
  tinktur:   {unit:'ml', eff:92, hint:'Ethanol ~92%', carrier:'Ethanol gesamt', portion:'Angereichertes Ethanol pro fertige Portion'},
  gummies:   {unit:'g',  eff:80, hint:'Gummies', carrier:'Gummimasse gesamt', portion:'Angereicherte Gummimasse pro fertige Portion'},
  hard_candy:{unit:'g',  eff:82, hint:'Hard Candy', carrier:'Zuckermasse gesamt', portion:'Angereicherte Zuckermasse pro fertige Portion'},
  baked:     {unit:'g',  eff:75, hint:'Backwaren', carrier:'Teigmasse gesamt', portion:'Angereicherte Teigmasse pro fertige Portion'},
  kapseln:   {unit:'ml', eff:88, hint:'Kapseln', carrier:'Trägeröl gesamt', portion:'Angereichertes Trägeröl pro fertige Portion'}
};"""

if old1 not in content:
    print("WARNUNG 1: MEDIA_CFG nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: MEDIA_CFG um 'portion'-Label je Medium ergänzt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) HTML: Label "Gramm Wirkstoffträger..." bekommt id="label-portion"
# ─────────────────────────────────────────────────────────────────────────
old2 = """<label class="cl">Gramm Wirkstoffträger pro fertige Portion enthalten</label>"""
new2 = """<label class="cl" id="label-portion">Gramm Wirkstoffträger pro fertige Portion enthalten</label>"""

if old2 not in content:
    print("WARNUNG 2: Portion-Label nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Portion-Label bekommt id='label-portion'.")

# ─────────────────────────────────────────────────────────────────────────
# 3) HTML: Eingesetzte Wirkstoffmenge -> Einheiten-Select
# ─────────────────────────────────────────────────────────────────────────
old3 = """<div class="input-row"><input type="number" id="ig" value="5" min="0.001" step="0.001" oninput="calcUpdate()"><span class="unit-badge" id="input-unit-label">g</span></div>"""
new3 = """<div class="input-row"><input type="number" id="ig" value="5" min="0.001" step="0.001" oninput="calcUpdate()"><select class="unit-badge" id="input-unit-label" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>"""

if old3 not in content:
    print("WARNUNG 3: Eingabefeld 'ig' nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: 'Eingesetzte Wirkstoffmenge' hat jetzt Einheiten-Umschalter.")

# ─────────────────────────────────────────────────────────────────────────
# 4) HTML: Trägermenge gesamt -> Einheiten-Select
# ─────────────────────────────────────────────────────────────────────────
old4 = """<div class="input-row"><input type="number" id="carrier" value="200" min="1" step="1" oninput="calcUpdate()"><span class="unit-badge" id="carrier-unit">g</span></div>"""
new4 = """<div class="input-row"><input type="number" id="carrier" value="200" min="1" step="1" oninput="calcUpdate()"><select class="unit-badge" id="carrier-unit" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>"""

if old4 not in content:
    print("WARNUNG 4: Eingabefeld 'carrier' nicht gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: 'Trägermenge gesamt' hat jetzt Einheiten-Umschalter.")

# ─────────────────────────────────────────────────────────────────────────
# 5) HTML: Menge pro Portion -> Einheiten-Select
# ─────────────────────────────────────────────────────────────────────────
old5 = """<div class="input-row"><input type="number" id="portion-c" value="10" min="0.1" step="0.1" oninput="calcUpdate()"><span class="unit-badge" id="portion-unit">g</span></div>"""
new5 = """<div class="input-row"><input type="number" id="portion-c" value="10" min="0.1" step="0.1" oninput="calcUpdate()"><select class="unit-badge" id="portion-unit" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>"""

if old5 not in content:
    print("WARNUNG 5: Eingabefeld 'portion-c' nicht gefunden.")
else:
    content = content.replace(old5, new5)
    changes += 1
    print(f"5/{total}: 'Menge pro Portion' hat jetzt Einheiten-Umschalter.")

# ─────────────────────────────────────────────────────────────────────────
# 6) onMediumChange(): Select-Optionen (g/kg oder ml/l) je nach Medium setzen
#    statt nur Text zu schreiben
# ─────────────────────────────────────────────────────────────────────────
old6 = """window.onMediumChange = function() {
  var med = document.getElementById('cm').value;
  var cfg = MEDIA_CFG[med]||{unit:'g',eff:80,hint:''};
  document.getElementById('carrier-unit').textContent = cfg.unit;
  document.getElementById('portion-unit').textContent = cfg.unit;
  document.getElementById('input-unit-label').textContent = cfg.unit;
  document.getElementById('eff').value = cfg.eff;
  document.getElementById('eo').textContent = cfg.eff;
  document.getElementById('eff-hint').textContent = cfg.hint;
  calcUpdate();
};"""

new6 = """function setUnitOptions(id, baseUnit) {
  var el = document.getElementById(id);
  if(!el) return;
  if(baseUnit === 'ml') el.innerHTML = '<option value="1">ml</option><option value="1000">l</option>';
  else el.innerHTML = '<option value="1">g</option><option value="1000">kg</option>';
  el.value = '1';
}
window.onMediumChange = function() {
  var med = document.getElementById('cm').value;
  var cfg = MEDIA_CFG[med]||{unit:'g',eff:80,hint:''};
  setUnitOptions('carrier-unit', cfg.unit);
  setUnitOptions('portion-unit', cfg.unit);
  setUnitOptions('input-unit-label', cfg.unit);
  document.getElementById('eff').value = cfg.eff;
  document.getElementById('eo').textContent = cfg.eff;
  document.getElementById('eff-hint').textContent = cfg.hint;
  calcUpdate();
};"""

if old6 not in content:
    print("WARNUNG 6: onMediumChange() nicht (exakt) gefunden.")
else:
    content = content.replace(old6, new6)
    changes += 1
    print(f"6/{total}: onMediumChange() befüllt jetzt Einheiten-Selects statt nur Text zu setzen.")

# ─────────────────────────────────────────────────────────────────────────
# 7) calcUpdate(): Werte mit gewähltem Einheiten-Multiplikator umrechnen,
#    dynamisches Portion-Label setzen
# ─────────────────────────────────────────────────────────────────────────
old7 = """  var lc = document.getElementById('label-carrier');
  if(lc) lc.textContent = cfg.carrier || 'Trägermenge gesamt';
  var carrier = parseFloat(document.getElementById('carrier').value)||0;
  var pc = parseFloat(document.getElementById('portion-c').value)||0;
  var e = parseFloat(document.getElementById('eff').value)||80;
  var g = parseFloat(document.getElementById('ig').value)||0;"""

new7 = """  var lc = document.getElementById('label-carrier');
  if(lc) lc.textContent = cfg.carrier || 'Trägermenge gesamt';
  var lp = document.getElementById('label-portion');
  if(lp) lp.textContent = cfg.portion || 'Gramm Wirkstoffträger pro fertige Portion enthalten';
  var carrierMult = parseFloat(document.getElementById('carrier-unit').value)||1;
  var carrier = (parseFloat(document.getElementById('carrier').value)||0) * carrierMult;
  var pcMult = parseFloat(document.getElementById('portion-unit').value)||1;
  var pc = (parseFloat(document.getElementById('portion-c').value)||0) * pcMult;
  var e = parseFloat(document.getElementById('eff').value)||80;
  var gMult = parseFloat(document.getElementById('input-unit-label').value)||1;
  var g = (parseFloat(document.getElementById('ig').value)||0) * gMult;"""

if old7 not in content:
    print("WARNUNG 7: calcUpdate()-Anfang nicht (exakt) gefunden.")
else:
    content = content.replace(old7, new7)
    changes += 1
    print(f"7/{total}: calcUpdate() rechnet Eingaben jetzt mit dem gewählten Einheiten-Multiplikator um, Portion-Label wird dynamisch gesetzt.")

# ─────────────────────────────────────────────────────────────────────────
# 8) saveToCharge(): korrekte Einheiten in Anzeigetext und Portionen-Berechnung
# ─────────────────────────────────────────────────────────────────────────
old8 = """  var g = document.getElementById('ig').value;
  var carrier = document.getElementById('carrier').value;
  var pcv = document.getElementById('portion-c').value;
  var cfg2 = MEDIA_CFG[document.getElementById('cm').value]||{unit:'g'};
  var mat = calcMode==='extract' ? g+'g Extrakt ('+document.getElementById('potency-ext').value+'%)' : g+'g Blüten ('+document.getElementById('potency').value+'%)';
  var c = {id:Date.now(), name:'Charge '+ds+' – '+med, medium:med, date:ds,
    dose:portion.replace(' mg',''), portions:Math.round(parseFloat(carrier)/parseFloat(pcv)||0),
    material:mat, recipe:'Aus Rechner: '+mat+' in '+carrier+cfg2.unit+' '+med+'. Gesamt: '+total+'.',
    notes:'', attachments:[], created:Date.now()};"""

new8 = """  var g = document.getElementById('ig').value;
  var carrier = document.getElementById('carrier').value;
  var pcv = document.getElementById('portion-c').value;
  var igUnitSel = document.getElementById('input-unit-label');
  var igUnitTxt = igUnitSel.options[igUnitSel.selectedIndex].text;
  var carrierUnitSel = document.getElementById('carrier-unit');
  var carrierUnitTxt = carrierUnitSel.options[carrierUnitSel.selectedIndex].text;
  var carrierMult2 = parseFloat(carrierUnitSel.value)||1;
  var portionMult2 = parseFloat(document.getElementById('portion-unit').value)||1;
  var carrierBase2 = (parseFloat(carrier)||0) * carrierMult2;
  var pcvBase2 = (parseFloat(pcv)||0) * portionMult2;
  var mat = calcMode==='extract' ? g+igUnitTxt+' Extrakt ('+document.getElementById('potency-ext').value+'%)' : g+igUnitTxt+' Blüten ('+document.getElementById('potency').value+'%)';
  var c = {id:Date.now(), name:'Charge '+ds+' – '+med, medium:med, date:ds,
    dose:portion.replace(' mg',''), portions:Math.round(carrierBase2/pcvBase2||0),
    material:mat, recipe:'Aus Rechner: '+mat+' in '+carrier+carrierUnitTxt+' '+med+'. Gesamt: '+total+'.',
    notes:'', attachments:[], created:Date.now()};"""

if old8 not in content:
    print("WARNUNG 8: saveToCharge() nicht (exakt) gefunden.")
else:
    content = content.replace(old8, new8)
    changes += 1
    print(f"8/{total}: saveToCharge() berücksichtigt jetzt die gewählten Einheiten korrekt.")

# ─────────────────────────────────────────────────────────────────────────
# 9) CSS: unit-badge als <select> braucht minimale Anpassung (Cursor/Look)
# ─────────────────────────────────────────────────────────────────────────
old9 = """.unit-badge{display:flex;align-items:center;padding:0 10px;background:var(--bg3);border:1px solid var(--border2);border-radius:var(--radius);font-size:var(--fs);color:var(--text3);white-space:nowrap;margin-top:3px}"""
new9 = """.unit-badge{display:flex;align-items:center;padding:0 10px;background:var(--bg3);border:1px solid var(--border2);border-radius:var(--radius);font-size:var(--fs);color:var(--text3);white-space:nowrap;margin-top:3px;cursor:pointer}
select.unit-badge{-webkit-appearance:none;appearance:none;font-family:inherit}"""

if old9 not in content:
    print("WARNUNG 9: .unit-badge CSS nicht gefunden.")
else:
    content = content.replace(old9, new9)
    changes += 1
    print(f"9/{total}: CSS für Einheiten-Select (Cursor, Aussehen) ergänzt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
