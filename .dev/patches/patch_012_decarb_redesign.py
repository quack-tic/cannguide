#!/usr/bin/env python3
# Patch 7: Decarb-Toggle-Redesign nach Adrians Korrekturen.
#  - Pflicht-Auswahl (kein Default) -> ohne Ja/Nein kein Ergebnis
#  - saubere Ja/Nein-Optionen, keine Produktlisten (Produkt != Decarb-Status)
#  - Toggle auch im Rohmaterial-Modus (THCA vs. Total-THC)
#  - Auto-Default nach Extrakt-Typ entfernt (war sachlich falsch)
#  - Lexikon "Decarb bei Extrakten" mit korrekten Fakten neu
import sys, re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

changed = False

# ---------------------------------------------------------------------------
# 7a: Extrakt-Toggle -> Pflichtauswahl + saubere Ja/Nein
# ---------------------------------------------------------------------------
old_ext = '''        <select id="extract-decarb" onchange="onDecarbChange()">
          <option value="yes">Ja \u2013 bereits aktiv (Destillat, FECO, RSO, erhitzt)</option>
          <option value="no">Nein \u2013 Roh-Extrakt (Rosin, Kief, THCA-Kristalle)</option>
        </select>'''
new_ext = '''        <select id="extract-decarb" onchange="onDecarbChange()">
          <option value="" selected disabled>\u2014 bitte w\u00e4hlen \u2014</option>
          <option value="no">Nein \u2013 Rohwert (THCA, Aktivierung n\u00f6tig)</option>
          <option value="yes">Ja \u2013 bereits aktives THC</option>
        </select>'''
if 'value="" selected disabled' in html and 'id="extract-decarb"' in html:
    print('  [skip] 7a: Extrakt-Toggle bereits umgestellt.')
elif old_ext in html:
    html = html.replace(old_ext, new_ext, 1)
    print('  [ok]   7a: Extrakt-Toggle = Pflichtauswahl, saubere Optionen.')
    changed = True
else:
    sys.exit('  [FAIL] 7a: alter Extrakt-Toggle nicht gefunden.')

# ---------------------------------------------------------------------------
# 7b: Roh-Toggle in raw-inputs einfuegen
# ---------------------------------------------------------------------------
anchor_raw = '''    <div id="raw-inputs">
      <div class="cr"><label class="cl">Wirkstoffgehalt Material: <strong id="po">20</strong>%</label>
        <input type="range" min="1" max="35" step="1" value="20" id="potency" oninput="document.getElementById('po').textContent=this.value;calcUpdate()">
      </div>
    </div>'''
new_raw = '''    <div id="raw-inputs">
      <div class="cr"><label class="cl">Wirkstoffgehalt Material: <strong id="po">20</strong>%</label>
        <input type="range" min="1" max="35" step="1" value="20" id="potency" oninput="document.getElementById('po').textContent=this.value;calcUpdate()">
      </div>
      <div class="cr"><label class="cl">Wert bereits als aktives THC angegeben?</label>
        <select id="raw-decarb" onchange="onDecarbChange()">
          <option value="" selected disabled>\u2014 bitte w\u00e4hlen \u2014</option>
          <option value="no">Nein \u2013 Rohwert / THCA (Aktivierung n\u00f6tig)</option>
          <option value="yes">Ja \u2013 aktives (Total-)THC</option>
        </select>
      </div>
      <div id="raw-decarb-info" style="display:none;border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);margin-bottom:.625rem"></div>
    </div>'''
if 'id="raw-decarb"' in html:
    print('  [skip] 7b: Roh-Toggle existiert bereits.')
elif anchor_raw in html:
    html = html.replace(anchor_raw, new_raw, 1)
    print('  [ok]   7b: Roh-Decarb-Toggle eingefuegt.')
    changed = True
else:
    sys.exit('  [FAIL] 7b: raw-inputs-Anker nicht gefunden.')

# ---------------------------------------------------------------------------
# 7c: Auto-Default nach Extrakt-Typ entfernen (5e revert)
# ---------------------------------------------------------------------------
old_5e = '''  document.getElementById('extract-hint').textContent = cfg.hint;
  var dc = document.getElementById('extract-decarb');
  if(dc) dc.value = (['dest','feco','rso','tred'].indexOf(t) >= 0) ? 'yes' : 'no';
  if(window.onDecarbChange) onDecarbChange(); else calcUpdate();
};'''
new_5e = '''  document.getElementById('extract-hint').textContent = cfg.hint;
  calcUpdate();
};'''
if "indexOf(t) >= 0) ? 'yes' : 'no'" not in html:
    print('  [skip] 7c: Auto-Default bereits entfernt.')
elif old_5e in html:
    html = html.replace(old_5e, new_5e, 1)
    print('  [ok]   7c: Auto-Default nach Typ entfernt.')
    changed = True
else:
    sys.exit('  [FAIL] 7c: 5e-Block nicht gefunden.')

# ---------------------------------------------------------------------------
# 7d: Rechenblock -> beide Modi + decarbSel fuer Pflichtpruefung
# ---------------------------------------------------------------------------
old_calc = '''  // Decarb-Korrektur: Roh-Extrakte (THCA) verlieren beim Aktivieren ~12,3% Masse (CO2).
  var decarbNo = false;
  if(calcMode==='extract') {
    var _dc = document.getElementById('extract-decarb');
    if(_dc && _dc.value === 'no') { totMg = totMg * 0.877; decarbNo = true; }
  }'''
new_calc = '''  // Decarb-Korrektur: Rohwerte (THCA) verlieren beim Aktivieren ~12,3% Masse (CO2).
  var decarbNo = false, decarbSel = 'na';
  if(calcMode==='extract' || calcMode==='raw') {
    var _dc = document.getElementById(calcMode==='extract' ? 'extract-decarb' : 'raw-decarb');
    decarbSel = _dc ? _dc.value : '';
    if(decarbSel === 'no') { totMg = totMg * 0.877; decarbNo = true; }
  }'''
if 'var decarbNo = false, decarbSel' in html:
    print('  [skip] 7d: Rechenblock bereits erweitert.')
elif old_calc in html:
    html = html.replace(old_calc, new_calc, 1)
    print('  [ok]   7d: Rechenblock deckt beide Modi ab.')
    changed = True
else:
    sys.exit('  [FAIL] 7d: alter Decarb-Rechenblock nicht gefunden.')

# ---------------------------------------------------------------------------
# 7e: Pflichtpruefung in errs
# ---------------------------------------------------------------------------
anchor_err = "  if(g<=0) errs.push('Eingesetzte Wirkstoffmenge eingeben.');"
err_insert = "\n  if((calcMode==='extract'||calcMode==='raw') && decarbSel!=='yes' && decarbSel!=='no') errs.push('Decarboxylierung w\\u00e4hlen (Ja/Nein).');"
if "errs.push('Decarboxylierung w" in html:
    print('  [skip] 7e: Pflichtpruefung existiert bereits.')
elif anchor_err in html:
    html = html.replace(anchor_err, anchor_err + err_insert, 1)
    print('  [ok]   7e: Pflichtpruefung (kein Ergebnis ohne Auswahl).')
    changed = True
else:
    sys.exit('  [FAIL] 7e: errs-Anker nicht gefunden.')

# ---------------------------------------------------------------------------
# 7f: effLabel im Rohmaterial-Modus decarb-aware
# ---------------------------------------------------------------------------
old_lbl = """  } else {
    effLabel = 'Nach Effizienz ('+eEff+'%)';
  }"""
new_lbl = """  } else {
    effLabel = 'Nach Effizienz ('+eEff+'%)'+(decarbNo?' \\u00b7 Rohwert decarbt ~87,7%':'');
  }"""
if "Rohwert decarbt ~87,7%" in html:
    print('  [skip] 7f: effLabel (raw) bereits erweitert.')
elif old_lbl in html:
    html = html.replace(old_lbl, new_lbl, 1)
    print('  [ok]   7f: effLabel (raw) decarb-aware.')
    changed = True
else:
    sys.exit('  [FAIL] 7f: raw-effLabel nicht gefunden.')

# ---------------------------------------------------------------------------
# 7g: onDecarbChange -> beide Toggles, Konsequenz-Text je Zustand
# ---------------------------------------------------------------------------
old_fn = """window.onDecarbChange = function() {
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
};"""
new_fn = """window.onDecarbChange = function() {
  [['extract-decarb','decarb-info'],['raw-decarb','raw-decarb-info']].forEach(function(p){
    var dc = document.getElementById(p[0]); var box = document.getElementById(p[1]);
    if(!dc || !box) return;
    if(dc.value === 'no') {
      box.style.display = 'block';
      box.style.background='var(--warn-bg)'; box.style.border='1px solid var(--warn)'; box.style.color='var(--warn)';
      box.innerHTML = '\\u26a0\\ufe0f <b>Rohwert (THCA):</b> muss vor oder beim Verarbeiten zu Edibles decarboxyliert (erhitzt) werden \\u2013 sonst kaum Wirkung. Beim Aktivieren gehen ~12% Masse als CO\\u2082 verloren; der Rechner zieht das ab.';
    } else if(dc.value === 'yes') {
      box.style.display = 'block';
      box.style.background='var(--bg3)'; box.style.border='1px solid var(--border)'; box.style.color='var(--text3)';
      box.innerHTML = '\\u2713 Wird als bereits aktives THC gerechnet (voller Wert, kein Decarb-Abzug).';
    } else {
      box.style.display = 'none';
    }
  });
  calcUpdate();
};"""
if "['raw-decarb','raw-decarb-info']" in html:
    print('  [skip] 7g: onDecarbChange bereits umgebaut.')
elif old_fn in html:
    html = html.replace(old_fn, new_fn, 1)
    print('  [ok]   7g: onDecarbChange deckt beide Toggles ab.')
    changed = True
else:
    sys.exit('  [FAIL] 7g: alte onDecarbChange nicht gefunden.')

# ---------------------------------------------------------------------------
# 7h: Lexikon "Decarb bei Extrakten" mit korrekten Fakten (ROHENTWURF)
# ---------------------------------------------------------------------------
new_entry = (
    "{t:'Decarb bei Extrakten & Konzentraten',b:'"
    "<span class=\"lex-term\">Decarb bei Extrakten</span>"
    "<span class=\"lex-tag adv\">Fortgeschritten</span><br>"
    "[ROHENTWURF \u2013 bitte pr\u00fcfen] Ob ein Extrakt bereits decarboxyliert ist, "
    "h\u00e4ngt vom Herstellungsprozess ab \u2013 nicht vom Produktnamen. Entscheidend ist, "
    "ob dabei \u00fcber l\u00e4ngere Zeit Temperaturen um ~115 \u00b0C erreicht wurden. "
    "Vakuumdestillation trennt das L\u00f6sungsmittel bei ~50 \u00b0C ab \u2013 dabei wird "
    "nichts aktiviert. FECO muss aktiv decarboxyliert werden. RSO erreicht auf "
    "\u00fcblichen Wegen die n\u00f6tige Temperatur meist nicht \u2013 im Zweifel "
    "decarboxylieren. Bei der Fraktionsdestillation von FECO zu Cannabino\u00efd\u00f6l "
    "muss bereits vorher decarbt werden, sonst entsteht bei der Fraktionierung zu viel "
    "CO\u2082. Faustregel: Bist du unsicher, behandle den Extrakt als Rohwert und "
    "decarboxyliere. Kalt einger\u00fchrtes Roh-Konzentrat wirkt kaum \u2013 und "
    "verleitet beim n\u00e4chsten Versuch zur gef\u00e4hrlichen \u00dcberdosierung.'},"
)
pattern = r"\{t:'Decarb bei Extrakten & Konzentraten',b:'.*?'\},"
if '[ROHENTWURF \u2013 bitte pr\u00fcfen] Ob ein Extrakt' in html:
    print('  [skip] 7h: Lexikon-Eintrag bereits aktualisiert.')
elif re.search(pattern, html, re.DOTALL):
    html = re.sub(pattern, lambda m: new_entry, html, count=1, flags=re.DOTALL)
    print('  [ok]   7h: Lexikon "Decarb bei Extrakten" neu (korrekte Fakten).')
    changed = True
else:
    sys.exit('  [FAIL] 7h: alter Lexikon-Eintrag nicht gefunden.')

if changed:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
print('Patch 7 geschrieben.')
