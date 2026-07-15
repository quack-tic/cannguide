#!/usr/bin/env python3
# Patch 037: Tour-Spotlight-Technik komplett gewechselt.
# Vorher: backdrop-filter (Weichzeichner) + mask-image (SVG-Ausschnitt) --
# browserabhaengig unzuverlaessig (Alpha- vs. Luminanz-Maskierung,
# backdrop-filter+mask-Kombination inkonsistent).
# Jetzt: klassische "riesiger box-shadow"-Technik (wie Shepherd.js/Intro.js) --
# ein kleines transparentes Element mit box-shadow:0 0 0 9999px liegt exakt
# ueber dem Ziel und dunkelt so den Rest der Seite ab. Kein mask-image, kein
# backdrop-filter mehr -- seit jeher in jedem Browser absolut zuverlaessig.
# Kompromiss: Hintergrund wird abgedunkelt statt milchig weichgezeichnet.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 3

# ─────────────────────────────────────────────────────────────────────────
# 1) CSS: .tour-overlay (blur+mask) -> .tour-hole (box-shadow-Technik)
# ─────────────────────────────────────────────────────────────────────────
old1 = """.tour-overlay{position:fixed;inset:0;z-index:9997;background:rgba(248,248,250,.32);backdrop-filter:blur(7px);-webkit-backdrop-filter:blur(7px);pointer-events:none;mask-repeat:no-repeat;-webkit-mask-repeat:no-repeat;mask-position:0 0;-webkit-mask-position:0 0}"""
new1 = """.tour-hole{position:fixed;z-index:9997;border-radius:14px;box-shadow:0 0 0 9999px rgba(10,10,14,.72);pointer-events:none;transition:top .2s ease,left .2s ease,width .2s ease,height .2s ease}"""

if old1 not in content:
    print("WARNUNG 1: .tour-overlay CSS nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: CSS auf .tour-hole (box-shadow-Technik) umgestellt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) tourBuildMask() entfernen, tourPositionOverlay() auf Box-Positionierung
#    statt Maske umstellen
# ─────────────────────────────────────────────────────────────────────────
old2 = """function tourBuildMask(b, pad) {
  var w = window.innerWidth, h = window.innerHeight;
  var x = Math.max(0, b.left-pad), y = Math.max(0, b.top-pad);
  var rw = (b.right-b.left)+2*pad, rh = (b.bottom-b.top)+2*pad;
  var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'">'+
    '<rect width="'+w+'" height="'+h+'" fill="white"/>'+
    '<rect x="'+x+'" y="'+y+'" width="'+rw+'" height="'+rh+'" rx="14" ry="14" fill="black" fill-opacity="0"/>'+
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
}"""

new2 = """function tourPositionOverlay(step) {
  var b = tourBounds(step.sel);
  if(!b) return false;
  var pad = 16;
  var x = Math.max(0, b.left-pad), y = Math.max(0, b.top-pad);
  var rw = (b.right-b.left)+2*pad, rh = (b.bottom-b.top)+2*pad;
  tourOverlayEl.style.left = x+'px';
  tourOverlayEl.style.top = y+'px';
  tourOverlayEl.style.width = rw+'px';
  tourOverlayEl.style.height = rh+'px';
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
}"""

if old2 not in content:
    print("WARNUNG 2: tourBuildMask()/tourPositionOverlay() nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: tourBuildMask() entfernt, tourPositionOverlay() nutzt jetzt direkte Box-Positionierung.")

# ─────────────────────────────────────────────────────────────────────────
# 3) startCalcTour(): Element-Klasse tour-overlay -> tour-hole
# ─────────────────────────────────────────────────────────────────────────
old3 = """  tourOverlayEl = document.createElement('div');
  tourOverlayEl.className = 'tour-overlay';
  document.body.appendChild(tourOverlayEl);"""
new3 = """  tourOverlayEl = document.createElement('div');
  tourOverlayEl.className = 'tour-hole';
  document.body.appendChild(tourOverlayEl);"""

if old3 not in content:
    print("WARNUNG 3: startCalcTour()-Element-Erstellung nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: startCalcTour() erstellt jetzt ein .tour-hole-Element.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
