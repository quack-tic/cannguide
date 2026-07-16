#!/usr/bin/env python3
# Patch 059 (zusammengefuehrt): Empfohlene Einstiegsdosis flexibler gestaltet.
# 1) Statt einem fixen Einzelwert (~2.5 mg, kaum spuerbar) wird jetzt eine
#    Range gezeigt.
# 2) Die Range passt sich der angegebenen Konsumfrequenz an:
#    - Gelegentlich / Regelmaessig (tolFactor 1.0 / 1.3): ~2.5-5 mg
#    - Taeglich / Taeglich mehrmals (tolFactor 1.7 / 2.2): ~5-10 mg
#    (Toleranzbedingt braucht es fuer einen spuerbaren Effekt praktisch
#    ohnehin mehr -- das bildet sich jetzt schon in der Einstiegsempfehlung
#    ab, nicht erst im separaten Toleranz-Warnhinweis darunter.)
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """  var kgBox = document.getElementById('r-kg-box');
  var kgEl = document.getElementById('r-kg');
  // Einstiegsdosis (MacCallum & Russo 2018): absolut, immer sichtbar als Grundempfehlung.
  if(kgBox && kgEl) {
    kgBox.style.display = 'block';
    kgEl.innerHTML = '~2.5 mg<div style="display:block;font-size:11px;font-weight:400;color:var(--text3);line-height:1.5;margin-top:4px">Delta-9-THC aufgenommen · oral wirksam als 11-OH · bis ~5 mg langsam steigern<br>empfindliche Personen (tendenziell weiblichen Geschlechts) tiefer ansetzen</div>';
  }"""

new1 = """  var kgBox = document.getElementById('r-kg-box');
  var kgEl = document.getElementById('r-kg');
  // Einstiegsdosis (MacCallum & Russo 2018 als Basis): als Range, passt sich der Konsumfrequenz an.
  if(kgBox && kgEl) {
    kgBox.style.display = 'block';
    var kgRange = tolFactor>=1.7 ? '~5–10 mg' : '~2.5–5 mg';
    var kgFreqNote = tolFactor>=1.7 ? ' Bei täglichem Konsum braucht es für einen spürbaren Effekt erfahrungsgemäss mehr — daher die höhere Spanne.' : '';
    kgEl.innerHTML = kgRange+'<div style="display:block;font-size:11px;font-weight:400;color:var(--text3);line-height:1.5;margin-top:4px">Delta-9-THC aufgenommen · oral wirksam als 11-OH · innerhalb dieser Spanne langsam steigern, nicht sofort das obere Ende nehmen.'+kgFreqNote+'<br>empfindliche Personen (tendenziell weiblichen Geschlechts) eher am unteren Ende ansetzen</div>';
  }"""

if old1 not in content:
    print("WARNUNG 1: Startdosis-Block nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Einstiegsdosis zeigt jetzt Range (2.5–5mg bzw. 5–10mg bei täglichem Konsum) statt fixem Einzelwert.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
