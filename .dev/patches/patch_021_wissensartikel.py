#!/usr/bin/env python3
# Patch I: Neue Kategorie "Vertiefungsartikel" (4 Blogbeitraege aus NotebookLM/157-Quellen-Korpus),
#          Meistgelesen final auf diese Artikel verlinkt inkl. echter Kurzquellen statt Platzhalter.
#
# VORAUSSETZUNG: Patch H (patch_H_wechselwirkungen_und_startseite.py) wurde bereits angewendet.
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 3

# ─────────────────────────────────────────────────────────────────────────
# 1) Neue LIB-Kategorie "artikel" nach "wechselwirkungen" einfuegen
#    (Ankerpunkt: Ende der wechselwirkungen-Items aus Patch H, vor "risiken")
# ─────────────────────────────────────────────────────────────────────────
old1 = """Diese Liste ist nicht vollständig — bei jeder Dauermedikation lohnt sich die gezielte Nachfrage nach CYP450-Interaktionen bei Arzt oder Apotheke.'}
  ]},
  risiken:{cat:'Physiologie & Risiken',items:["""

new1 = """Diese Liste ist nicht vollständig — bei jeder Dauermedikation lohnt sich die gezielte Nachfrage nach CYP450-Interaktionen bei Arzt oder Apotheke.'}
  ]},
  artikel:{cat:'Vertiefungsartikel',items:[
    {t:'Warum Essen und Inhalieren zwei völlig verschiedene Rauscherlebnisse sind',b:'[ROHENTWURF – bitte prüfen] <b>Die Expressroute: Inhalieren</b><br>Beim Rauchen oder Vapen gelangt THC über die Lungenbläschen direkt in den Blutkreislauf — vorbei an Magen-Darm-Trakt und Leber. Die Wirkung (Onset) setzt innerhalb von Sekunden bis maximal einer Minute ein, die Blutkonzentration steigt rasant. Weil das so unmittelbar geschieht, lässt sich die Dosis beim Inhalieren vergleichsweise gut steuern — man spürt schnell, wann es reicht.<br><br><b>Der lange Weg: Essen und die Leber</b><br>Bei oraler Aufnahme ist die Resorption von Natur aus träge, langsam und unregelmässig. THC wird im oberen Magen-Darm-Trakt aufgenommen und wandert über die Pfortader zuerst in die Leber (First-Pass-Effekt). Dort wird ein grosser Teil des Delta-9-THC zu <b>11-Hydroxy-THC (11-OH-THC)</b> umgewandelt — einem Metaboliten, der die Blut-Hirn-Schranke effizienter überwindet und stärker sowie körperlastiger wirkt als das ursprüngliche THC.<br><br><b>Das Problem mit dem Onset</b><br>Bis die maximale Blutkonzentration erreicht ist, vergehen bei Edibles meist 60–120 Minuten. Genau hier liegt die grösste Gefahr: Wer nach 45 Minuten ungeduldig wird und nachisst, riskiert eine massive Überdosierung, sobald beide Portionen zeitversetzt anfluten. Der orale Rausch hält zudem deutlich länger an — oft 6 bis 10 Stunden.<br><br><b>Fazit</b><br>Wer Cannabis isst, konsumiert de facto eine andere chemische Zusammensetzung als jemand, der raucht oder vapet. Geduld und eine vorsichtige, tiefe Startdosis sind bei Edibles das oberste Gebot.<br><br><span style="font-size:11px;color:var(--text3)">Quellen: Gebhardt (2012); Grotenhermen (2012); Hoch, Friemel & Schneider (Hrsg., 2019/2022); Zernikow (Hrsg., 2022)</span>'},
    {t:'Toleranz — was sich bei regelmässigem Konsum wirklich im Gehirn verändert',b:'[ROHENTWURF – bitte prüfen] <b>Das körpereigene Fine-Tuning: Das Endocannabinoidsystem</b><br>Unser Gehirn reguliert die Signalübertragung ständig selbst nach: Feuern Nervenzellen zu stark, schüttet der Körper eigene Cannabinoide (Anandamid, 2-AG) aus, die rückwärts zum Sender-Neuron wandern und dort an den <b>CB1-Rezeptor</b> andocken — Signal: bremsen. CB1 gehört zu den häufigsten Rezeptoren im Säugetiergehirn, konzentriert in Regionen für Gedächtnis (Hippocampus), Bewegung (Kleinhirn) und Belohnung.<br><br><b>Die Flutwelle: Exogene Cannabinoide</b><br>Beim Konsum überflutet pflanzliches THC dieselben CB1-Rezeptoren — wird aber viel langsamer abgebaut als körpereigene Botenstoffe und besetzt die Rezeptoren dauerhaft. Die Zelle empfindet das als Stress und reagiert mit zwei Schutzmechanismen: <b>Desensitivierung</b> (die Signalkaskade nach dem Andocken wird abgeschwächt) und bei anhaltendem Konsum <b>CB1-Downregulation</b> (Rezeptoren werden von der Oberfläche abgebaut und ins Zellinnere geschleust — ihre Dichte sinkt spürbar).<br><br><b>Die Auswirkung der Downregulation</b><br>Sind viele CB1-Rezeptoren abgebaut, verpufft die Wirkung derselben Dosis — Toleranz. Weil das ECS insgesamt heruntergefahren ist, funktioniert auch der körpereigene Tempomat im Alltag schlechter; abruptes Absetzen kann zu Schlafproblemen, Schwitzen, innerer Unruhe oder lebhaften Träumen führen.<br><br><b>Die gute Nachricht: Das Gehirn regeneriert sich</b><br>Anders als bei manch anderen Substanzen ist die CB1-Downregulation in der Regel vollständig reversibel. Bildgebende Studien zeigen, dass sich die CB1-Rezeptordichte nach etwa 3–4 Wochen konsequenter Konsumpause weitgehend normalisiert.<br><br><span style="font-size:11px;color:var(--text3)">Quellen: Hoch, Friemel & Schneider (Hrsg., 2019/2022); Zernikow (Hrsg., 2022)</span>'},
    {t:'Gefährliche Wechselwirkungen — warum Medikamente + Cannabis riskanter sind als gedacht',b:'[ROHENTWURF – bitte prüfen] <b>Die biologische Sortieranlage: CYP450</b><br>Medikamente werden in der Leber vor allem über die Cytochrom-P450-Enzymfamilie abgebaut — allen voran die "Fliessbänder" <b>CYP3A4</b> und <b>CYP2C9</b>, über die schätzungsweise die Hälfte aller gängigen Medikamente laufen: Schmerzmittel, Antidepressiva, Blutverdünner, Betablocker.<br><br><b>Cannabis als Blockade in der Sortieranlage</b><br>THC und vor allem CBD wirken als Enzym-Inhibitoren und blockieren CYP3A4/CYP2C9 teilweise. Andere Medikamente, die dasselbe Fliessband benötigen, werden dann langsamer abgebaut, stauen sich im Blut an — mit dem Risiko schwerer, potenziell gefährlicher Überdosierungen.<br><br><b>Konkrete Risikokombinationen im Überblick</b><br>1. Opioide/starke Schmerzmittel (z.B. Oxycodon, Tramadol): verstärkte Sedierung, Atemdepression, Krampfanfallrisiko.<br>2. Psychopharmaka/Antidepressiva (z.B. Duloxetin, Haloperidol, Olanzapin): unvorhersehbare Serumspiegel, Herzrhythmusstörungen, Blutdruckschwankungen, mögliche Verstärkung von Psychosen.<br>3. Blutverdünner (Warfarin/Phenprocoumon): geringe therapeutische Breite — Blockade von CYP2C9 kann das Blutungsrisiko deutlich erhöhen.<br><br><b>Das zweischneidige Schwert</b><br>Die Wechselwirkung geht auch andersherum: CYP-Inhibitoren (bestimmte Antibiotika, Antimykotika) können den THC-Abbau bremsen und die Wirkung unerwartet verstärken; CYP-Induktoren (z.B. Carbamazepin) können den THC-Spiegel so weit senken, dass eine medizinische Therapie wirkungslos bleibt.<br><br><b>Fazit</b><br>Cannabis ist ein aktiver biochemischer Akteur, kein "sanftes Naturprodukt ohne Interaktionen". Bei bestehender Dauermedikation gehört das Thema zwingend ins Gespräch mit Arzt oder Apotheke.<br><br><span style="font-size:11px;color:var(--text3)">Quellen: Hoch, Friemel & Schneider (Hrsg., 2019/2022); Seifert (2021); Stout & Cimino (2014), Drug Metabolism Reviews</span>'},
    {t:'Der Entourage-Effekt — was die Studienlage wirklich hergibt',b:'[ROHENTWURF – bitte prüfen] <b>Die biologische Basis: Warum die Theorie Sinn ergibt</b><br>Cannabis enthält über 100 Phytocannabinoide und zahlreiche Terpene, die im Körper interagieren können. Am klarsten belegt ist das Zusammenspiel von <b>THC und CBD</b>: CBD wirkt als moderater Gegenspieler am CB1-Rezeptor und dämpft die stark psychotropen Spitzen von THC — ausgewogene THC:CBD-Verhältnisse verursachen statistisch seltener Paranoia, Angst oder Gedächtnisausfälle als reines, hochdosiertes THC. Diese Cannabinoid-Interaktion gilt als wissenschaftlich gut abgesichert.<br><br><b>Die Grauzone: Terpene</b><br>Die eigentliche Debatte betrifft die Terpene. Entgegen der verbreiteten Annahme zeigen pharmakologische In-vitro-Studien, dass die meisten Terpene in konsumrelevanten Konzentrationen <b>keine nennenswerte Affinität zu CB1/CB2-Rezeptoren</b> aufweisen — sie docken dort kaum an.<br><br><b>Was die Studienlage wirklich hergibt</b><br>Wirkungslos sind Terpene deshalb nicht, ihr Mechanismus dürfte aber ein anderer sein:<br>1. Andere Rezeptorsysteme — z.B. moduliert Linalool (auch aus Lavendel bekannt) über das GABA-System beruhigend, unabhängig von Cannabinoid-Rezeptoren.<br>2. Mögliche leichte Effekte auf die Durchlässigkeit von Zellmembranen bzw. der Blut-Hirn-Schranke.<br>Der grösste Schwachpunkt der Forschung: Es fehlen standardisierte klinische Doppelblindstudien am Menschen. Die meisten Entourage-Behauptungen stützen sich auf Erfahrungsberichte oder Tier-/Zellversuche mit unnatürlich hohen Konzentrationen.<br><br><b>Fazit</b><br>Den Entourage-Effekt gibt es — primär belegt über die THC-CBD-Interaktion. Die oft zitierte steuernde Wirkung einzelner Terpene ist dagegen eher ein spannendes Forschungsfeld als harte klinische Evidenz.<br><br><span style="font-size:11px;color:var(--text3)">Quellen: Dyck et al. (2022); Hermann & Schneider (2012); Hoch, Friemel & Schneider (Hrsg., 2019/2022); Russo (2011), British Journal of Pharmacology</span>'}
  ]},
  risiken:{cat:'Physiologie & Risiken',items:["""

if old1 not in content:
    print("WARNUNG 1: Einfügepunkt für 'artikel'-Kategorie nicht gefunden (Patch H schon angewendet?).")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Neue Kategorie 'Vertiefungsartikel' (4 Artikel) eingefügt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) Kategorie in den Bibliotheks-Tabs sichtbar machen
# ─────────────────────────────────────────────────────────────────────────
old2 = """var cats = {loesungsmittel:'Lösungsmittel', tricks:'Profi-Tricks', dekarb:'Dekarboxylierung', fehler:'Troubleshooting', extrakte:'🔷 Extrakte', cannabinoide:'🧪 Cannabinoide', ecs:'🔬 ECS', botanik:'🌿 Botanik', produkte:'🍃 Produkte', konsum:'💨 Konsum', grow:'🌱 Anbau', medizin:'💊 Medizin', risiken:'⚠️ Risiken', szene:'📖 Szene'};"""
new2 = """var cats = {loesungsmittel:'Lösungsmittel', tricks:'Profi-Tricks', dekarb:'Dekarboxylierung', fehler:'Troubleshooting', extrakte:'🔷 Extrakte', cannabinoide:'🧪 Cannabinoide', ecs:'🔬 ECS', botanik:'🌿 Botanik', produkte:'🍃 Produkte', konsum:'💨 Konsum', grow:'🌱 Anbau', medizin:'💊 Medizin', wechselwirkungen:'⚕️ Wechselwirkungen', risiken:'⚠️ Risiken', szene:'📖 Szene', artikel:'📰 Vertiefung'};"""

if old2 not in content:
    print("WARNUNG 2: cats-Objekt in renderLib() nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: 'Wechselwirkungen' + 'Vertiefung' als Bibliotheks-Tabs sichtbar gemacht.")

# ─────────────────────────────────────────────────────────────────────────
# 3) Meistgelesen final: echte Artikel + echte Kurzquellen statt Platzhalter
# ─────────────────────────────────────────────────────────────────────────
old3 = """      <div class="read" onclick="gotoEntry('library','cannabinoide',4)"><span class="rank">01</span><div><div class="t">Wie lange wirken Edibles?</div><div class="m">Sicherheit · 4 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Quelle: [ROHENTWURF]</span></div>
      <div class="read" onclick="gotoEntry('library','cannabinoide',0)"><span class="rank">02</span><div><div class="t">THC und CBD im Vergleich</div><div class="m">Wirkstoffe · 6 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Quelle: [ROHENTWURF]</span></div>
      <div class="read" onclick="gotoEntry('library','dekarb',0)"><span class="rank">03</span><div><div class="t">Was ist Decarboxylierung?</div><div class="m">Konsumformen · 5 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Quelle: [ROHENTWURF]</span></div>
      <div class="read" onclick="gotoEntry('safety','recht',0)"><span class="rank">04</span><div><div class="t">Cannabis-Pilotprojekte Schweiz</div><div class="m">Recht · 7 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Quelle: [ROHENTWURF]</span></div>"""

new3 = """      <div class="read" onclick="gotoEntry('library','artikel',0)"><span class="rank">01</span><div><div class="t">Warum Essen und Inhalieren zwei verschiedene Rauscherlebnisse sind</div><div class="m">Pharmakokinetik · 5 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Grotenhermen 2012</span></div>
      <div class="read" onclick="gotoEntry('library','artikel',1)"><span class="rank">02</span><div><div class="t">Toleranz: Was sich im Gehirn wirklich verändert</div><div class="m">Neurobiologie · 4 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Hoch et al. 2019</span></div>
      <div class="read" onclick="gotoEntry('library','artikel',2)"><span class="rank">03</span><div><div class="t">Wechselwirkungen: Warum Medikamente + Cannabis riskanter sind</div><div class="m">Pharmakologie · 5 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Stout & Cimino 2014</span></div>
      <div class="read" onclick="gotoEntry('library','artikel',3)"><span class="rank">04</span><div><div class="t">Der Entourage-Effekt: Was die Studienlage wirklich hergibt</div><div class="m">Wirkstoffe · 5 Min.</div></div><span class="v" style="font-size:10px;color:var(--text3)">Russo 2011</span></div>"""

if old3 not in content:
    print("WARNUNG 3: Meistgelesen-Block (Patch-H-Version) nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: Meistgelesen final auf die 4 Vertiefungsartikel verlinkt, echte Kurzquellen eingesetzt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — prüfen, ob Patch H vorher gelaufen ist!")
