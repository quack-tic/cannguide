#!/usr/bin/env python3
# Patch 034: Reparatur der doppelt/inkonsistent eingefuegten Rechner-Tour (Patch 033).
#
# Patch 033 wurde versehentlich zweimal angewendet; die Anker (</style>, INIT-Kommentar)
# waren nicht eindeutig genug fuer die Idempotenz-Pruefung. Dadurch existieren jetzt:
#  - .tour-* CSS doppelt
#  - der komplette JS-Tour-Block doppelt (alte Ellipsen- UND neue Rechteck-Version)
#  - der "Rechner-Tour"-Einstellungs-Button doppelt
#  - id="btn-save-charge" ggf. mehrfach am selben Element
#
# Dieses Patch entfernt ALLE Tour-Bestandteile restlos und setzt sie danach GENAU EINMAL
# in der korrekten (rechteckigen, selbst-neupositionierenden) Version wieder ein.
#
# Idempotent & wiederholbar: arbeitet mit Zaehlungen und definierten Markern.

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

report = []

# ─────────────────────────────────────────────────────────────────────────
# SCHRITT 1: Alle bisherigen Tour-CSS-Zeilen entfernen (.tour-*)
# ─────────────────────────────────────────────────────────────────────────
css_line_re = re.compile(r'^\.tour-(?:overlay|tooltip|step-count|nav|prompt|prompt-card)\b.*\n', re.M)
n_css = len(css_line_re.findall(content))
content = css_line_re.sub('', content)
report.append(f"Entfernte Tour-CSS-Zeilen: {n_css}")

# ─────────────────────────────────────────────────────────────────────────
# SCHRITT 2: Alle JS-Tour-Bloecke entfernen.
# Jeder Block beginnt mit dem Marker-Kommentar und endet unmittelbar vor
# "// ── INIT" ODER vor einem weiteren "// ── RECHNER-TOUR"-Marker.
# ─────────────────────────────────────────────────────────────────────────
tour_marker = '// \u2500\u2500 RECHNER-TOUR'
init_marker = '// \u2500\u2500 INIT'

# Wiederholt entfernen, solange noch ein Tour-Marker existiert
removed_blocks = 0
while tour_marker in content:
    start = content.index(tour_marker)
    # Ende = naechstes Vorkommen von entweder weiterem Tour-Marker oder INIT-Marker, nach start
    rest = content[start+len(tour_marker):]
    next_tour = rest.find(tour_marker)
    next_init = rest.find(init_marker)
    candidates = [x for x in [next_tour, next_init] if x != -1]
    if not candidates:
        # Kein Ende gefunden -> nur bis Dateiende (sollte nicht vorkommen)
        content = content[:start]
    else:
        end_rel = min(candidates)
        end = start + len(tour_marker) + end_rel
        content = content[:start] + content[end:]
    removed_blocks += 1
report.append(f"Entfernte JS-Tour-Bloecke: {removed_blocks}")

# ─────────────────────────────────────────────────────────────────────────
# SCHRITT 3: Alle "Rechner-Tour"-Einstellungs-Bloecke entfernen
# ─────────────────────────────────────────────────────────────────────────
settings_block = re.compile(
    r'\s*<div class="cr">\s*'
    r'<label class="cl"[^>]*>Rechner-Tour</label>\s*'
    r'<div style="margin-top:\.375rem">\s*'
    r'<button class="btn" onclick="resetCalcTour\(\)">[^<]*</button>\s*'
    r'</div>\s*</div>', re.S)
n_settings = len(settings_block.findall(content))
content = settings_block.sub('', content)
report.append(f"Entfernte Einstellungs-Tour-Bloecke: {n_settings}")

# ─────────────────────────────────────────────────────────────────────────
# SCHRITT 4: maybeOfferCalcTour() aus showPage-Hook entfernen (wird neu gesetzt)
# ─────────────────────────────────────────────────────────────────────────
content = content.replace(
    "if(p==='calc') { renderTerpeneGrid(); calcUpdate(); maybeOfferCalcTour(); }",
    "if(p==='calc') { renderTerpeneGrid(); calcUpdate(); }")

# ─────────────────────────────────────────────────────────────────────────
# SCHRITT 5: id="btn-save-charge"-Dopplung am Button bereinigen
# (kann durch doppelten str_replace am selben Element entstanden sein)
# ─────────────────────────────────────────────────────────────────────────
# doppelte id-Attribute -> auf genau eines reduzieren
content = re.sub(
    r'(<button class="btn primary")(?:\s+id="btn-save-charge")+(\s+onclick="saveToCharge\(\)">)',
    r'\1 id="btn-save-charge"\2', content)
# Falls gar keine id vorhanden (durch frueheres Entfernen), wieder setzen:
if 'id="btn-save-charge"' not in content:
    content = content.replace(
        '<button class="btn primary" onclick="saveToCharge()">+ Als Charge speichern</button>',
        '<button class="btn primary" id="btn-save-charge" onclick="saveToCharge()">+ Als Charge speichern</button>')
report.append("btn-save-charge id normalisiert (genau 1x)")

# ─────────────────────────────────────────────────────────────────────────
# JETZT: sauber genau einmal neu einsetzen
# ─────────────────────────────────────────────────────────────────────────

# 6a) CSS wieder direkt vor </style> einsetzen (genau einmal)
tour_css = """.tour-overlay{position:fixed;inset:0;z-index:9997;background:rgba(248,248,250,.32);backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);pointer-events:none;mask-repeat:no-repeat;-webkit-mask-repeat:no-repeat;mask-position:0 0;-webkit-mask-position:0 0}
.tour-tooltip{position:fixed;z-index:9999;width:300px;max-width:90vw;background:var(--bg2);border:1px solid var(--border2);border-radius:var(--radius-lg);padding:1rem 1.125rem;box-shadow:0 10px 40px rgba(0,0,0,.5);font-size:var(--fs-sm);color:var(--text2);line-height:1.55}
.tour-tooltip h4{font-size:var(--fs);font-weight:700;color:var(--text);margin:0 0 .4rem}
.tour-tooltip p{margin:0}
.tour-step-count{font-size:10px;color:var(--text3);margin-bottom:.4rem;letter-spacing:.05em;text-transform:uppercase}
.tour-nav{display:flex;justify-content:space-between;align-items:center;margin-top:.85rem;gap:8px}
.tour-nav .tour-skip{cursor:pointer;color:var(--text3);font-size:var(--fs-xs)}
.tour-prompt{position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;padding:1.5rem}
.tour-prompt-card{background:var(--bg2);border:1px solid var(--border2);border-radius:var(--radius-lg);padding:1.5rem;max-width:340px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.55)}
</style>"""
assert content.count('</style>') >= 1, "kein </style> gefunden"
content = content.replace('</style>', tour_css, 1)
report.append("CSS neu eingesetzt (1x)")

# 6b) showPage-Hook wieder mit maybeOfferCalcTour ergaenzen
content = content.replace(
    "if(p==='calc') { renderTerpeneGrid(); calcUpdate(); }",
    "if(p==='calc') { renderTerpeneGrid(); calcUpdate(); maybeOfferCalcTour(); }")
report.append("showPage-Hook neu gesetzt (1x)")

# 6c) Einstellungs-Button wieder einsetzen (genau einmal, vor dem Daten-Block)
settings_anchor = """    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">Daten</label>"""
settings_new = """    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">Rechner-Tour</label>
      <div style="margin-top:.375rem">
        <button class="btn" onclick="resetCalcTour()">\U0001F9ED Tour erneut anzeigen</button>
      </div>
    </div>
    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">Daten</label>"""
assert content.count(settings_anchor) == 1, f"Daten-Anker nicht eindeutig ({content.count(settings_anchor)}x)"
content = content.replace(settings_anchor, settings_new, 1)
report.append("Einstellungs-Button neu eingesetzt (1x)")

# 6d) JS-Tour-Logik wieder genau einmal vor INIT einsetzen
tour_js = """// \u2500\u2500 RECHNER-TOUR \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
var TOUR_STEPS = [
  {sel:['.mode-toggle'], t:'Modus w\u00e4hlen', b:'W\u00e4hle hier, ob du mit rohem Pflanzenmaterial (Bl\u00fcten) oder einem Extrakt/Konzentrat rechnest. Die restlichen Felder passen sich automatisch an.'},
  {sel:['#carrier-medium-row'], t:'Medium & Menge', b:'W\u00e4hle dein Tr\u00e4germedium (z.B. Butter, MCT-\u00d6l) und gib ein, wie viel Gramm Ausgangsmaterial du tats\u00e4chlich eingesetzt hast.'},
  {sel:['#potency'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest \u2014 beeinflusst die ganze Rechnung stark. Ohne Test: eher h\u00f6her sch\u00e4tzen als tiefer \u2014 eine Untersch\u00e4tzung f\u00fchrt leicht zu ungewolltem Nachdosieren und Greening Out.'},
  {sel:['#raw-decarb'], t:'Decarboxyliert?', b:'Entscheidend: Ist dein Material schon aktiviert (decarboxyliert) oder noch Rohwert (THCA)? Im Zweifel \u201eNein\u201c w\u00e4hlen \u2014 unaktiviertes Material wirkt kaum.'},
  {sel:['#carrier','#portion-c'], t:'Tr\u00e4germenge & Portion', b:'Wie viel hast du insgesamt hergestellt, und wie viele Gramm Wirkstofftr\u00e4ger stecken in einer fertigen Portion? Beides zusammen bestimmt die Dosis pro St\u00fcck.'},
  {sel:['#bioavail'], t:'Aufnahmeform', b:'W\u00e4hle die Aufnahmeform. Die Prozentwerte zeigen die durchschnittliche Verf\u00fcgbarkeit nach Applikationsform aus Studien \u2014 individuell kann das sp\u00fcrbar abweichen.'},
  {sel:['#tolerance'], t:'Konsumfrequenz', b:'Pflichtfeld: Deine Konsumh\u00e4ufigkeit beeinflusst, wie stark eine bestehende Toleranz die wahrscheinliche Wirkschwelle in den Ergebnissen verschiebt.'},
  {sel:['#result-grid'], t:'Ergebnis', b:'Hier siehst du die Gesamtmenge, die Menge pro Portion und die Intensit\u00e4tseinsch\u00e4tzung.'},
  {sel:['#r-kg-box'], t:'Empfohlene Einstiegsdosis', b:'Das ist deine Startdosis \u2014 hier anfangen, nicht bei der Gesamtmenge! Falls eine Toleranz-Warnung mit einer h\u00f6heren mg-Zahl erscheint: Das ist ausdr\u00fccklich keine Empfehlung, sondern nur ein Erfahrungswert.'},
  {sel:['#btn-save-charge'], t:'Charge speichern', b:'Ergebnis merken? Direkt als Charge speichern \u2014 inklusive aller Angaben f\u00fcr sp\u00e4ter.'}
];
var tourIdx = 0, tourOverlayEl = null, tourTooltipEl = null;

function tourBounds(sel) {
  var els = sel.map(function(s){ var el = document.querySelector(s); if(!el) return null; return el.closest('.cr') || el; }).filter(Boolean);
  if(!els.length) return null;
  var rects = els.map(function(e){ return e.getBoundingClientRect(); });
  return {
    top: Math.min.apply(null, rects.map(function(r){return r.top;})),
    left: Math.min.apply(null, rects.map(function(r){return r.left;})),
    bottom: Math.max.apply(null, rects.map(function(r){return r.bottom;})),
    right: Math.max.apply(null, rects.map(function(r){return r.right;}))
  };
}

function tourBuildMask(b, pad) {
  var w = window.innerWidth, h = window.innerHeight;
  var x = Math.max(0, b.left-pad), y = Math.max(0, b.top-pad);
  var rw = (b.right-b.left)+2*pad, rh = (b.bottom-b.top)+2*pad;
  var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'">'+
    '<rect width="'+w+'" height="'+h+'" fill="white"/>'+
    '<rect x="'+x+'" y="'+y+'" width="'+rw+'" height="'+rh+'" rx="14" ry="14" fill="black"/>'+
    '</svg>';
  return 'url("data:image/svg+xml,'+encodeURIComponent(svg)+'")';
}

function tourPositionOverlay(step) {
  var b = tourBounds(step.sel);
  if(!b) return false;
  var pad = 16;
  var mask = tourBuildMask(b, pad);
  tourOverlayEl.style.maskImage = mask;
  tourOverlayEl.style.webkitMaskImage = mask;
  var cx = (b.left+b.right)/2;
  var tw = 300;
  var top = b.bottom+pad+18;
  if(top+170 > window.innerHeight) top = Math.max(12, b.top-pad-170);
  var left = Math.min(Math.max(12, cx-tw/2), window.innerWidth-tw-12);
  tourTooltipEl.style.top = top+'px';
  tourTooltipEl.style.left = left+'px';
  var targetEl = document.querySelector(step.sel[0]);
  if(targetEl && typeof targetEl.scrollIntoView === 'function') targetEl.scrollIntoView({behavior:'smooth', block:'center'});
  return true;
}

var tourRepositionTimer = null;
function tourStartRepositioning() {
  if(tourRepositionTimer) clearInterval(tourRepositionTimer);
  tourRepositionTimer = setInterval(function(){
    if(!tourOverlayEl) return;
    tourPositionOverlay(TOUR_STEPS[tourIdx]);
  }, 150);
}
function tourStopRepositioning() {
  if(tourRepositionTimer) { clearInterval(tourRepositionTimer); tourRepositionTimer = null; }
}

function tourRenderStep() {
  if(!tourOverlayEl) return;
  var step = TOUR_STEPS[tourIdx];
  var ok = tourPositionOverlay(step);
  if(!ok) { window.tourNext(); return; }
  tourStartRepositioning();
  tourTooltipEl.innerHTML =
    '<div class="tour-step-count">Schritt '+(tourIdx+1)+' / '+TOUR_STEPS.length+'</div>'+
    '<h4>'+step.t+'</h4><p>'+step.b+'</p>'+
    '<div class="tour-nav">'+
      '<span class="tour-skip" onclick="endCalcTour()">\u00dcberspringen</span>'+
      '<div style="display:flex;gap:6px">'+
        (tourIdx>0 ? '<button class="btn" onclick="tourPrev()">\u2190 Zur\u00fcck</button>' : '')+
        '<button class="btn primary" onclick="tourNext()">'+(tourIdx===TOUR_STEPS.length-1?'Fertig':'Weiter \u2192')+'</button>'+
      '</div>'+
    '</div>';
}

window.tourNext = function() {
  if(tourIdx >= TOUR_STEPS.length-1) { endCalcTour(); return; }
  tourIdx++;
  tourRenderStep();
};
window.tourPrev = function() {
  if(tourIdx<=0) return;
  tourIdx--;
  tourRenderStep();
};
window.endCalcTour = function() {
  tourStopRepositioning();
  if(tourOverlayEl) { tourOverlayEl.remove(); tourOverlayEl = null; }
  if(tourTooltipEl) { tourTooltipEl.remove(); tourTooltipEl = null; }
  window.removeEventListener('resize', tourRenderStep);
  try { localStorage.setItem('cannguide_calc_tour_done', '1'); } catch(e) {}
};
window.startCalcTour = function() {
  setCalcMode('raw');
  calcUpdate();
  tourIdx = 0;
  tourOverlayEl = document.createElement('div');
  tourOverlayEl.className = 'tour-overlay';
  document.body.appendChild(tourOverlayEl);
  tourTooltipEl = document.createElement('div');
  tourTooltipEl.className = 'tour-tooltip';
  document.body.appendChild(tourTooltipEl);
  window.addEventListener('resize', tourRenderStep);
  setTimeout(tourRenderStep, 60);
};
window.maybeOfferCalcTour = function() {
  var done;
  try { done = localStorage.getItem('cannguide_calc_tour_done'); } catch(e) { done = null; }
  if(done) return;
  var wrap = document.createElement('div');
  wrap.className = 'tour-prompt';
  wrap.id = 'tour-prompt-el';
  wrap.innerHTML = '<div class="tour-prompt-card">'+
    '<div style="font-size:28px;margin-bottom:.5rem">\U0001F9ED</div>'+
    '<div style="font-weight:700;font-size:var(--fs-lg);margin-bottom:.5rem">Kurze Einf\u00fchrung ansehen?</div>'+
    '<div style="font-size:var(--fs-sm);color:var(--text2);margin-bottom:1.1rem;line-height:1.5">Wir zeigen dir in 10 kurzen Schritten, wie der Dosierungsrechner funktioniert.</div>'+
    '<div style="display:flex;gap:8px;justify-content:center">'+
      '<button class="btn" onclick="dismissTourPrompt(false)">\u00dcberspringen</button>'+
      '<button class="btn primary" onclick="dismissTourPrompt(true)">Ja, zeigen</button>'+
    '</div></div>';
  document.body.appendChild(wrap);
};
window.dismissTourPrompt = function(startIt) {
  var el = document.getElementById('tour-prompt-el');
  if(el) el.remove();
  if(startIt) { startCalcTour(); }
  else { try { localStorage.setItem('cannguide_calc_tour_done', '1'); } catch(e) {} }
};
window.resetCalcTour = function() {
  try { localStorage.removeItem('cannguide_calc_tour_done'); } catch(e) {}
  showPage('calc');
  setTimeout(function(){ startCalcTour(); }, 80);
};

// \u2500\u2500 INIT"""

assert content.count(init_marker) == 1, f"INIT-Marker nicht eindeutig ({content.count(init_marker)}x)"
content = content.replace(init_marker, tour_js, 1)
report.append("JS-Tour-Logik neu eingesetzt (1x)")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("REPARATUR ABGESCHLOSSEN:")
for r in report:
    print("  - " + r)
