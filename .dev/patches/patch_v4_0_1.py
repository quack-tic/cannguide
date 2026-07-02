#!/usr/bin/env python3
"""
CannGuide Hotfix v4.0.1 — im Repo-Root ausführen: python3 patch_v4_0_1.py

Behebt:
  [1] KRITISCH: GPL-Kommentar wurde in den JS-String der Print-Export-
      Funktion injiziert -> SyntaxError -> gesamtes App-JS tot.
  [2] Manifest-Link: /cannguide/ (lowercase) -> relativ ./manifest.json
  [3] Apple-Touch-Icon: falscher Pfad UND falscher Dateiname -> ./icon192.jpg
  [4] SW-Registrierung: /cannguide/service-worker.js existiert nicht
      -> ./serviceworker.js (relativ, case-sicher)
  [5] manifest.json: icon-192.jpg / icon-512.jpg -> icon192.jpg / icon512.jpg

Idempotent: bereits gepatchte Stellen werden erkannt und übersprungen.
"""
import re, subprocess, sys, tempfile, os

def patch_file(path, replacements):
    src = open(path, encoding='utf-8').read()
    changed = 0
    for label, old, new in replacements:
        if old in src:
            src = src.replace(old, new)
            print(f"  ✔ {label}")
            changed += 1
        elif new in src:
            print(f"  · {label} (bereits gepatcht)")
        else:
            print(f"  ✘ {label} — MUSTER NICHT GEFUNDEN, bitte manuell prüfen!")
    if changed:
        open(path, 'w', encoding='utf-8').write(src)
    return changed

print("== index.html ==")
BROKEN_STRING = '''var html = '<!DOCTYPE html><html lang="de">
<!-- CannGuide \u00a9 2024-2026 quack-tic
     Licensed under GNU GPL v3 \u2014 https://github.com/quack-tic/CannGuide --><head>'''
FIXED_STRING = '''var html = '<!DOCTYPE html><html lang="de"><head>'''

patch_file('index.html', [
    ("[1] JS-String repariert (SyntaxError-Fix)", BROKEN_STRING, FIXED_STRING),
    ("[2] Manifest-Link relativ",
     '<link rel="manifest" href="/cannguide/manifest.json">',
     '<link rel="manifest" href="./manifest.json">'),
    ("[3] Apple-Touch-Icon korrigiert",
     '<link rel="apple-touch-icon" href="/cannguide/icon-192.jpg">',
     '<link rel="apple-touch-icon" href="./icon192.jpg">'),
    ("[4] SW-Registrierungspfad korrigiert",
     "navigator.serviceWorker.register('/cannguide/service-worker.js')",
     "navigator.serviceWorker.register('./serviceworker.js')"),
])

print("== manifest.json ==")
patch_file('manifest.json', [
    ("[5a] Icon 192 Dateiname", '"src": "icon-192.jpg"', '"src": "icon192.jpg"'),
    ("[5b] Icon 512 Dateiname", '"src": "icon-512.jpg"', '"src": "icon512.jpg"'),
])

# ── Verifikation: JS aus index.html extrahieren und mit Node prüfen ──────────
print("== Verifikation ==")
html = open('index.html', encoding='utf-8').read()
scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', html, re.DOTALL)
ok = True
for i, s in enumerate(scripts):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(s); tmp = f.name
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode == 0:
        print(f"  ✔ Script-Block {i}: Syntax OK")
    else:
        print(f"  ✘ Script-Block {i}: {r.stderr.strip().splitlines()[-1]}")
        ok = False

import json
try:
    json.load(open('manifest.json', encoding='utf-8'))
    print("  ✔ manifest.json: valides JSON")
except Exception as e:
    print(f"  ✘ manifest.json: {e}"); ok = False

sys.exit(0 if ok else 1)
