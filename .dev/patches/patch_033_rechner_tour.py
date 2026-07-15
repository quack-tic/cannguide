#!/usr/bin/env python3
# Patch 033: Onboarding-Tour fuer den Rechner.
# - Spotlight-Effekt: Seite wird milchig/verblasst, nur ein ausgeschnittener
#   Bereich um das jeweilige Element bleibt klar sichtbar (CSS mask-image).
# - Startet beim ersten Besuch der Rechner-Seite mit einem Hinweis-Dialog
#   ("Kurze Einfuehrung ansehen?" Ja / Ueberspringen).
# - Merkt sich den Zustand in localStorage (nur einmal automatisch).
# - Einstellungen bekommen einen Button, um die Tour jederzeit erneut zu starten.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 5

# ─────────────────────────────────────────────────────────────────────────
# 1) CSS fuer Overlay, Tooltip und Prompt-Dialog
# ─────────────────────────────────────────────────────────────────────────
old1 = """</style>"""
new1 = """.tour-overlay{position:fixed;inset:0;z-index:9997;background:rgba(248,248,250,.32);backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);pointer-events:none;mask-repeat:no-repeat;-webkit-mask-repeat:no-repeat;mask-position:0 0;-webkit-mask-position:0 0}
.tour-tooltip{position:fixed;z-index:9999;width:300px;max-width:90vw;background:var(--bg2);border:1px solid var(--border2);border-radius:var(--radius-lg);padding:1rem 1.125rem;box-shadow:0 10px 40px rgba(0,0,0,.5);font-size:var(--fs-sm);color:var(--text2);line-height:1.55}
.tour-tooltip h4{font-size:var(--fs);font-weight:700;color:var(--text);margin:0 0 .4rem}
.tour-tooltip p{margin:0}
.tour-step-count{font-size:10px;color:var(--text3);margin-bottom:.4rem;letter-spacing:.05em;text-transform:uppercase}
.tour-nav{display:flex;justify-content:space-between;align-items:center;margin-top:.85rem;gap:8px}
.tour-nav .tour-skip{cursor:pointer;color:var(--text3);font-size:var(--fs-xs)}
.tour-prompt{position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;padding:1.5rem}
.tour-prompt-card{background:var(--bg2);border:1px solid var(--border2);border-radius:var(--radius-lg);padding:1.5rem;max-width:340px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.55)}
</style>"""

if old1 not in content:
    print("WARNUNG 1: </style>-Ende nicht gefunden.")
else:
    content = content.replace(old1, new1, 1)
    changes += 1
    print(f"1/{total}: CSS für Tour-Overlay, Tooltip und Prompt-Dialog eingefügt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Eindeutige ID fuer den "Als Charge speichern"-Button (Tour-Ziel)
# ─────────────────────────────────────────────────────────────────────────
old2 = """<button class="btn primary" onclick="saveToCharge()">+ Als Charge speichern</button>"""
new2 = """<button class="btn primary" id="btn-save-charge" onclick="saveToCharge()">+ Als Charge speichern</button>"""

if old2 not in content:
    print("WARNUNG 2: Charge-Speichern-Button nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: ID für 'Als Charge speichern'-Button ergänzt.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Einstellungen: Button zum erneuten Anzeigen der Tour
# ─────────────────────────────────────────────────────────────────────────
old3 = """    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">Daten</label>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:.375rem">
        <button class="btn" onclick="exportData()">↓ JSON Export</button>
        <button class="btn danger" onclick="clearCharges()">✕ Chargen löschen</button>
      </div>
    </div>
  </div>
</div>"""

new3 = """    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">Rechner-Tour</label>
      <div style="margin-top:.375rem">
        <button class="btn" onclick="resetCalcTour()">🧭 Tour erneut anzeigen</button>
      </div>
    </div>
    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">Daten</label>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:.375rem">
        <button class="btn" onclick="exportData()">↓ JSON Export</button>
        <button class="btn danger" onclick="clearCharges()">✕ Chargen löschen</button>
      </div>
    </div>
  </div>
</div>"""

if old3 not in content:
    print("WARNUNG 3: Einstellungen-Datenblock nicht (exakt) gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: Button 'Tour erneut anzeigen' in Einstellungen eingefügt.")

# ─────────────────────────────────────────────────────────────────────────
# 4) showPage() um Tour-Angebot erweitern
# ─────────────────────────────────────────────────────────────────────────
old4 = """  if(p==='calc') { renderTerpeneGrid(); calcUpdate(); }"""
new4 = """  if(p==='calc') { renderTerpeneGrid(); calcUpdate(); maybeOfferCalcTour(); }"""

if old4 not in content:
    print("WARNUNG 4: showPage()-Calc-Zeile nicht gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: showPage() bietet die Tour beim Rechner-Besuch an.")

# ─────────────────────────────────────────────────────────────────────────
# 5) Komplette Tour-Logik (JS) vor dem INIT-Block einfuegen
# ─────────────────────────────────────────────────────────────────────────
old5 = """// ── INIT ──────────────────────────────────────────────────────────────────
(function init(){"""

new5 = """// ── RECHNER-TOUR ──────────────────────────────────────────────────────────
var TOUR_STEPS = [
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
      '<span class="tour-skip" onclick="endCalcTour()">Überspringen</span>'+
      '<div style="display:flex;gap:6px">'+
        (tourIdx>0 ? '<button class="btn" onclick="tourPrev()">← Zurück</button>' : '')+
        '<button class="btn primary" onclick="tourNext()">'+(tourIdx===TOUR_STEPS.length-1?'Fertig':'Weiter →')+'</button>'+
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
    '<div style="font-size:28px;margin-bottom:.5rem">🧭</div>'+
    '<div style="font-weight:700;font-size:var(--fs-lg);margin-bottom:.5rem">Kurze Einführung ansehen?</div>'+
    '<div style="font-size:var(--fs-sm);color:var(--text2);margin-bottom:1.1rem;line-height:1.5">Wir zeigen dir in 10 kurzen Schritten, wie der Dosierungsrechner funktioniert.</div>'+
    '<div style="display:flex;gap:8px;justify-content:center">'+
      '<button class="btn" onclick="dismissTourPrompt(false)">Überspringen</button>'+
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

// ── INIT ──────────────────────────────────────────────────────────────────
(function init(){"""

if old5 not in content:
    print("WARNUNG 5: INIT-Block nicht gefunden — Tour-Logik nicht eingefügt.")
else:
    content = content.replace(old5, new5)
    changes += 1
    print(f"5/{total}: Komplette Tour-Logik (JS) eingefügt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
