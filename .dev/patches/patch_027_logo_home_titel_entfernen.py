#!/usr/bin/env python3
# Patch O: 1) Klick auf den Titel "CannGuide" (h1) fuehrt zur Startseite
#             (das Logo/SVG hatte das onclick schon, der Titeltext nicht).
#          2) Moeglichkeit, die App umzubenennen, komplett aus den
#             Einstellungen entfernt (Eingabefeld, setTitle()-Funktion,
#             Wiederherstellung des gespeicherten Titels beim Laden).
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 4

# ─────────────────────────────────────────────────────────────────────────
# 1) Titel-Text klickbar machen -> showPage('home')
# ─────────────────────────────────────────────────────────────────────────
old1 = """    <div><h1 id="app-title">CannGuide</h1><p class="sub" id="app-sub">Guide · Bibliothek · Rechner · Chargen · Prävention</p></div>"""
new1 = """    <div onclick="showPage('home')" style="cursor:pointer"><h1 id="app-title">CannGuide</h1><p class="sub" id="app-sub">Guide · Bibliothek · Rechner · Chargen · Prävention</p></div>"""

if old1 not in content:
    print("WARNUNG 1: Titel-Block (h1/app-sub) nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Klick auf Titel/Untertitel führt jetzt zur Startseite.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Umbenennen-Feld aus den Einstellungen entfernen (HTML)
# ─────────────────────────────────────────────────────────────────────────
old2 = """    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">App-Titel</label>
      <div style="display:flex;gap:8px;margin-top:.375rem">
        <input type="text" id="title-input" placeholder="CannGuide" style="flex:1">
        <button class="btn primary" onclick="setTitle()">✓</button>
      </div>
    </div>
    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">Daten</label>"""

new2 = """    <div class="cr">
      <label class="cl" style="font-size:var(--fs);font-weight:500;color:var(--text2)">Daten</label>"""

if old2 not in content:
    print("WARNUNG 2: Umbenennen-Feld in den Einstellungen nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: 'App-Titel'-Eingabefeld aus den Einstellungen entfernt.")

# ─────────────────────────────────────────────────────────────────────────
# 3) setTitle()-Funktion entfernen
# ─────────────────────────────────────────────────────────────────────────
old3 = """window.setTitle = function() {
  var v=document.getElementById('title-input').value.trim();
  if(v) document.getElementById('app-title').textContent=v;
  try{localStorage.setItem('cannguide_title',v);}catch(e){}
};

"""
new3 = """"""

if old3 not in content:
    print("WARNUNG 3: setTitle()-Funktion nicht (exakt) gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: setTitle()-Funktion entfernt.")

# ─────────────────────────────────────────────────────────────────────────
# 4) Wiederherstellung des gespeicherten Titels beim Laden entfernen
# ─────────────────────────────────────────────────────────────────────────
old4 = """    var tl=localStorage.getItem('cannguide_title'); if(tl) document.getElementById('app-title').textContent=tl;
"""
new4 = """"""

if old4 not in content:
    print("WARNUNG 4: Titel-Wiederherstellung beim Init nicht gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: Wiederherstellung eines gespeicherten Custom-Titels beim Laden entfernt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
