#!/usr/bin/env python3
# Patch 051 (final, ersetzt fruehere Version): Ergebnisanzeige des Rechners
# neu geordnet + Toleranz-Text praezisiert. Zwei Themen in einem Patch:
#
# 1) Reihenfolge: Die eigentliche Antwort ("Empf. Einstiegsdosis") stand
#    bisher NACH den Warnkaesten (11-OH-THC, Toleranz) -- das versteckt die
#    wichtigste, handlungsrelevante Zahl. Neue Reihenfolge:
#      Einstiegsdosis + Intensitaet (ganz oben, die Antwort)
#      -> Gesamt / Pro Portion / Bioverfuegbar (der Rechenweg dahinter)
#      -> Empfehlung (Text)
#      -> "Wichtige Hinweise"-Trenner + beide Warnkaesten gebuendelt (zum
#         Schluss lesen, bevor man konsumiert)
#
# 2) Toleranz-Hinweis: "~X mg" war mehrdeutig (koennte als 11-OH-THC
#    missverstanden werden, was lebensgefaehrlich falsch waere). Jetzt
#    explizit "~X mg Delta-9-THC (oral)".
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 2

# ─────────────────────────────────────────────────────────────────────────
# 1) Ergebnis-Grid komplett neu geordnet
# ─────────────────────────────────────────────────────────────────────────
old1 = """  <div class="rg" id="result-grid">
    <div class="rm"><div class="rl">Delta-9-THC gesamt in Charge</div><div class="rv hi" id="r-total">—</div></div>
    <div class="rm"><div class="rl">Delta-9-THC pro Portion</div><div class="rv hi" id="r-portion">—</div></div>
    <div class="rm" id="r-bio-box" style="display:none"><div class="rl" id="r-bio-label">Bioverfügbar (Ø)</div><div class="rv am" id="r-bio">—</div></div>
    <div id="r-11oh-warn" style="display:none;grid-column:1/-1;background:#1f0a0a;border:1px solid #c0392b;border-radius:var(--radius);padding:10px 12px;font-size:var(--fs-sm);color:#e07070;line-height:1.7">
      ⚠️ <b>Achtung: 11-Hydroxy-THC</b><br>
      Diese bioverfügbare Menge entsteht oral in der Leber als <b>11-Hydroxy-THC</b> — nicht als Delta-9-THC wie beim Inhalieren. 11-OH-THC wirkt <b>4–5× stärker</b> und bis zu <b>8 Stunden</b>.<br>
      Bereits <b>1–2mg 11-OH-THC</b> gelten als spürbare Startdosis. Die angezeigte bioverfügbare Menge ist <b>kein Freifahrtschein</b> für höhere Dosierung — im Gegenteil.<br>
      <b>Immer mit der kleinstmöglichen Portion starten und mindestens 2h warten.</b><br>
      <span onclick="gotoLexCat('cannabinoide')" style="display:inline-block;margin-top:8px;cursor:pointer;font-size:var(--fs-xs);color:#e07070;border:1px solid #c0392b;border-radius:20px;padding:3px 10px">📖 Mehr im Lexikon: 11-OH-THC →</span>
    </div>
    <div id="r-tol-box" style="display:none;grid-column:1/-1;background:var(--warn-bg);border:1px solid var(--warn);border-radius:var(--radius);padding:10px 12px;font-size:var(--fs-sm);color:var(--warn);line-height:1.65">⚠️ <b>Hinweis bei angegebener Toleranz</b> (<span id="r-tol-lvl">—</span>)<br><span id="r-tol-text">—</span><br><span onclick="gotoLexCat('risiken')" style="display:inline-block;margin-top:6px;cursor:pointer;font-size:var(--fs-xs);color:var(--warn);border:1px solid var(--warn);border-radius:20px;padding:3px 10px">📖 Mehr: Toleranz →</span></div>
    <div class="rm pulse-green" id="r-kg-box" style="display:none"><div class="rl">Empf. Einstiegsdosis (Delta-9, oral)</div><div class="rv hi" id="r-kg">—</div></div>
    <div class="rm"><div class="rl">Intensität</div><div class="rv" id="r-int">—</div></div>
    <div class="rm"><div class="rl">Empfehlung</div><div class="rv sm" id="r-rec" style="color:var(--text3)">—</div></div>
  </div>"""

new1 = """  <div class="rg" id="result-grid">
    <div class="rm pulse-green" id="r-kg-box" style="display:none"><div class="rl">Empf. Einstiegsdosis (Delta-9, oral)</div><div class="rv hi" id="r-kg">—</div></div>
    <div class="rm"><div class="rl">Intensität</div><div class="rv" id="r-int">—</div></div>
    <div class="rm"><div class="rl">Delta-9-THC gesamt in Charge</div><div class="rv hi" id="r-total">—</div></div>
    <div class="rm"><div class="rl">Delta-9-THC pro Portion</div><div class="rv hi" id="r-portion">—</div></div>
    <div class="rm" id="r-bio-box" style="display:none"><div class="rl" id="r-bio-label">Bioverfügbar (Ø)</div><div class="rv am" id="r-bio">—</div></div>
    <div class="rm"><div class="rl">Empfehlung</div><div class="rv sm" id="r-rec" style="color:var(--text3)">—</div></div>
    <div id="r-hints-label" style="display:none;grid-column:1/-1;font-size:var(--fs-xs);color:var(--text3);text-transform:uppercase;letter-spacing:.05em;font-weight:700;margin-top:4px">⚠️ Wichtige Hinweise — bitte vor dem Konsum lesen</div>
    <div id="r-11oh-warn" style="display:none;grid-column:1/-1;background:#1f0a0a;border:1px solid #c0392b;border-radius:var(--radius);padding:10px 12px;font-size:var(--fs-sm);color:#e07070;line-height:1.7">
      ⚠️ <b>Achtung: 11-Hydroxy-THC</b><br>
      Diese bioverfügbare Menge entsteht oral in der Leber als <b>11-Hydroxy-THC</b> — nicht als Delta-9-THC wie beim Inhalieren. 11-OH-THC wirkt <b>4–5× stärker</b> und bis zu <b>8 Stunden</b>.<br>
      Bereits <b>1–2mg 11-OH-THC</b> gelten als spürbare Startdosis. Die angezeigte bioverfügbare Menge ist <b>kein Freifahrtschein</b> für höhere Dosierung — im Gegenteil.<br>
      <b>Immer mit der kleinstmöglichen Portion starten und mindestens 2h warten.</b><br>
      <span onclick="gotoLexCat('cannabinoide')" style="display:inline-block;margin-top:8px;cursor:pointer;font-size:var(--fs-xs);color:#e07070;border:1px solid #c0392b;border-radius:20px;padding:3px 10px">📖 Mehr im Lexikon: 11-OH-THC →</span>
    </div>
    <div id="r-tol-box" style="display:none;grid-column:1/-1;background:var(--warn-bg);border:1px solid var(--warn);border-radius:var(--radius);padding:10px 12px;font-size:var(--fs-sm);color:var(--warn);line-height:1.65">⚠️ <b>Hinweis bei angegebener Toleranz</b> (<span id="r-tol-lvl">—</span>)<br><span id="r-tol-text">—</span><br><span onclick="gotoLexCat('risiken')" style="display:inline-block;margin-top:6px;cursor:pointer;font-size:var(--fs-xs);color:var(--warn);border:1px solid var(--warn);border-radius:20px;padding:3px 10px">📖 Mehr: Toleranz →</span></div>
  </div>"""

if old1 not in content:
    print("WARNUNG 1: Ergebnis-Grid nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Ergebnis-Grid neu geordnet — Einstiegsdosis zuerst, Warnungen gebündelt am Ende.")

# ─────────────────────────────────────────────────────────────────────────
# 2) calcUpdate(): r-hints-label sichtbar machen, wenn mind. eine Warnbox
#    angezeigt wird
# ─────────────────────────────────────────────────────────────────────────
old2 = """  var tolTextEl=document.getElementById('r-tol-text');
  var tolLvlEl=document.getElementById('r-tol-lvl');
  if(tolFactor>1.0 && tolTextEl) {
    var _tolSel=document.getElementById('tolerance');
    if(tolLvlEl) tolLvlEl.textContent=_tolSel.options[_tolSel.selectedIndex].text;
    tolTextEl.innerHTML='Bei bestehender Toleranz kann für einen spürbaren Wirkungseintritt mehr nötig sein — erfahrungsgemäss bis <span style="background:var(--amber);color:#1a1200;font-weight:800;font-size:1.15em;padding:1px 8px;border-radius:6px;white-space:nowrap">~'+ppTol+' mg</span>. <b>Das ist keine Empfehlung.</b> Höhere Dosen steigern Risiko und Toleranz weiter; eine Konsumpause (T-Break) senkt den Bedarf wieder.';
  }"""

new2 = """  var tolTextEl=document.getElementById('r-tol-text');
  var tolLvlEl=document.getElementById('r-tol-lvl');
  if(tolFactor>1.0 && tolTextEl) {
    var _tolSel=document.getElementById('tolerance');
    if(tolLvlEl) tolLvlEl.textContent=_tolSel.options[_tolSel.selectedIndex].text;
    tolTextEl.innerHTML='Bei bestehender Toleranz kann für einen spürbaren Wirkungseintritt mehr nötig sein — erfahrungsgemäss bis <span style="background:var(--amber);color:#1a1200;font-weight:800;font-size:1.15em;padding:1px 8px;border-radius:6px;white-space:nowrap">~'+ppTol+' mg Delta-9-THC (oral)</span>. <b>Das ist keine Empfehlung.</b> Höhere Dosen steigern Risiko und Toleranz weiter; eine Konsumpause (T-Break) senkt den Bedarf wieder.';
  }
  var hintsLabel = document.getElementById('r-hints-label');
  if(hintsLabel) {
    var oh = document.getElementById('r-11oh-warn'), tb = document.getElementById('r-tol-box');
    var ohVisible = oh && oh.style.display !== 'none';
    var tbVisible = tolFactor>1.0;
    hintsLabel.style.display = (ohVisible || tbVisible) ? 'block' : 'none';
  }"""

if old2 not in content:
    print("WARNUNG 2: Toleranz-Text-Block in calcUpdate() nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Toleranz-Text präzisiert (Delta-9-THC) + 'Wichtige Hinweise'-Label wird bei Bedarf eingeblendet.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
