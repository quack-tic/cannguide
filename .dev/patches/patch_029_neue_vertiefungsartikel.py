#!/usr/bin/env python3
# Patch Q: 4 neue Vertiefungsartikel eingefuegt (Wirkdauer, Mikrodosierung,
# THC vs. CBD, Decarboxylierung). Die 4 Themen-Chips auf der Startseite
# fuehren jetzt zu diesen Artikeln statt zu Bibliothekskategorien/Rechner.
# Der Mikrodosierungs-Artikel enthaelt einen kontrastreich hervorgehobenen
# Link zurueck zum Dosierungsrechner.
#
# Enthaelt zusaetzlich 2 Konsistenzfixes: die Wirkdauer-Zahl war an 3 Stellen
# unterschiedlich (4-8h / 6-10h / 8-12h) -- vereinheitlicht auf 4-8h als
# Kernbereich mit explizit gekennzeichneter Ausnahme. Der Onset-Unterschied
# (30-120min vs. 60-120min) wird stattdessen begruendet (Erstwirkung vs. Peak),
# da beide Werte pharmakologisch unterschiedliche Zeitpunkte beschreiben.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 7

# ─────────────────────────────────────────────────────────────────────────
# 1) 4 neue Artikel an die "artikel"-Kategorie anhaengen (Index 4-7)
# ─────────────────────────────────────────────────────────────────────────
old1 = """<span style="font-size:11px;color:var(--text3)">Quellen: Dyck et al. (2022); Hermann & Schneider (2012); Hoch, Friemel & Schneider (Hrsg., 2019/2022); Russo (2011), British Journal of Pharmacology</span>'}
  ]},
  risiken:{cat:'Physiologie & Risiken',items:["""

new1 = """<span style="font-size:11px;color:var(--text3)">Quellen: Dyck et al. (2022); Hermann & Schneider (2012); Hoch, Friemel & Schneider (Hrsg., 2019/2022); Russo (2011), British Journal of Pharmacology</span>'},
    {t:'Die Wirkdauer von Edibles — warum der Rausch aus dem Magen einen ganzen Tag anhalten kann',b:'[ROHENTWURF – bitte prüfen] Während der Rausch beim Inhalieren meist nach 2–3 Stunden abflacht, hält die Wirkung von oral aufgenommenem Cannabis in der Regel <b>4–8 Stunden</b> an — bei hohen Dosen oder besonders empfindlichen Personen auch deutlich länger, in Einzelfällen bis in den nächsten Tag. Drei pharmakokinetische Prozesse sind dafür verantwortlich.<br><br><b>Die langsame, verzögerte Resorption</b><br>Der Magen-Darm-Trakt ist eine Barriere: Cannabinoide sind stark lipophil und kaum wasserlöslich. Je nach Magenfüllung und Fettanteil der Mahlzeit gibt der Körper das THC nur in kleinen, kontinuierlichen Schüben über Stunden hinweg ins Blut ab — das erklärt auch, warum der Onset (erste spürbare Wirkung) meist schon ab 30 Minuten beginnt, die maximale Blutkonzentration (Peak) aber oft erst nach 60–120 Minuten erreicht ist. Beides sind unterschiedliche Zeitpunkte im selben Prozess, keine widersprüchlichen Angaben.<br><br><b>Das langlebige 11-OH-THC</b><br>Die Leber wandelt einen Grossteil des THC über den First-Pass-Effekt in 11-Hydroxy-THC um — potenter, überwindet die Blut-Hirn-Schranke leichter und wird deutlich langsamer abgebaut als pflanzliches THC.<br><br><b>Enterohepatischer Kreislauf & Fettspeicher</b><br>Die Leber scheidet einen Teil der Metaboliten über die Galle wieder in den Darm aus, von wo sie teils erneut resorbiert werden — das kann zu unerwarteten "Wellen" im Rauscherleben führen. Zusätzlich lagert sich lipophiles THC in Fettzellen an und wird nur tröpfchenweise wieder freigesetzt — ein Grund, warum die Wirkung bei hohen Dosen die üblichen 4–8 Stunden überschreiten kann.<br><br><b>Fazit</b><br>Ein Edible ist kein Sprint, sondern ein pharmakologischer Marathon — langsame Verdauung, langlebige Leber-Metaboliten und Rückresorption aus dem Darm bestimmen zusammen den gesamten Tagesablauf.<br><br><span style="font-size:11px;color:var(--text3)">Quellen: Grotenhermen (2012); Freissmuth et al. (2020); Zernikow (Hrsg., 2022)</span>'},
    {t:'Mikrodosierung von Edibles — die Kunst der unsichtbaren Wirkung',b:'[ROHENTWURF – bitte prüfen] Mikrodosierung kennt man vor allem von Psychedelika, etabliert sich aber auch bei Cannabis-Edibles. Ziel: den Endocannabinoid-Tonus sanft stimulieren, ohne jede berauschende Wirkung.<br><br><b>Was ist eine Cannabis-Mikrodosis?</b><br>Während ein üblicher "Space Cake" 15–50 mg THC enthält, bewegt sich eine Mikrodosis bei 1,0–2,5 mg THC (oft kombiniert mit gleicher oder höherer Menge CBD). Das 11-OH-THC entsteht zwar auch hier, erreicht im Gehirn aber nicht die Schwelle für eine Bewusstseinsveränderung. Berichtet werden subtile Angstlösung, besserer Fokus und leichte Schmerzlinderung — und entscheidend: keine CB1-Downregulation, also keine Toleranzbildung.<br><br><b>Das Homogenitäts-Problem</b><br>Cannabinoide sind fettlöslich und verklumpen in Teigen oder Flüssigkeiten. Wer Cannabutter einfach in Teig rührt, riskiert, dass ein Keks 0 mg und der nächste 10 mg THC enthält — für Mikrodosierung völlig ungeeignet.<br><br><b>Die Lösung: Lecithin-Extraktion und Emulsionen</b><br>Emulgatoren wie Lecithin verbinden das fettliebende Extrakt untrennbar mit wasserhaltigen Zutaten und sorgen für eine stabile, homogene Verteilung — nur so enthält jedes Gummibärchen wirklich dieselbe Dosis.<br><br><b>Fazit</b><br>Cannabis-Microdosing ist ein präzises Werkzeug für den fokussierten Alltag — aber nur mit sauberer Berechnung und Emulgatoren zuverlässig umsetzbar. Zum genauen Berechnen deiner eigenen Mikrodosis:<br><span onclick="showPage(\\'calc\\')" style="display:inline-block;margin-top:8px;cursor:pointer;font-weight:700;font-size:var(--fs);color:#08130d;background:var(--accent);border-radius:20px;padding:6px 16px">∑ Zum Dosierungsrechner →</span><br><br><span style="font-size:11px;color:var(--text3)">Quellen: Knodt (2020); Grotenhermen (2012); Hoch, Friemel & Schneider (Hrsg., 2019/2022)</span>'},
    {t:'THC vs. CBD — das biochemische Yin und Yang der Cannabispflanze',b:'[ROHENTWURF – bitte prüfen] THC und CBD besitzen die exakt gleiche chemische Summenformel (C21H30O2), unterscheiden sich aber in ihrer dreidimensionalen Struktur — dieser kleine bauliche Unterschied entscheidet, ob man high wird oder nicht.<br><br><b>THC: Der direkte Schlüssel zum Rausch</b><br>THC passt wie ein Schlüssel in die CB1-Rezeptoren im zentralen Nervensystem. Als partieller Agonist löst es dort eine Kaskade aus, verändert die Neurotransmitter-Ausschüttung und stimuliert das Belohnungssystem — Folgen: Euphorie, veränderte Zeitwahrnehmung, Heisshunger, aber auch mögliche Paranoia oder Herzrasen.<br><br><b>CBD: Der besänftigende Modulator</b><br>CBD hat kaum direkte Bindungsaffinität zum CB1-Rezeptor und wirkt daher nicht berauschend. Es agiert dort als negativer allosterischer Modulator — bindet an anderer Stelle, verändert die Rezeptorform leicht und bremst so THC biochemisch aus, wenn beide gleichzeitig andocken. Zusätzlich wirkt CBD über Serotonin-Rezeptoren (5-HT1A, angstlösend) und TRPV1-Kanäle (Schmerz, Entzündung).<br><br><b>Fazit</b><br>THC stimuliert das Gehirn direkt und sorgt für Rausch sowie Schmerzlinderung, während CBD als subtiler Systemregulator im Hintergrund Entzündungen hemmt, Ängste löst und das Endocannabinoidsystem in Balance hält.<br><br><span style="font-size:11px;color:var(--text3)">Quellen: Hermann & Schneider (2012); Hoch, Friemel & Schneider (Hrsg., 2019/2022)</span>'},
    {t:'Decarboxylierung — warum rohes Cannabis nicht high macht',b:'[ROHENTWURF – bitte prüfen] Ein häufiger Anfängerfehler: rohe Blüten direkt in Teig oder Alkohol geben. Die erhoffte Wirkung bleibt aus — der Grund ist die Decarboxylierung.<br><br><b>Das THCA-Problem</b><br>Die frische Pflanze produziert kein psychoaktives THC, sondern THCA (Tetrahydrocannabinolsäure). Die zusätzliche Carboxylgruppe (COOH) macht das Molekül zu gross und klobig, um die Blut-Hirn-Schranke effektiv zu passieren oder an CB1-Rezeptoren anzudocken — rohes Cannabis ist praktisch frei von Rauschwirkung.<br><br><b>Hitze als chemischer Aktivator</b><br>Um aus THCA aktives THC zu machen, muss die Carboxylgruppe als CO2 abgespalten werden — das passiert durch Zeit und vor allem Hitze. Beim Rauchen/Vapen geschieht das durch die Flamme/Glut in Sekundenbruchteilen; beim Backen/Kochen/Extrahieren muss aktiv erhitzt werden. Faustregel: ca. 110–120°C für 30–45 Minuten im Backofen (genauer Zielwert je nach Material — THC-Kristalle etwas höher). Über 150°C wird THC zerstört oder zu CBN umgewandelt.<br><br><b>Fazit</b><br>Ohne Hitze keine Wirkung — Decarboxylierung ist der Schlüsselschritt, um das Potenzial der Pflanze für Tinkturen, Tropfen und Edibles überhaupt erst freizusetzen.<br><br><span style="font-size:11px;color:var(--text3)">Quellen: Gebhardt (2012); Knodt (2020)</span>'}
  ]},
  risiken:{cat:'Physiologie & Risiken',items:["""

if old1 not in content:
    print("WARNUNG 1: Einfügepunkt für neue Artikel nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: 4 neue Vertiefungsartikel eingefügt (Wirkdauer=4, Mikrodosierung=5, THC vs. CBD=6, Decarboxylierung=7).")

# ─────────────────────────────────────────────────────────────────────────
# 2) Chip "Wirkdauer"
# ─────────────────────────────────────────────────────────────────────────
old2 = """<span class="kchip" onclick="gotoEntry('library','cannabinoide',4)"><b>↗</b> Wirkdauer</span>"""
new2 = """<span class="kchip" onclick="gotoEntry('library','artikel',4)"><b>↗</b> Wirkdauer</span>"""
if old2 not in content:
    print("WARNUNG 2: Wirkdauer-Chip nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: 'Wirkdauer'-Chip -> neuer Artikel.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Chip "THC vs. CBD"
# ─────────────────────────────────────────────────────────────────────────
old3 = """<span class="kchip" onclick="gotoEntry('library','cannabinoide',0)"><b>↗</b> THC vs. CBD</span>"""
new3 = """<span class="kchip" onclick="gotoEntry('library','artikel',6)"><b>↗</b> THC vs. CBD</span>"""
if old3 not in content:
    print("WARNUNG 3: THC-vs-CBD-Chip nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: 'THC vs. CBD'-Chip -> neuer Artikel.")

# ─────────────────────────────────────────────────────────────────────────
# 4) Chip "Mikrodosierung"
# ─────────────────────────────────────────────────────────────────────────
old4 = """<span class="kchip" onclick="showPage('calc')"><b>↗</b> Mikrodosierung</span>"""
new4 = """<span class="kchip" onclick="gotoEntry('library','artikel',5)"><b>↗</b> Mikrodosierung</span>"""
if old4 not in content:
    print("WARNUNG 4: Mikrodosierung-Chip nicht gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: 'Mikrodosierung'-Chip -> neuer Artikel (mit Link zurück zum Rechner im Artikel selbst).")

# ─────────────────────────────────────────────────────────────────────────
# 5) Chip "Decarboxylierung"
# ─────────────────────────────────────────────────────────────────────────
old5 = """<span class="kchip" onclick="gotoEntry('library','dekarb',0)"><b>↗</b> Decarboxylierung</span>"""
new5 = """<span class="kchip" onclick="gotoEntry('library','artikel',7)"><b>↗</b> Decarboxylierung</span>"""
if old5 not in content:
    print("WARNUNG 5: Decarboxylierung-Chip nicht gefunden.")
else:
    content = content.replace(old5, new5)
    changes += 1
    print(f"5/{total}: 'Decarboxylierung'-Chip -> neuer Artikel.")

# ─────────────────────────────────────────────────────────────────────────
# 6) Konsistenzfix: bereits liver Artikel "Essen vs. Inhalieren" -- Wirkdauer
#    von "6 bis 10 Stunden" auf denselben Kernbereich (4-8h) angeglichen
# ─────────────────────────────────────────────────────────────────────────
old6 = """Der orale Rausch hält zudem deutlich länger an — oft 6 bis 10 Stunden."""
new6 = """Der orale Rausch hält zudem deutlich länger an — meist 4–8 Stunden, bei hohen Dosen oder empfindlichen Personen auch darüber hinaus."""

if old6 not in content:
    print("WARNUNG 6: Wirkdauer-Satz im Essen/Inhalieren-Artikel nicht gefunden.")
else:
    content = content.replace(old6, new6)
    changes += 1
    print(f"6/{total}: Wirkdauer-Angabe im 'Essen vs. Inhalieren'-Artikel auf 4–8h (Kernbereich) angeglichen.")

# ─────────────────────────────────────────────────────────────────────────
# 7) Konsistenzfix: Onset-Unterschied (30-120min vs. 60-120min) im selben
#    Artikel als Erstwirkung-vs-Peak begruendet statt unerklaert stehen zu lassen
# ─────────────────────────────────────────────────────────────────────────
old7 = """Bis die maximale Blutkonzentration erreicht ist, vergehen bei Edibles meist 60–120 Minuten. Genau hier liegt die grösste Gefahr:"""
new7 = """Bis die maximale Blutkonzentration erreicht ist, vergehen bei Edibles oft 60–120 Minuten — erste, schwächere Effekte können aber schon ab 30 Minuten spürbar sein (Onset ≠ Peak, zwei unterschiedliche Zeitpunkte im selben Prozess). Genau hier liegt die grösste Gefahr:"""

if old7 not in content:
    print("WARNUNG 7: Onset-Satz im Essen/Inhalieren-Artikel nicht gefunden.")
else:
    content = content.replace(old7, new7)
    changes += 1
    print(f"7/{total}: Onset-Unterschied (30 vs. 60–120 Min.) im Artikel explizit begründet.")


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
