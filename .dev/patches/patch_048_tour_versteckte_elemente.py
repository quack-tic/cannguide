#!/usr/bin/env python3
# Patch 048: Tour-Robustheit. Wenn waehrend der Tour der Modus (Bluete/Extrakt)
# gewechselt wird, kann ein Zielelement des aktuellen Schritts unsichtbar
# werden (display:none am Elternelement) -- getBoundingClientRect() liefert
# dann eine 0x0-Box bei Position (0,0), wodurch die Tour-Blase oben links
# haengenblieb. Fix: tourBounds() erkennt unsichtbare/nullgrosse Elemente
# und behandelt sie wie "nicht gefunden" -> der Schritt wird automatisch
# uebersprungen (bestehende Fallback-Logik in tourRenderStep greift bereits).
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """function tourBounds(sel) {
  var els = sel.map(function(s){ var el = document.querySelector(s); if(!el) return null; return el.closest('.cr') || el; }).filter(Boolean);
  if(!els.length) return null;
  var rects = els.map(function(e){ return e.getBoundingClientRect(); });
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

if old1 not in content:
    print("WARNUNG 1: tourBounds() nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: tourBounds() erkennt versteckte Elemente und überspringt den Schritt automatisch.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
