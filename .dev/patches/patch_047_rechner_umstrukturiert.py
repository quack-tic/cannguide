#!/usr/bin/env python3
# Patch 047: Rechner-Formular thematisch neu gegliedert, um eine echte
# Verwechslungsgefahr zu beheben: "Traeger/Medium" und "Eingesetzte
# Wirkstoffmenge" standen bisher nebeneinander in derselben Zeile, obwohl sie
# inhaltlich nichts miteinander zu tun haben (Medium-TYP vs. Cannabis-MENGE).
#
# Neue Struktur:
#   Block A "Ausgangsmaterial"          -- Wirkstoffmenge, Potenz, Decarb
#   Block B "Herstellung & Portionierung" -- Medium, Traegermenge, Portion, Effizienz
#   Block C "Wirkung & Einordnung"      -- Bioverfuegbarkeit, Toleranz, Terpene
#
# Alle Info-/Warnboxen (raw-decarb-info, decarb-info, extract-hint,
# bio-appinfo, bio-disclaimer, terp-info) wandern mit ihrem jeweiligen Feld
# mit. Die Tour (TOUR_STEPS) wird entsprechend auf 11 Schritte erweitert
# (Traeger/Medium bekommt jetzt einen eigenen Schritt statt mit der
# Wirkstoffmenge zusammengelegt zu sein).
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

# ─────────────────────────────────────────────────────────────────────────
# 1) Formular-Reihenfolge komplett neu aufbauen
# ─────────────────────────────────────────────────────────────────────────
old1 = """  <div class="cs">
    <div class="mode-toggle">
      <button id="btn-mode-raw" class="btn primary" onclick="setCalcMode('raw')">🌿 Blüten</button>
      <button id="btn-mode-extract" class="btn" onclick="setCalcMode('extract')">💧 Extrakt / Konzentrat</button>
    </div>
    <div class="row2" id="carrier-medium-row">
      <div class="cr"><label class="cl">Träger / Medium</label>
        <select id="cm" onchange="onMediumChange()">
          <optgroup label="Fette"><option value="butter">Butter</option><option value="ghee">Ghee</option><option value="kokosoel">Kokosöl (nativ)</option><option value="kokosfett">Kokosfett (raffiniert)</option></optgroup>
          <optgroup label="Öle"><option value="mct">MCT-Öl (C8/C10)</option><option value="olivenoel">Olivenöl</option></optgroup>
          <optgroup label="Weitere Träger"><option value="glycerin">Glycerin (VG)</option><option value="tinktur">Tinktur / Ethanol</option></optgroup>
          <optgroup label="Fertigprodukte"><option value="gummies">Gummies</option><option value="hard_candy">Hard Candy</option><option value="baked">Backwaren</option><option value="kapseln">Kapseln</option></optgroup>
        </select>
      </div>
      <div class="cr"><label class="cl">Eingesetzte Wirkstoffmenge</label>
        <div class="input-row"><input type="number" id="ig" value="5" min="0.001" step="0.001" oninput="calcUpdate()"><select class="unit-badge" id="input-unit-label" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>
      </div>
    </div>
    <!-- Blüten -->
    <div id="raw-inputs">
      <div class="cr"><label class="cl">Wirkstoffgehalt Blüten: <strong id="po">20</strong>%</label>
        <input type="range" min="1" max="35" step="1" value="20" id="potency" oninput="document.getElementById('po').textContent=this.value;calcUpdate()">
      </div>
      <div class="cr"><label class="cl">Bereits decarboxyliert (aktiviert)?</label>
        <select id="raw-decarb" onchange="onDecarbChange()">
          <option value="" selected disabled>— bitte wählen —</option>
          <option value="no">Nein – Rohwert / THCA (Aktivierung nötig)</option>
          <option value="yes">Ja – aktives Material</option>
        </select>
      </div>
      <div id="raw-decarb-info" style="display:none;border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);margin-bottom:.625rem"></div>
    </div>
    <!-- Extrakt -->
    <div id="extract-inputs" style="display:none">
      <div class="row2">
        <div class="cr"><label class="cl">Extrakt-Typ</label>
          <select id="extract-type" onchange="onExtractTypeChange()">
            <optgroup label="Blütenmaterial (unverarbeitet)"><option value="kief">Kief / Pollen (30–60%)</option></optgroup>
            <optgroup label="Lösungsmittelfrei"><option value="rosin">Rosin (60–80%)</option><option value="thca_k">THCA-Kristalle (95–99%)</option></optgroup>
            <optgroup label="Lösungsmittel-Extrakte"><option value="bho_s">BHO Shatter (70–90%)</option><option value="bho_w">BHO Wax/Budder (65–85%)</option><option value="bho_o">BHO Sauce/Öl (50–80%)</option><option value="rso">RSO (40–70%)</option><option value="feco">FECO (50–80%)</option><option value="tred">Tinktur-Redukt (30–60%)</option></optgroup>
            <optgroup label="Destillate"><option value="dest">Vakuumdestillat (85–99%)</option></optgroup>
            <option value="custom">Eigener Wert</option>
          </select>
        </div>
        <div class="cr"><label class="cl">Wirkstoffgehalt: <strong id="po-ext">70</strong>%</label>
          <input type="range" min="1" max="99" step="1" value="70" id="potency-ext" oninput="document.getElementById('po-ext').textContent=this.value;calcUpdate()">
        </div>
      </div>
      <div class="cr"><label class="cl">Bereits decarboxyliert (aktiviert)?</label>
        <select id="extract-decarb" onchange="onDecarbChange()">
          <option value="" selected disabled>— bitte wählen —</option>
          <option value="no">Nein – Rohwert (THCA, Aktivierung nötig)</option>
          <option value="yes">Ja – aktives Material</option>
        </select>
      </div>
      <div id="decarb-info" style="display:none;background:var(--warn-bg);border:1px solid var(--warn);border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);color:var(--warn);margin-bottom:.625rem"></div>
      <div id="extract-hint" style="background:var(--bg3);border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);color:var(--text3);margin-bottom:.625rem"></div>
    </div>
    <div id="edible-fields">
      <div class="cr"><label class="cl" id="label-carrier">Trägermenge gesamt</label>
        <div class="input-row"><input type="number" id="carrier" value="200" min="1" step="1" oninput="calcUpdate()"><select class="unit-badge" id="carrier-unit" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>
      </div>
      <div class="cr"><label class="cl" id="label-portion">Gramm Wirkstoffträger pro fertige Portion enthalten</label>
        <div class="input-row"><input type="number" id="portion-c" value="10" min="0.1" step="0.1" oninput="calcUpdate()"><select class="unit-badge" id="portion-unit" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>
      </div>
    <!-- Effizienz -->
    <div class="cr" id="eff-row">
      <label class="cl">Extraktionseffizienz: <strong id="eo">80</strong>% <span id="eff-hint" style="font-size:var(--fs-xs);color:var(--text3);margin-left:4px"></span></label>
      <input type="range" min="50" max="98" step="1" value="80" id="eff" oninput="document.getElementById('eo').textContent=this.value;calcUpdate()">
    </div>
    <!-- Applikation / Bioverfügbarkeit -->
    <div class="cr">
      <label class="cl">Applikationsform (Bioverfügbarkeit)</label>
      <select id="bioavail" onchange="onBioChange()">
        <option value="0">— Nicht berücksichtigen —</option>
        <option value="0.275">Sublingual (Ø 20–35%)</option>
        <option value="0.13">Oral / Edibles (Ø 6–20%)</option>
        <option value="0.03">Topisch (Ø 1–5%)</option>
      </select>
    </div>
    <div id="bio-appinfo" style="display:none;background:var(--accent-bg);border:1px solid var(--accent);border-radius:var(--radius);padding:9px 12px;font-size:var(--fs-xs);color:#7ec8a0;line-height:1.65;margin-bottom:.875rem"></div>
    <div id="bio-disclaimer" style="display:none;background:var(--amber-bg);border:1px solid var(--amber);border-radius:var(--radius);padding:9px 12px;font-size:var(--fs-xs);color:var(--amber);line-height:1.65;margin-bottom:.875rem">
      ⚠ Bioverfügbarkeitswerte sind Mittelwerte aus klinischen Studien und stellen keine individuellen Prognosen dar. Natürliche Produkte unterliegen inhärenten Schwankungen in Wirkstoffgehalt und -zusammensetzung. Darüber hinaus beeinflussen genetische Veranlagung, Stoffwechselrate, Mageninhalt, Toleranz und Enzymaktivität (insb. CYP2C9/CYP3A4) die tatsächlich bioverfügbare Menge erheblich. Die angezeigten Werte dienen ausschliesslich der groben Orientierung.
    </div>
    </div>
    <!-- Toleranz -->
    <div class="cr">
      <label class="cl">Konsumfrequenz (Toleranzkorrektur)</label>
      <select id="tolerance" onchange="calcUpdate()">
        <option value="" selected disabled>— bitte wählen —</option>
        <option value="1.0">Gelegentlich (1× / Woche oder weniger)</option>
        <option value="1.3">Regelmässig (2–4× / Woche)</option>
        <option value="1.7">Täglich</option>
        <option value="2.2">Täglich mehrmals</option>
      </select>
    </div>

    <!-- Terpene -->
    <div class="cr">
      <div style="display:flex;align-items:center;justify-content:space-between;cursor:pointer" onclick="var g=document.getElementById('terpene-grid');var i=document.getElementById('terp-toggle');var v=g.style.display==='none';g.style.display=v?'grid':'none';i.textContent=v?'▲':'▼'">
        <label class="cl" style="cursor:pointer;margin:0">Terpenprofil (optional — Info)</label>
        <span id="terp-toggle" style="font-size:10px;color:var(--text3)">▼</span>
      </div>
      <div class="terpene-grid" id="terpene-grid" style="display:none"></div>
    </div>
    <div id="terp-info" style="display:none;background:var(--accent-bg);border:1px solid var(--accent);border-radius:var(--radius);padding:9px 12px;font-size:var(--fs-sm);color:#7ec8a0;line-height:1.65;margin-top:4px"></div>
    </div>
"""

new1 = """  <div class="cs">
    <div class="mode-toggle">
      <button id="btn-mode-raw" class="btn primary" onclick="setCalcMode('raw')">🌿 Blüten</button>
      <button id="btn-mode-extract" class="btn" onclick="setCalcMode('extract')">💧 Extrakt / Konzentrat</button>
    </div>

    <div class="ksec-h" style="margin-top:.75rem"><h2>① Ausgangsmaterial</h2></div>
    <div class="cr"><label class="cl">Eingesetzte Wirkstoffmenge</label>
      <div class="input-row"><input type="number" id="ig" value="5" min="0.001" step="0.001" oninput="calcUpdate()"><select class="unit-badge" id="input-unit-label" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>
    </div>
    <!-- Blüten -->
    <div id="raw-inputs">
      <div class="cr"><label class="cl">Wirkstoffgehalt Blüten: <strong id="po">20</strong>%</label>
        <input type="range" min="1" max="35" step="1" value="20" id="potency" oninput="document.getElementById('po').textContent=this.value;calcUpdate()">
      </div>
      <div class="cr"><label class="cl">Bereits decarboxyliert (aktiviert)?</label>
        <select id="raw-decarb" onchange="onDecarbChange()">
          <option value="" selected disabled>— bitte wählen —</option>
          <option value="no">Nein – Rohwert / THCA (Aktivierung nötig)</option>
          <option value="yes">Ja – aktives Material</option>
        </select>
      </div>
      <div id="raw-decarb-info" style="display:none;border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);margin-bottom:.625rem"></div>
    </div>
    <!-- Extrakt -->
    <div id="extract-inputs" style="display:none">
      <div class="row2">
        <div class="cr"><label class="cl">Extrakt-Typ</label>
          <select id="extract-type" onchange="onExtractTypeChange()">
            <optgroup label="Blütenmaterial (unverarbeitet)"><option value="kief">Kief / Pollen (30–60%)</option></optgroup>
            <optgroup label="Lösungsmittelfrei"><option value="rosin">Rosin (60–80%)</option><option value="thca_k">THCA-Kristalle (95–99%)</option></optgroup>
            <optgroup label="Lösungsmittel-Extrakte"><option value="bho_s">BHO Shatter (70–90%)</option><option value="bho_w">BHO Wax/Budder (65–85%)</option><option value="bho_o">BHO Sauce/Öl (50–80%)</option><option value="rso">RSO (40–70%)</option><option value="feco">FECO (50–80%)</option><option value="tred">Tinktur-Redukt (30–60%)</option></optgroup>
            <optgroup label="Destillate"><option value="dest">Vakuumdestillat (85–99%)</option></optgroup>
            <option value="custom">Eigener Wert</option>
          </select>
        </div>
        <div class="cr"><label class="cl">Wirkstoffgehalt: <strong id="po-ext">70</strong>%</label>
          <input type="range" min="1" max="99" step="1" value="70" id="potency-ext" oninput="document.getElementById('po-ext').textContent=this.value;calcUpdate()">
        </div>
      </div>
      <div class="cr"><label class="cl">Bereits decarboxyliert (aktiviert)?</label>
        <select id="extract-decarb" onchange="onDecarbChange()">
          <option value="" selected disabled>— bitte wählen —</option>
          <option value="no">Nein – Rohwert (THCA, Aktivierung nötig)</option>
          <option value="yes">Ja – aktives Material</option>
        </select>
      </div>
      <div id="decarb-info" style="display:none;background:var(--warn-bg);border:1px solid var(--warn);border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);color:var(--warn);margin-bottom:.625rem"></div>
      <div id="extract-hint" style="background:var(--bg3);border-radius:var(--radius);padding:8px 10px;font-size:var(--fs-sm);color:var(--text3);margin-bottom:.625rem"></div>
    </div>

    <div class="ksec-h" style="margin-top:1.1rem"><h2>② Herstellung & Portionierung</h2></div>
    <div class="cr"><label class="cl">Träger / Medium</label>
      <select id="cm" onchange="onMediumChange()">
        <optgroup label="Fette"><option value="butter">Butter</option><option value="ghee">Ghee</option><option value="kokosoel">Kokosöl (nativ)</option><option value="kokosfett">Kokosfett (raffiniert)</option></optgroup>
        <optgroup label="Öle"><option value="mct">MCT-Öl (C8/C10)</option><option value="olivenoel">Olivenöl</option></optgroup>
        <optgroup label="Weitere Träger"><option value="glycerin">Glycerin (VG)</option><option value="tinktur">Tinktur / Ethanol</option></optgroup>
        <optgroup label="Fertigprodukte"><option value="gummies">Gummies</option><option value="hard_candy">Hard Candy</option><option value="baked">Backwaren</option><option value="kapseln">Kapseln</option></optgroup>
      </select>
    </div>
    <div id="edible-fields">
      <div class="cr"><label class="cl" id="label-carrier">Trägermenge gesamt</label>
        <div class="input-row"><input type="number" id="carrier" value="200" min="1" step="1" oninput="calcUpdate()"><select class="unit-badge" id="carrier-unit" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>
      </div>
      <div class="cr"><label class="cl" id="label-portion">Gramm Wirkstoffträger pro fertige Portion enthalten</label>
        <div class="input-row"><input type="number" id="portion-c" value="10" min="0.1" step="0.1" oninput="calcUpdate()"><select class="unit-badge" id="portion-unit" onchange="calcUpdate()"><option value="1">g</option><option value="1000">kg</option></select></div>
      </div>
    <!-- Effizienz -->
    <div class="cr" id="eff-row">
      <label class="cl">Extraktionseffizienz: <strong id="eo">80</strong>% <span id="eff-hint" style="font-size:var(--fs-xs);color:var(--text3);margin-left:4px"></span></label>
      <input type="range" min="50" max="98" step="1" value="80" id="eff" oninput="document.getElementById('eo').textContent=this.value;calcUpdate()">
    </div>
    </div>

    <div class="ksec-h" style="margin-top:1.1rem"><h2>③ Wirkung & Einordnung</h2></div>
    <!-- Applikation / Bioverfügbarkeit -->
    <div class="cr">
      <label class="cl">Applikationsform (Bioverfügbarkeit)</label>
      <select id="bioavail" onchange="onBioChange()">
        <option value="0">— Nicht berücksichtigen —</option>
        <option value="0.275">Sublingual (Ø 20–35%)</option>
        <option value="0.13">Oral / Edibles (Ø 6–20%)</option>
        <option value="0.03">Topisch (Ø 1–5%)</option>
      </select>
    </div>
    <div id="bio-appinfo" style="display:none;background:var(--accent-bg);border:1px solid var(--accent);border-radius:var(--radius);padding:9px 12px;font-size:var(--fs-xs);color:#7ec8a0;line-height:1.65;margin-bottom:.875rem"></div>
    <div id="bio-disclaimer" style="display:none;background:var(--amber-bg);border:1px solid var(--amber);border-radius:var(--radius);padding:9px 12px;font-size:var(--fs-xs);color:var(--amber);line-height:1.65;margin-bottom:.875rem">
      ⚠ Bioverfügbarkeitswerte sind Mittelwerte aus klinischen Studien und stellen keine individuellen Prognosen dar. Natürliche Produkte unterliegen inhärenten Schwankungen in Wirkstoffgehalt und -zusammensetzung. Darüber hinaus beeinflussen genetische Veranlagung, Stoffwechselrate, Mageninhalt, Toleranz und Enzymaktivität (insb. CYP2C9/CYP3A4) die tatsächlich bioverfügbare Menge erheblich. Die angezeigten Werte dienen ausschliesslich der groben Orientierung.
    </div>
    <!-- Toleranz -->
    <div class="cr">
      <label class="cl">Konsumfrequenz (Toleranzkorrektur)</label>
      <select id="tolerance" onchange="calcUpdate()">
        <option value="" selected disabled>— bitte wählen —</option>
        <option value="1.0">Gelegentlich (1× / Woche oder weniger)</option>
        <option value="1.3">Regelmässig (2–4× / Woche)</option>
        <option value="1.7">Täglich</option>
        <option value="2.2">Täglich mehrmals</option>
      </select>
    </div>
    <!-- Terpene -->
    <div class="cr">
      <div style="display:flex;align-items:center;justify-content:space-between;cursor:pointer" onclick="var g=document.getElementById('terpene-grid');var i=document.getElementById('terp-toggle');var v=g.style.display==='none';g.style.display=v?'grid':'none';i.textContent=v?'▲':'▼'">
        <label class="cl" style="cursor:pointer;margin:0">Terpenprofil (optional — Info)</label>
        <span id="terp-toggle" style="font-size:10px;color:var(--text3)">▼</span>
      </div>
      <div class="terpene-grid" id="terpene-grid" style="display:none"></div>
    </div>
    <div id="terp-info" style="display:none;background:var(--accent-bg);border:1px solid var(--accent);border-radius:var(--radius);padding:9px 12px;font-size:var(--fs-sm);color:#7ec8a0;line-height:1.65;margin-top:4px"></div>
    </div>
"""

if old1 not in content:
    print("WARNUNG 1: Rechner-Formular-Block nicht (exakt) gefunden — evtl. seit letztem Abgleich verändert.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Rechner-Formular in 3 Blöcke neu gegliedert (Ausgangsmaterial / Herstellung & Portionierung / Wirkung).")

# ─────────────────────────────────────────────────────────────────────────
# 2) Tour an die neue Reihenfolge anpassen (10 -> 11 Schritte: Medium
#    bekommt jetzt einen eigenen Schritt statt mit der Wirkstoffmenge
#    zusammengelegt zu sein)
# ─────────────────────────────────────────────────────────────────────────
old2 = """var TOUR_STEPS = [
  {sel:['.mode-toggle'], t:'Modus wählen', b:'Wähle hier, ob du mit rohem Pflanzenmaterial (Blüten) oder einem Extrakt/Konzentrat rechnest. Die restlichen Felder passen sich automatisch an.'},
  {sel:['#carrier-medium-row'], t:'Medium & Menge', b:'Wähle dein Trägermedium (z.B. Butter, MCT-Öl) und gib ein, wie viel Gramm Ausgangsmaterial du tatsächlich eingesetzt hast.'},
  {sel:['#potency'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest — beeinflusst die ganze Rechnung stark. Ohne Test: eher höher schätzen als tiefer — eine Unterschätzung führt leicht zu ungewolltem Nachdosieren und Greening Out.'},
  {sel:['#raw-decarb'], t:'Decarboxyliert?', b:'Entscheidend: Ist dein Material schon aktiviert (decarboxyliert) oder noch Rohwert (THCA)? Im Zweifel „Nein“ wählen — unaktiviertes Material wirkt kaum.'},
  {sel:['#carrier','#portion-c'], t:'Trägermenge & Portion', b:'Wie viel hast du insgesamt hergestellt, und wie viele Gramm Wirkstoffträger stecken in einer fertigen Portion? Beides zusammen bestimmt die Dosis pro Stück.'},
  {sel:['#bioavail'], t:'Aufnahmeform', b:'Wähle die Aufnahmeform. Die Prozentwerte zeigen die durchschnittliche Verfügbarkeit nach Applikationsform aus Studien — individuell kann das spürbar abweichen.'},
  {sel:['#tolerance'], t:'Konsumfrequenz', b:'Pflichtfeld: Deine Konsumhäufigkeit beeinflusst, wie stark eine bestehende Toleranz die wahrscheinliche Wirkschwelle in den Ergebnissen verschiebt.'},
  {sel:['#result-grid'], t:'Ergebnis', b:'Hier siehst du die Gesamtmenge, die Menge pro Portion und die Intensitätseinschätzung.'},
  {sel:['#r-kg-box'], t:'Empfohlene Einstiegsdosis', b:'Das ist deine Startdosis — hier anfangen, nicht bei der Gesamtmenge! Falls eine Toleranz-Warnung mit einer höheren mg-Zahl erscheint: Das ist ausdrücklich keine Empfehlung, sondern nur ein Erfahrungswert.'},
  {sel:['#btn-save-charge'], t:'Charge speichern', b:'Ergebnis merken? Direkt als Charge speichern — inklusive aller Angaben für später.'}
];"""

new2 = """var TOUR_STEPS = [
  {sel:['.mode-toggle'], t:'Modus wählen', b:'Wähle hier, ob du mit rohem Pflanzenmaterial (Blüten) oder einem Extrakt/Konzentrat rechnest. Die restlichen Felder passen sich automatisch an.'},
  {sel:['#ig'], t:'① Eingesetzte Wirkstoffmenge', b:'Wie viel Gramm Blüten oder Extrakt setzt du ein? Wichtig: Das ist die Menge des Cannabis-Ausgangsmaterials — NICHT die Menge deines Trägermediums (Butter, Öl etc.), die kommt gleich in Block ②.'},
  {sel:['#potency'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest — beeinflusst die ganze Rechnung stark. Ohne Test: eher höher schätzen als tiefer — eine Unterschätzung führt leicht zu ungewolltem Nachdosieren und Greening Out.'},
  {sel:['#raw-decarb'], t:'Decarboxyliert?', b:'Entscheidend: Ist dein Material schon aktiviert (decarboxyliert) oder noch Rohwert (THCA)? Im Zweifel „Nein“ wählen — unaktiviertes Material wirkt kaum.'},
  {sel:['#cm'], t:'② Träger / Medium', b:'Womit stellst du her — Butter, MCT-Öl, Gummies? Das bestimmt automatisch die passende Extraktionseffizienz. Hier geht es nur um die Art, die Menge folgt im nächsten Schritt.'},
  {sel:['#carrier','#portion-c'], t:'Trägermenge & Portion', b:'Wie viel hast du insgesamt hergestellt, und wie viele Gramm Wirkstoffträger stecken in einer fertigen Portion? Beides zusammen bestimmt die Dosis pro Stück.'},
  {sel:['#bioavail'], t:'③ Aufnahmeform', b:'Wähle die Aufnahmeform. Die Prozentwerte zeigen die durchschnittliche Verfügbarkeit nach Applikationsform aus Studien — individuell kann das spürbar abweichen.'},
  {sel:['#tolerance'], t:'Konsumfrequenz', b:'Pflichtfeld: Deine Konsumhäufigkeit beeinflusst, wie stark eine bestehende Toleranz die wahrscheinliche Wirkschwelle in den Ergebnissen verschiebt.'},
  {sel:['#result-grid'], t:'Ergebnis', b:'Hier siehst du die Gesamtmenge, die Menge pro Portion und die Intensitätseinschätzung.'},
  {sel:['#r-kg-box'], t:'Empfohlene Einstiegsdosis', b:'Das ist deine Startdosis — hier anfangen, nicht bei der Gesamtmenge! Falls eine Toleranz-Warnung mit einer höheren mg-Zahl erscheint: Das ist ausdrücklich keine Empfehlung, sondern nur ein Erfahrungswert.'},
  {sel:['#btn-save-charge'], t:'Charge speichern', b:'Ergebnis merken? Direkt als Charge speichern — inklusive aller Angaben für später.'}
];"""

if old2 not in content:
    print("WARNUNG 2: TOUR_STEPS nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Tour auf 11 Schritte erweitert, 'Träger/Medium' bekommt eigenen Schritt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
