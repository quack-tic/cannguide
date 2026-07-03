#!/usr/bin/env python3
# Patch 3: Effizienz-Slider im Extrakt-Modus ausblenden (eEff ignoriert ihn ohnehin)
import sys

with open('index.html', encoding='utf-8') as f:
    html = f.read()

changed = False

# 3a: ID auf den Slider-Container
old_div = '''    <!-- Effizienz -->
    <div class="cr">
      <label class="cl">Extraktionseffizienz:'''
new_div = '''    <!-- Effizienz -->
    <div class="cr" id="eff-row">
      <label class="cl">Extraktionseffizienz:'''
if 'id="eff-row"' in html:
    print('  [skip] 3a: eff-row-ID existiert bereits.')
elif old_div in html:
    html = html.replace(old_div, new_div, 1)
    print('  [ok]   3a: eff-row-ID gesetzt.')
    changed = True
else:
    sys.exit('  [FAIL] 3a: Slider-Container nicht gefunden — Pattern prüfen!')

# 3b: Hide-Logik in setCalcMode
anchor = "var ef = document.getElementById('edible-fields'); if(ef) ef.style.display = m==='inhale'?'none':'block';"
insert = "\n  var er = document.getElementById('eff-row'); if(er) er.style.display = m==='extract'?'none':'block';"
if "getElementById('eff-row')" in html:
    print('  [skip] 3b: Hide-Logik existiert bereits.')
elif anchor in html:
    html = html.replace(anchor, anchor + insert, 1)
    print('  [ok]   3b: eff-row wird im Extrakt-Modus ausgeblendet.')
    changed = True
else:
    sys.exit('  [FAIL] 3b: Anker in setCalcMode nicht gefunden — Pattern prüfen!')

if changed:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
print('Patch 3 geschrieben.')
