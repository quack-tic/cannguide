#!/usr/bin/env python3
# Patch 5: Decarb-Toggle im Extrakt-Modus.
# Roh-Extrakte (Rosin, Kief, THCA) sind nicht decarboxyliert -> beim Aktivieren
# verliert THCA ~12,3% Masse (CO2). Bisher rechnete der Rechner IMMER mit 100%
# aktiv -> Ueberschaetzung bei Roh-Extrakten. Toggle korrigiert das.
import sys

with open('index.html', encoding='utf-8') as f:
    html = f.read()

changed = False

# ---------------------------------------------------------------------------
# 5a: UI-Toggle + Info-Box vor dem extract-hint einfuegen
# ---------------------------------------------------------------------------
anchor_ui = '      <div id="extract-hint" style="background:var(--bg3);border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);color:var(--text3);margin-bottom:.625rem"></div>'
toggle_ui = '''      <div class="cr"><label class="cl">Bereits decarboxyliert (aktiviert)?</label>
        <select id="extract-decarb" onchange="onDecarbChange()">
          <option value="yes">Ja \u2013 bereits aktiv (Destillat, FECO, RSO, erhitzt)</option>
          <option value="no">Nein \u2013 Roh-Extrakt (Rosin, Kief, THCA-Kristalle)</option>
        </select>
      </div>
      <div id="decarb-info" style="display:none;background:var(--warn-bg);border:1px solid var(--warn);border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);color:var(--warn);margin-bottom:.625rem"></div>
'''
if 'id="extract-decarb"' in html:
    print('  [skip] 5a: Toggle-UI existiert bereits.')
elif anchor_ui in html:
    html = html.replace(anchor_ui, toggle_ui + anchor_ui, 1)
    print('  [ok]   5a: Decarb-Toggle + Info-Box eingefuegt.')
    changed = True
else:
    sys.exit('  [FAIL] 5a: Anker (extract-hint div) nicht gefunden.')

# ---------------------------------------------------------------------------
# 5b: Rechenlogik - nach totMg den Decarb-Faktor anwenden
# ---------------------------------------------------------------------------
anchor_calc = '  var eEff = (calcMode===\'extract\') ? 100 : e;\n  var totMg = rawMg*(eEff/100);'
calc_insert = '''
  // Decarb-Korrektur: Roh-Extrakte (THCA) verlieren beim Aktivieren ~12,3% Masse (CO2).
  var decarbNo = false;
  if(calcMode==='extract') {
    var _dc = document.getElementById('extract-decarb');
    if(_dc && _dc.value === 'no') { totMg = totMg * 0.877; decarbNo = true; }
  }'''
if 'var decarbNo' in html:
    print('  [skip] 5b: Rechenlogik existiert bereits.')
elif anchor_calc in html:
    html = html.replace(anchor_calc, anchor_calc + calc_insert, 1)
    print('  [ok]   5b: Decarb-Faktor in Rechnung eingefuegt.')
    changed = True
else:
    sys.exit('  [FAIL] 5b: Anker (totMg-Berechnung) nicht gefunden.')

# ---------------------------------------------------------------------------
# 5c: effLabel decarb-aware machen (ersetzt die einzeilige Zuweisung)
# ---------------------------------------------------------------------------
old_label = "  var effLabel = (calcMode==='extract') ? 'Vollst\\u00e4ndige Einarbeitung (~100% Transfer, kein Pflanzenmaterial-Verlust)' : 'Nach Effizienz ('+eEff+'%)';"
new_label = """  var effLabel;
  if(calcMode==='extract') {
    effLabel = decarbNo
      ? 'Roh-Extrakt \\u2192 decarboxyliert: ~87,7% aktiv (THCA\\u2192THC, CO\\u2082-Verlust)'
      : 'Vollst\\u00e4ndige Einarbeitung (~100% Transfer, bereits aktiv)';
  } else {
    effLabel = 'Nach Effizienz ('+eEff+'%)';
  }"""
if 'var effLabel;' in html:
    print('  [skip] 5c: effLabel-Logik existiert bereits.')
elif old_label in html:
    html = html.replace(old_label, new_label, 1)
    print('  [ok]   5c: effLabel decarb-aware.')
    changed = True
else:
    sys.exit('  [FAIL] 5c: altes effLabel nicht gefunden.')

# ---------------------------------------------------------------------------
# 5d: onDecarbChange()-Funktion + smarter Default in onExtractTypeChange
# ---------------------------------------------------------------------------
anchor_fn = '''window.onExtractTypeChange = function() {'''
new_fn = '''window.onDecarbChange = function() {
  var dc = document.getElementById('extract-decarb');
  var box = document.getElementById('decarb-info');
  if(dc && box) {
    if(dc.value === 'no') {
      box.style.display = 'block';
      box.innerHTML = '\\u26a0\\ufe0f <b>Roh-Extrakt:</b> THCA muss vor oder beim Verarbeiten zu Edibles decarboxyliert (erhitzt) werden \\u2013 sonst kaum Wirkung. Beim Aktivieren verliert THCA ~12% Masse (CO\\u2082), der Rechner zieht das automatisch ab. Rosin/Kief/BHO nicht kalt verr\\u00fchren.';
    } else {
      box.style.display = 'none';
    }
  }
  calcUpdate();
};

window.onExtractTypeChange = function() {'''
if 'window.onDecarbChange' in html:
    print('  [skip] 5d: onDecarbChange existiert bereits.')
elif anchor_fn in html:
    html = html.replace(anchor_fn, new_fn, 1)
    print('  [ok]   5d: onDecarbChange-Funktion eingefuegt.')
    changed = True
else:
    sys.exit('  [FAIL] 5d: onExtractTypeChange nicht gefunden.')

# 5e: Default-Setzung ans Ende von onExtractTypeChange haengen
anchor_def = """  document.getElementById('extract-hint').textContent = cfg.hint;
  calcUpdate();
};"""
new_def = """  document.getElementById('extract-hint').textContent = cfg.hint;
  var dc = document.getElementById('extract-decarb');
  if(dc) dc.value = (['dest','feco','rso','tred'].indexOf(t) >= 0) ? 'yes' : 'no';
  if(window.onDecarbChange) onDecarbChange(); else calcUpdate();
};"""
if "indexOf(t) >= 0) ? 'yes' : 'no'" in html:
    print('  [skip] 5e: Default-Setzung existiert bereits.')
elif anchor_def in html:
    html = html.replace(anchor_def, new_def, 1)
    print('  [ok]   5e: Smarter Default je Extrakt-Typ.')
    changed = True
else:
    sys.exit('  [FAIL] 5e: Ende von onExtractTypeChange nicht gefunden.')

if changed:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
print('Patch 5 geschrieben.')
