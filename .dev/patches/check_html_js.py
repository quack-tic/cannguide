#!/usr/bin/env python3
import re, subprocess, sys, tempfile, os
html = open('index.html', encoding='utf-8').read()
# Inline-Scripts auch mit Attributen erfassen, <script src=...> aber überspringen
scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.S)
if not scripts:
    print("Kein Inline-<script>-Block gefunden"); sys.exit(1)
js = "\n;\n".join(scripts)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
    f.write(js)
    tmp = f.name
r = subprocess.run(['node', '--check', tmp])
os.unlink(tmp)
if r.returncode == 0:
    print(f"✓ JS-Syntax OK ({len(scripts)} Block/Blöcke geprüft)")
sys.exit(r.returncode)
