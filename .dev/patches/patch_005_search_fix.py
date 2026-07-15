#!/usr/bin/env python3
"""
Patch: Landing-Page-Suche springt direkt zum passenden Lexikon-/Bibliothekseintrag
statt nur auf die Bibliothek zu verweisen.

Idempotent: kann mehrfach ausgeführt werden ohne doppelte Patches.
"""
import re
import sys

PATH = "index.html"

with open(PATH, "r", encoding="utf-8") as f:
    html = f.read()

changed = False

# ── 1) Suchfeld auf der Landing Page: id + neuer Handler ───────────────────
old_search_block = '''  <div class="ksearch">
    <span class="mag"></span>
    <input type="text" placeholder="Wissen durchsuchen — Wirkstoff, Begriff oder Frage…" onkeydown="if(event.key==='Enter')showPage('library')" />
    <button class="go" onclick="showPage('library')">Suchen</button>
  </div>'''

new_search_block = '''  <div class="ksearch">
    <span class="mag"></span>
    <input type="text" id="ksearch-input" placeholder="Wissen durchsuchen — Wirkstoff, Begriff oder Frage…" onkeydown="if(event.key==='Enter'){doGlobalSearch()}" />
    <button class="go" onclick="doGlobalSearch()">Suchen</button>
  </div>'''

if old_search_block in html:
    html = html.replace(old_search_block, new_search_block)
    changed = True
    print("✔ Suchfeld gepatcht (id + doGlobalSearch)")
elif "doGlobalSearch()" in html and 'id="ksearch-input"' in html:
    print("• Suchfeld war bereits gepatcht, überspringe")
else:
    print("✘ FEHLER: Such-Block nicht gefunden — Datei manuell prüfen", file=sys.stderr)
    sys.exit(1)

# ── 2) CSS: Highlight-Animation für Treffer ─────────────────────────────────
css_anchor = ".le{padding:10px 0;border-bottom:1px solid var(--border);cursor:pointer}"
css_addition = ".le{padding:10px 0;border-bottom:1px solid var(--border);cursor:pointer}\n.le.hl{animation:leHl 2s ease}\n@keyframes leHl{0%{background:var(--accent-bg)}100%{background:transparent}}"

if css_anchor in html and ".le.hl{animation:leHl" not in html:
    html = html.replace(css_anchor, css_addition)
    changed = True
    print("✔ CSS-Highlight-Animation ergänzt")
elif ".le.hl{animation:leHl" in html:
    print("• CSS-Highlight war bereits vorhanden, überspringe")
else:
    print("✘ FEHLER: CSS-Anker für .le nicht gefunden", file=sys.stderr)
    sys.exit(1)

# ── 3) JS: doGlobalSearch + Hilfsfunktionen, direkt vor renderLib einfügen ──
js_anchor = "// ── LIBRARY ───────────────────────────────────────────────────────────────\nwindow.renderLib = function() {"

js_addition = '''// ── GLOBALE SUCHE ────────────────────────────────────────────────────────
function stripHtml(str) {
  return String(str).replace(/<[^>]*>/g, ' ').replace(/\\s+/g, ' ').trim();
}

function searchIndex(query) {
  var q = query.toLowerCase();
  var titleHits = [];
  var bodyHits = [];
  Object.keys(LIB).forEach(function(cat) {
    LIB[cat].items.forEach(function(item, i) {
      var title = stripHtml(item.t).toLowerCase();
      var body = stripHtml(item.b).toLowerCase();
      if (title.indexOf(q) !== -1) {
        titleHits.push({page: 'library', cat: cat, index: i});
      } else if (body.indexOf(q) !== -1) {
        bodyHits.push({page: 'library', cat: cat, index: i});
      }
    });
  });
  if (typeof SAFETY !== 'undefined') {
    Object.keys(SAFETY).forEach(function(cat) {
      SAFETY[cat].items.forEach(function(item, i) {
        var title = stripHtml(item.t).toLowerCase();
        var body = stripHtml(item.b).toLowerCase();
        if (title.indexOf(q) !== -1) {
          titleHits.push({page: 'safety', cat: cat, index: i});
        } else if (body.indexOf(q) !== -1) {
          bodyHits.push({page: 'safety', cat: cat, index: i});
        }
      });
    });
  }
  return titleHits.concat(bodyHits);
}

window.doGlobalSearch = function() {
  var inputEl = document.getElementById('ksearch-input');
  var query = inputEl ? inputEl.value.trim() : '';
  if (!query) { showPage('library'); return; }

  var hits = searchIndex(query);
  if (!hits.length) {
    showPage('library');
    var box = document.getElementById('lib-content');
    if (box) {
      box.insertAdjacentHTML('afterbegin',
        '<div style="background:var(--bg3);border-radius:var(--radius);padding:10px 14px;margin-bottom:1rem;font-size:var(--fs-sm);color:var(--text2)">' +
        'Keine Treffer für "' + query.replace(/</g, '&lt;') + '". Hier ist die Bibliothek.</div>');
    }
    return;
  }

  var hit = hits[0];
  if (hit.page === 'safety') {
    activeSafetyCat = hit.cat;
    showPage('safety');
    setTimeout(function() { jumpToEntry('s' + hit.cat + hit.index); }, 60);
  } else {
    activeLibCat = hit.cat;
    showPage('library');
    setTimeout(function() { jumpToEntry('l' + hit.cat + hit.index); }, 60);
  }
};

function jumpToEntry(id) {
  var el = document.getElementById(id);
  if (!el) return;
  el.classList.add('open');
  var row = el.closest('.le');
  if (row) {
    row.scrollIntoView({behavior: 'smooth', block: 'center'});
    row.classList.add('hl');
    setTimeout(function() { row.classList.remove('hl'); }, 2000);
  }
}

// ── LIBRARY ───────────────────────────────────────────────────────────────
window.renderLib = function() {'''

if js_anchor in html and "window.doGlobalSearch = function" not in html:
    html = html.replace(js_anchor, js_addition)
    changed = True
    print("✔ JS-Suchlogik eingefügt (doGlobalSearch, searchIndex, jumpToEntry)")
elif "window.doGlobalSearch = function" in html:
    print("• JS-Suchlogik war bereits vorhanden, überspringe")
else:
    print("✘ FEHLER: JS-Anker vor renderLib nicht gefunden", file=sys.stderr)
    sys.exit(1)

if changed:
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("\n✅ Patch angewendet. Jetzt: node --check index.html && git add -A && git commit -m 'Landing-Suche springt direkt zu Bibliotheks-/Sicherheitseintrag' && git push")
else:
    print("\nKeine Änderungen nötig.")
