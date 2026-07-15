#!/usr/bin/env python3
# Patch H: Wechselwirkungen & Medikamente (neue Lexikon-Kategorie),
#          Deep-Links von Startseiten-Kacheln auf einzelne Einträge (gotoEntry),
#          Startseite: "16 Guides" + "Fortgeschritten"-Kachel aus Box 1 entfernt,
#          Meistgelesen: Fake-Zahl durch Quelle-Platzhalter ersetzt.
#
# Idempotent: prüft vor jeder Änderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 6

# ─────────────────────────────────────────────────────────────────────────
# 1) Neue LIB-Kategorie "wechselwirkungen" nach "medizin" einfügen
# ─────────────────────────────────────────────────────────────────────────
old1 = """Gehalt, Qualität und Reinheit sind GMP-zertifiziert — im Gegensatz zu Schwarzmarkt-Ware.'}
  ]},
  risiken:{cat:'Physiologie & Risiken',items:["""

new1 = """Gehalt, Qualität und Reinheit sind GMP-zertifiziert — im Gegensatz zu Schwarzmarkt-Ware.'}
  ]},
  wechselwirkungen:{cat:'Wechselwirkungen & Medikamente',items:[
    {t:'Benzodiazepine (z.B. Diazepam, Lorazepam)',b:'<span class="lex-term">Benzodiazepine</span><span class="lex-tag med">Medikament</span><span class="lex-tag adv">Wechselwirkung</span><br>[ROHENTWURF – bitte prüfen] Benzodiazepine (u.a. gegen Angst, Schlafstörungen, Krampfanfälle) wirken wie Cannabis dämpfend auf das zentrale Nervensystem. In Kombination verstärken sich Sedierung, Schwindel und Koordinationsverlust überproportional — nicht additiv, sondern potenzierend. Zusätzliches Risiko bei gleichzeitigem Alkoholkonsum. Wer Benzodiazepine verschrieben bekommt, sollte Cannabiskonsum mit der verschreibenden Stelle besprechen.'},
    {t:'Opioide (z.B. Oxycodon, Morphin, Tramadol)',b:'<span class="lex-term">Opioide</span><span class="lex-tag med">Medikament</span><span class="lex-tag adv">Wechselwirkung</span><br>[ROHENTWURF – bitte prüfen] Beide Substanzen wirken atemdepressiv und sedierend — in Kombination steigt das Risiko einer gefährlichen Atemdepression. Manche Studien diskutieren einen opioidsparenden Effekt von Cannabis bei chronischen Schmerzpatient:innen, die Datenlage dazu ist jedoch uneinheitlich und kein Freibrief für Selbstmedikation. Rücksprache mit Ärzt:in/Apotheke bei bestehender Opioidtherapie dringend empfohlen.'},
    {t:'Alkohol',b:'<span class="lex-term">Alkohol</span><span class="lex-tag adv">Wechselwirkung</span><br>[ROHENTWURF – bitte prüfen] Alkohol und Cannabis verstärken sich gegenseitig nicht additiv, sondern potenzierend — der kombinierte Effekt ist schwer vorhersagbar und ein häufiger Auslöser für Übelkeit, Kreislaufprobleme und unangenehme Erfahrungen ("Greening Out"). Die Reihenfolge spielt eine Rolle: Cannabis nach Alkohol erhöht THC-Aufnahme und -Wirkung stärker, als umgekehrt. Kombination erhöht zudem das Unfallrisiko im Strassenverkehr deutlich über die Einzelwirkungen hinaus.'},
    {t:'Blutverdünner (Vitamin-K-Antagonisten, z.B. Marcoumar/Warfarin)',b:'<span class="lex-term">Vitamin-K-Antagonisten</span><span class="lex-tag med">Medikament</span><span class="lex-tag adv">Wechselwirkung</span><br>[ROHENTWURF – bitte prüfen] Cannabinoide hemmen das Leberenzym CYP2C9, das auch am Abbau von Vitamin-K-Antagonisten (Marcoumar/Sintrom, Warfarin) beteiligt ist. Dadurch kann der Medikamentenspiegel steigen und die Blutungsneigung zunehmen (INR-Erhöhung). Menschen unter Blutverdünnung sollten regelmässige Cannabisnutzung mit der verschreibenden Stelle besprechen, insbesondere bei Dosisänderungen.'},
    {t:'SSRI/SNRI-Antidepressiva',b:'<span class="lex-term">SSRI/SNRI</span><span class="lex-tag med">Medikament</span><span class="lex-tag adv">Wechselwirkung</span><br>[ROHENTWURF – bitte prüfen] CBD hemmt u.a. CYP2C19 und CYP3A4, worüber viele Antidepressiva verstoffwechselt werden — der Wirkspiegel kann dadurch ansteigen. THC selbst kann bei manchen Personen Angst oder Stimmungsschwankungen verstärken, was sich mit einer bestehenden depressiven oder Angst-Symptomatik überschneiden kann. Keine pauschale Kontraindikation, aber ein Punkt für das Gespräch mit Ärzt:in oder Psychiater:in.'},
    {t:'Betablocker & Blutdrucksenker',b:'<span class="lex-term">Betablocker</span><span class="lex-tag med">Medikament</span><span class="lex-tag adv">Wechselwirkung</span><br>[ROHENTWURF – bitte prüfen] THC kann in niedrigen Dosen die Herzfrequenz erhöhen (Tachykardie), bei höheren Dosen dagegen Blutdruckabfall und orthostatische Hypotonie (Schwindel beim Aufstehen) begünstigen. In Kombination mit Blutdrucksenkern oder Betablockern kann dieser Effekt verstärkt oder maskiert werden. Besonders relevant für Personen mit bekannten Herz-Kreislauf-Vorerkrankungen.'},
    {t:'Stimulanzien & ADHS-Medikamente (Methylphenidat, Amphetamine, Kokain, MDMA)',b:'<span class="lex-term">Stimulanzien</span><span class="lex-tag adv">Wechselwirkung</span><br>[ROHENTWURF – bitte prüfen] Stimulanzien erhöhen Herzfrequenz und Blutdruck; Cannabis kann diesen Effekt zusätzlich verstärken, vor allem in Kombination mit Kokain oder MDMA (kardiovaskuläre Belastung, Herzrhythmusstörungen). Bei verschriebenen ADHS-Medikamenten (Methylphenidat u.ä.) sollte gleichzeitiger Cannabiskonsum mit der behandelnden Stelle besprochen werden, insbesondere wegen möglicher Wechselwirkungen auf Konzentration und Herz-Kreislauf-System.'},
    {t:'Immunsuppressiva & Statine (CYP3A4-Substrate)',b:'<span class="lex-term">CYP3A4-Substrate</span><span class="lex-tag med">Medikament</span><span class="lex-tag adv">Wechselwirkung</span><br>[ROHENTWURF – bitte prüfen] Viele Immunsuppressiva (z.B. nach Organtransplantation) und Statine (Cholesterinsenker) werden über CYP3A4 abgebaut, ein Enzym, das Cannabinoide teilweise hemmen. Das kann zu höheren Wirkstoffspiegeln und verstärkten Nebenwirkungen führen. Diese Liste ist nicht vollständig — bei jeder Dauermedikation lohnt sich die gezielte Nachfrage nach CYP450-Interaktionen bei Arzt oder Apotheke.'}
  ]},
  risiken:{cat:'Physiologie & Risiken',items:["""

if old1 not in content:
    print("WARNUNG 1: Einfügepunkt für 'wechselwirkungen'-Kategorie nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Neue Kategorie 'Wechselwirkungen & Medikamente' (8 Einträge) eingefügt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) gotoEntry-Helper: springt direkt zu einem Eintrag (Library ODER Safety)
# ─────────────────────────────────────────────────────────────────────────
old2 = """window.gotoLexCat = function(c){ activeLibCat = c; showPage('library'); };"""
new2 = """window.gotoLexCat = function(c){ activeLibCat = c; showPage('library'); };
window.gotoEntry = function(page, cat, idx){
  if(page==='library'){ activeLibCat = cat; } else if(page==='safety'){ activeSafetyCat = cat; }
  showPage(page);
  var prefix = page==='library' ? 'l' : 's';
  setTimeout(function(){ jumpToEntry(prefix+cat+idx); }, 60);
};"""

if old2 not in content:
    print("WARNUNG 2: gotoLexCat-Definition nicht gefunden — gotoEntry nicht eingefügt.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: gotoEntry()-Helper für Deep-Links auf einzelne Einträge eingefügt.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Wirkstoffe-Kacheln (THC/CBD/CBN/CBG) auf konkrete Einträge verlinken
# ─────────────────────────────────────────────────────────────────────────
ref_replacements = [
    ("""<div class="ref-card" onclick="gotoLexCat('cannabinoide')"><div class="k">THC</div>""",
     """<div class="ref-card" onclick="gotoEntry('library','cannabinoide',0)"><div class="k">THC</div>"""),
    ("""<div class="ref-card" onclick="gotoLexCat('cannabinoide')"><div class="k">CBD</div>""",
     """<div class="ref-card" onclick="gotoEntry('library','cannabinoide',1)"><div class="k">CBD</div>"""),
    ("""<div class="ref-card" onclick="gotoLexCat('cannabinoide')"><div class="k">CBN</div>""",
     """<div class="ref-card" onclick="gotoEntry('library','cannabinoide',5)"><div class="k">CBN</div>"""),
    ("""<div class="ref-card" onclick="gotoLexCat('cannabinoide')"><div class="k">CBG</div>""",
     """<div class="ref-card" onclick="gotoEntry('library','cannabinoide',6)"><div class="k">CBG</div>"""),
]
ref_ok = 0
for old, new in ref_replacements:
    if old in content:
        content = content.replace(old, new)
        ref_ok += 1
if ref_ok == len(ref_replacements):
    changes += 1
    print(f"3/{total}: Wirkstoffe-Kacheln (THC/CBD/CBN/CBG) auf einzelne Einträge verlinkt.")
else:
    print(f"WARNUNG 3: Nur {ref_ok}/{len(ref_replacements)} Wirkstoffe-Kacheln gefunden.")

# ─────────────────────────────────────────────────────────────────────────
# 4) Themen-Chips (Wirkdauer, THC vs. CBD, Decarboxylierung) verlinken
# ─────────────────────────────────────────────────────────────────────────
chip_replacements = [
    ("""<span class="kchip" onclick="showPage('safety')"><b>↗</b> Wirkdauer</span>""",
     """<span class="kchip" onclick="gotoEntry('library','cannabinoide',4)"><b>↗</b> Wirkdauer</span>"""),
    ("""<span class="kchip" onclick="gotoLexCat('cannabinoide')"><b>↗</b> THC vs. CBD</span>""",
     """<span class="kchip" onclick="gotoEntry('library','cannabinoide',0)"><b>↗</b> THC vs. CBD</span>"""),
    ("""<span class="kchip" onclick="gotoLexCat('dekarb')"><b>↗</b> Decarboxylierung</span>""",
     """<span class="kchip" onclick="gotoEntry('library','dekarb',0)"><b>↗</b> Decarboxylierung</span>"""),
]
chip_ok = 0
for old, new in chip_replacements:
    if old in content:
        content = content.replace(old, new)
        chip_ok += 1
if chip_ok == len(chip_replacements):
    changes += 1
    print(f"4/{total}: Themen-Chips (Wirkdauer, THC vs. CBD, Decarboxylierung) verlinkt.")
else:
    print(f"WARNUNG 4: Nur {chip_ok}/{len(chip_replacements)} Chips gefunden.")

# ─────────────────────────────────────────────────────────────────────────
# 5) Meistgelesen: auf konkrete Einträge verlinken + Fake-Zahl durch Quelle-Platzhalter ersetzen
# ─────────────────────────────────────────────────────────────────────────
old5 = """      <div class="read" onclick="showPage('safety')"><span class="rank">01</span><div><div class="t">Wie lange wirken Edibles?</div><div class="m">Sicherheit · 4 Min.</div></div><span class="v">12.4k</span></div>
      <div class="read" onclick="gotoLexCat('cannabinoide')"><span class="rank">02</span><div><div class="t">THC und CBD im Vergleich</div><div class="m">Wirkstoffe · 6 Min.</div></div><span class="v">9.8k</span></div>
      <div class="read" onclick="gotoLexCat('dekarb')"><span class="rank">03</span><div><div class="t">Was ist Decarboxylierung?</div><div class="m">Konsumformen · 5 Min.</div></div><span class="v">7.1k</span></div>
      <div class="read" onclick="showPage('safety')"><span class="rank">04</span><div><div class="t">Cannabis-Pilotprojekte Schweiz</div><div class="m">Recht · 7 Min.</div></div><span class="v">6.3k</span></div>"""

new5 = """      <div class="read" onclick="gotoEntry('library','cannabinoide',4)"><span class="rank">01</span><div><div class="t">Wie lange wirken Edibles?</div><div class="m">Sicherheit · 4 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Quelle: [ROHENTWURF]</span></div>
      <div class="read" onclick="gotoEntry('library','cannabinoide',0)"><span class="rank">02</span><div><div class="t">THC und CBD im Vergleich</div><div class="m">Wirkstoffe · 6 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Quelle: [ROHENTWURF]</span></div>
      <div class="read" onclick="gotoEntry('library','dekarb',0)"><span class="rank">03</span><div><div class="t">Was ist Decarboxylierung?</div><div class="m">Konsumformen · 5 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Quelle: [ROHENTWURF]</span></div>
      <div class="read" onclick="gotoEntry('safety','recht',0)"><span class="rank">04</span><div><div class="t">Cannabis-Pilotprojekte Schweiz</div><div class="m">Recht · 7 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Quelle: [ROHENTWURF]</span></div>"""

if old5 not in content:
    print("WARNUNG 5: Meistgelesen-Block nicht gefunden.")
else:
    content = content.replace(old5, new5)
    changes += 1
    print(f"5/{total}: Meistgelesen auf Einträge verlinkt, Fake-Zahlen durch Quelle-Platzhalter ersetzt.")
    print("       (Die 4 Themen selbst kannst du austauschen, sobald die NotebookLM-Texte stehen.)")

# ─────────────────────────────────────────────────────────────────────────
# 6) Startseite Box 1: "16 Guides" und "Fortgeschritten"-Kachel entfernen
# ─────────────────────────────────────────────────────────────────────────
old6 = """      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">☑ <b>16 Guides</b><br><span style="color:var(--text3)">mit Timern & Notizen</span></div>
      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">∑ <b>Dosierungsrechner</b><br><span style="color:var(--text3)">Blüten & Extrakte</span></div>
      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">⊡ <b>Chargenverwaltung</b><br><span style="color:var(--text3)">mit Diagrammen & PDF</span></div>
      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">⛨ <b>Prävention</b><br><span style="color:var(--text3)">DACH Anlaufstellen</span></div>
      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">📖 <b>Lexikon</b><br><span style="color:var(--text3)">Szene- & Fachbegriffe</span></div>
      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">⚗ <b>Fortgeschritten</b><br><span style="color:var(--text3)">BHO, THCA, Destillat</span></div>"""

new6 = """      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">∑ <b>Dosierungsrechner</b><br><span style="color:var(--text3)">Blüten & Extrakte</span></div>
      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">⊡ <b>Chargenverwaltung</b><br><span style="color:var(--text3)">mit Diagrammen & PDF</span></div>
      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">⛨ <b>Prävention</b><br><span style="color:var(--text3)">DACH Anlaufstellen</span></div>
      <div style="background:var(--bg3);border-radius:var(--radius);padding:8px 12px;font-size:var(--fs-sm)">📖 <b>Lexikon</b><br><span style="color:var(--text3)">Szene- & Fachbegriffe</span></div>"""

if old6 not in content:
    print("WARNUNG 6: Kachel-Grid in Startseiten-Box nicht gefunden.")
else:
    content = content.replace(old6, new6)
    changes += 1
    print(f"6/{total}: 'Guides'- und 'Fortgeschritten'-Kachel aus Box 1 entfernt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen (evtl. Zwischenstand seit letztem Fetch geändert)!")
