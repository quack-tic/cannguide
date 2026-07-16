#!/usr/bin/env python3
# Patch 057 (ueberarbeitet): Die Tour unterstuetzt jetzt BEIDE Modi
# (Bluete/Extrakt) gleichwertig, statt den Modus-Wechsel zu sperren.
#
# 1) tourBounds() filtert jetzt EINZELN unsichtbare Elemente aus einer
#    Mehrfach-Auswahl heraus, bevor die Bounding-Box berechnet wird -- so
#    kann ein Schritt zwei alternative Ziel-Selektoren angeben (z.B. das
#    Bluetenfeld ODER das Extraktfeld), und es zaehlt automatisch nur das
#    gerade sichtbare.
# 2) TOUR_STEPS: "Wirkstoffgehalt" und "Decarboxyliert?" zeigen jetzt auf
#    BEIDE moeglichen Ziele (Bluete + Extrakt) -- die Tour passt sich live
#    an, wenn waehrend Schritt 1 der Modus gewechselt wird. Kein
#    Ueberspringen, kein Sperren mehr noetig.
# 3) Als zusaetzliches Sicherheitsnetz (falls doch mal ein Ziel komplett
#    fehlt): die Ueberspring-Logik respektiert weiterhin die Navigations-
#    richtung, damit "Zurueck" nie in eine Vorwaerts-Falle laeuft.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 4

# ─────────────────────────────────────────────────────────────────────────
# 1) tourBounds(): einzeln unsichtbare Elemente aus der Auswahl filtern
# ─────────────────────────────────────────────────────────────────────────
old1 = """function tourBounds(sel) {
  var els = sel.map(function(s){ var el = document.querySelector(s); if(!el) return null; return el.closest('.cr') || el; }).filter(Boolean);
  if(!els.length) return null;
  var rects = els.map(function(e){ return e.getBoundingClientRect(); });
  var visible = rects.some(function(r){ return r.width > 0 && r.height > 0; });
  if(!visible) return null;
  return {
    top: Math.min.apply(null, rects.map(function(r){return r.top;})),
    left: Math.min.apply(null, rects.map(function(r){return r.left;})),
    bottom: Math.max.apply(null, rects.map(function(r){return r.bottom;})),
    right: Math.max.apply(null, rects.map(function(r){return r.right;}))
  };
}"""

new1 = """function tourBounds(sel) {
  var els = sel.map(function(s){ var el = document.querySelector(s); if(!el) return null; return el.closest('.cr') || el; }).filter(Boolean);
  if(!els.length) return null;
  var rects = els.map(function(e){ return e.getBoundingClientRect(); }).filter(function(r){ return r.width > 0 && r.height > 0; });
  if(!rects.length) return null;
  return {
    top: Math.min.apply(null, rects.map(function(r){return r.top;})),
    left: Math.min.apply(null, rects.map(function(r){return r.left;})),
    bottom: Math.max.apply(null, rects.map(function(r){return r.bottom;})),
    right: Math.max.apply(null, rects.map(function(r){return r.right;}))
  };
}"""

if old1 not in content:
    print("WARNUNG 1: tourBounds() nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: tourBounds() filtert jetzt einzeln unsichtbare Elemente korrekt heraus.")

# ─────────────────────────────────────────────────────────────────────────
# 2) TOUR_STEPS: Wirkstoffgehalt & Decarboxyliert zeigen auf beide Modi
# ─────────────────────────────────────────────────────────────────────────
old2 = """  {sel:['#potency'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest — beeinflusst die ganze Rechnung stark. Ohne Test: eher höher schätzen als tiefer — eine Unterschätzung führt leicht zu ungewolltem Nachdosieren und Greening Out.'},
  {sel:['#raw-decarb'], t:'Decarboxyliert?', b:'Entscheidend: Ist dein Material schon aktiviert (decarboxyliert) oder noch Rohwert (THCA)? Im Zweifel „Nein“ wählen — unaktiviertes Material wirkt kaum.'},"""

new2 = """  {sel:['#potency','#potency-ext'], t:'Wirkstoffgehalt', b:'Der %-Wert von der Verpackung oder einem Labortest — beeinflusst die ganze Rechnung stark. Ohne Test: eher höher schätzen als tiefer — eine Unterschätzung führt leicht zu ungewolltem Nachdosieren und Greening Out. Im Extrakt-Modus wählt "Extrakt-Typ" automatisch einen sinnvollen Startwert.'},
  {sel:['#raw-decarb','#extract-decarb'], t:'Decarboxyliert?', b:'Entscheidend: Ist dein Material schon aktiviert (decarboxyliert) oder noch Rohwert (THCA)? Im Zweifel „Nein“ wählen — unaktiviertes Material wirkt kaum.'},"""

if old2 not in content:
    print("WARNUNG 2: TOUR_STEPS (Wirkstoffgehalt/Decarboxyliert) nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: 'Wirkstoffgehalt' und 'Decarboxyliert?' zielen jetzt auf Blüten- UND Extrakt-Feld gleichzeitig.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Richtungsvariable + richtungsbewusstes Überspringen (Sicherheitsnetz)
# ─────────────────────────────────────────────────────────────────────────
old3 = """var tourIdx = 0, tourOverlayEl = null, tourTooltipEl = null;"""
new3 = """var tourIdx = 0, tourOverlayEl = null, tourTooltipEl = null, tourDirection = 1;"""

if old3 not in content:
    print("WARNUNG 3: tourIdx-Deklaration nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: Richtungsvariable 'tourDirection' ergänzt (Sicherheitsnetz).")

old3b = """  var ok = tourPositionOverlay(step);
  if(!ok) { window.tourNext(); return; }"""
new3b = """  var ok = tourPositionOverlay(step);
  if(!ok) { if(tourDirection<0) window.tourPrev(); else window.tourNext(); return; }"""

old3c = """window.tourNext = function() {
  if(tourIdx >= TOUR_STEPS.length-1) { endCalcTour(); return; }
  tourIdx++;
  tourRenderStep();
};
window.tourPrev = function() {
  if(tourIdx<=0) return;
  tourIdx--;
  tourRenderStep();
};"""
new3c = """window.tourNext = function() {
  tourDirection = 1;
  if(tourIdx >= TOUR_STEPS.length-1) { endCalcTour(); return; }
  tourIdx++;
  tourRenderStep();
};
window.tourPrev = function() {
  tourDirection = -1;
  if(tourIdx<=0) return;
  tourIdx--;
  tourRenderStep();
};"""

if old3b not in content or old3c not in content:
    print("WARNUNG 3b: Navigations-Funktionen nicht (vollständig) gefunden.")
else:
    content = content.replace(old3b, new3b).replace(old3c, new3c)
    changes += 1
    print(f"4/{total}: Überspring-Logik respektiert Navigationsrichtung (falls ein Ziel doch mal ganz fehlt).")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
