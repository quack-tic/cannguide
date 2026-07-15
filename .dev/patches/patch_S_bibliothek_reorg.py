#!/usr/bin/env python3
# Patch S: Loesungsmittel, Profi-Tricks, Dekarboxylierung und Troubleshooting
# als eigenstaendige Kategorien aufgeloest und thematisch in Extrakte, Produkte
# und Konsum & Methoden einsortiert. Fuehrt Zwischenueberschriften (sub) in der
# Bibliotheks-Darstellung ein, damit grosse Kategorien uebersichtlich bleiben.
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 6

# ─────────────────────────────────────────────────────────────────────────
# 1) CSS: Stil fuer Zwischenueberschriften in der Bibliothek
# ─────────────────────────────────────────────────────────────────────────
old1 = """.lib-title{font-size:var(--fs-lg);font-weight:600;color:var(--text2);margin-bottom:.625rem;padding-bottom:7px;border-bottom:1px solid var(--border)}"""
new1 = """.lib-title{font-size:var(--fs-lg);font-weight:600;color:var(--text2);margin-bottom:.625rem;padding-bottom:7px;border-bottom:1px solid var(--border)}
.lib-subhead{font-size:var(--fs-sm);font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--accent);margin:1.1rem 0 .5rem;padding-top:.25rem}"""

if old1 not in content:
    print("WARNUNG 1: .lib-title CSS nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: CSS für Zwischenüberschriften (.lib-subhead) hinzugefügt.")

# ─────────────────────────────────────────────────────────────────────────
# 2) renderLib(): cats-Objekt ohne die 4 aufgeloesten Kategorien,
#    plus Unterstuetzung fuer {sub:'...'}-Zwischenueberschriften
# ─────────────────────────────────────────────────────────────────────────
old2 = """  var cats = {loesungsmittel:'Lösungsmittel', tricks:'Profi-Tricks', dekarb:'Dekarboxylierung', fehler:'Troubleshooting', extrakte:'🔷 Extrakte', cannabinoide:'🧪 Cannabinoide', ecs:'🔬 ECS', botanik:'🌿 Botanik', produkte:'🍃 Produkte', konsum:'💨 Konsum', grow:'🌱 Anbau', medizin:'💊 Medizin', wechselwirkungen:'⚕️ Wechselwirkungen', risiken:'⚠️ Risiken', szene:'📖 Szene', artikel:'📰 Vertiefungsartikel'};
  var tabs = '';
  Object.keys(cats).forEach(function(k){
    tabs += '<button class="nb'+(k===activeLibCat?' active':'')+'" onclick="setLibCat(\\''+k+'\\')">'+cats[k]+'</button>';
  });
  document.getElementById('lib-tabs').innerHTML = tabs;
  var sec = LIB[activeLibCat];
  var h = '<div class="lib-sec"><div class="lib-title">'+sec.cat+'</div>';
  sec.items.forEach(function(item, i){
    var id = 'l'+activeLibCat+i;
    h += '<div class="le" onclick="toggleEntry(\\''+id+'\\')"><div class="le-title">'+item.t+'<span style="color:var(--text3);flex-shrink:0">⌄</span></div><div class="le-body" id="'+id+'">'+item.b+'</div></div>';
  });
  h += '</div>';
  document.getElementById('lib-content').innerHTML = h;
}"""

new2 = """  var cats = {extrakte:'🔷 Extrakte', cannabinoide:'🧪 Cannabinoide', ecs:'🔬 ECS', botanik:'🌿 Botanik', produkte:'🍃 Produkte', konsum:'💨 Konsum', grow:'🌱 Anbau', medizin:'💊 Medizin', wechselwirkungen:'⚕️ Wechselwirkungen', risiken:'⚠️ Risiken', szene:'📖 Szene', artikel:'📰 Vertiefungsartikel'};
  var tabs = '';
  Object.keys(cats).forEach(function(k){
    tabs += '<button class="nb'+(k===activeLibCat?' active':'')+'" onclick="setLibCat(\\''+k+'\\')">'+cats[k]+'</button>';
  });
  document.getElementById('lib-tabs').innerHTML = tabs;
  var sec = LIB[activeLibCat];
  var h = '<div class="lib-sec"><div class="lib-title">'+sec.cat+'</div>';
  sec.items.forEach(function(item, i){
    if(item.sub){ h += '<div class="lib-subhead">'+item.sub+'</div>'; return; }
    var id = 'l'+activeLibCat+i;
    h += '<div class="le" onclick="toggleEntry(\\''+id+'\\')"><div class="le-title">'+item.t+'<span style="color:var(--text3);flex-shrink:0">⌄</span></div><div class="le-body" id="'+id+'">'+item.b+'</div></div>';
  });
  h += '</div>';
  document.getElementById('lib-content').innerHTML = h;
}"""

if old2 not in content:
    print("WARNUNG 2: renderLib()-Funktion nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: renderLib() unterstützt jetzt Zwischenüberschriften, 4 Tabs entfernt.")

# ─────────────────────────────────────────────────────────────────────────
# 3) searchIndex(): Zwischenueberschriften von der Suche ausschliessen
# ─────────────────────────────────────────────────────────────────────────
old3 = """  Object.keys(LIB).forEach(function(cat) {
    LIB[cat].items.forEach(function(item, i) {
      var title = stripHtml(item.t).toLowerCase();
      var body = stripHtml(item.b).toLowerCase();
      if (title.indexOf(q) !== -1) {
        titleHits.push({page: 'library', cat: cat, index: i});
      } else if (body.indexOf(q) !== -1) {
        bodyHits.push({page: 'library', cat: cat, index: i});
      }
    });
  });"""

new3 = """  Object.keys(LIB).forEach(function(cat) {
    LIB[cat].items.forEach(function(item, i) {
      if(item.sub) return;
      var title = stripHtml(item.t).toLowerCase();
      var body = stripHtml(item.b).toLowerCase();
      if (title.indexOf(q) !== -1) {
        titleHits.push({page: 'library', cat: cat, index: i});
      } else if (body.indexOf(q) !== -1) {
        bodyHits.push({page: 'library', cat: cat, index: i});
      }
    });
  });"""

if old3 not in content:
    print("WARNUNG 3: searchIndex()-Library-Schleife nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: Suche überspringt Zwischenüberschriften.")

# ─────────────────────────────────────────────────────────────────────────
# 4) LIB: 4 Kategorien entfernen, Inhalte in "extrakte" einsortieren
#    (inkl. Anreicherung des bestehenden "Winterization"-Eintrags)
# ─────────────────────────────────────────────────────────────────────────
old4 = """var LIB = {
  loesungsmittel:{cat:'Lösungsmittel-Vergleich',items:[
    {t:'Vergleichstabelle',b:'<table class="solvent-table"><tr><th>Medium</th><th>Bindung</th><th>Alkohol</th><th>Best for</th></tr><tr><td>Kokosöl nativ</td><td><span class="dot dot-g"></span>~90%</td><td>Nein</td><td>Butter, Backwaren</td></tr><tr><td>Ghee</td><td><span class="dot dot-g"></span>~88%</td><td>Nein</td><td>Backwaren, lang haltbar</td></tr><tr><td>MCT C8/C10</td><td><span class="dot dot-g"></span>~85%</td><td>Nein</td><td>Kapseln, Tropfen</td></tr><tr><td>Butter</td><td><span class="dot dot-a"></span>~78%</td><td>Nein</td><td>Klassische Rezepte</td></tr><tr><td>Glycerin (VG)</td><td><span class="dot dot-a"></span>~55%</td><td>Nein</td><td>Alkoholfrei</td></tr><tr><td>Ethanol 95%</td><td><span class="dot dot-g"></span>~92%</td><td>Ja</td><td>Tinktur, FECO, RSO</td></tr><tr><td>N-Butan</td><td><span class="dot dot-g"></span>~90%</td><td>Nein*</td><td>BHO, Shatter, Wax</td></tr></table><p style="font-size:11px;color:var(--text3);margin-top:6px">* N-Butan ist kein Alkohol, aber brennbar/explosiv</p>'},
    {t:'MCT vs. Kokosöl',b:'MCT immer flüssig: Kapseln, Tropfen. Kokosöl wird fest: Butter-Ersatz. MCT C8 schnellste Absorption ohne Gallensalze.'},
    {t:'Glycerin: Vor/Nachteile',b:'Vorteile: Alkoholfrei, süsslich. Nachteile: 40–60% der Ethanol-Ausbeute, sehr viskös.'},
    {t:'Ethanol-Qualitätsstufen',b:'96% Lebensmittel: Standard. 99.9% anhydrous: reinste Extraktion. Niemals Isopropanol!'},
    {t:'Materialwahl bei Lösungsmitteln',b:'Bei organischen Lösungsmitteln (Ethanol, Ether, Butan, Propanol) ausschliesslich Glas oder Edelstahl verwenden. Plastik und Silikon können bei längerem Kontakt Moleküle abgeben. Silikonmatten erst nach vollständigem Lösungsmittelentzug verwenden.'}
  ]},
  tricks:{cat:'Profi-Tricks',items:[
    {t:'Ghee selbst klären',b:'Butter langsam schmelzen bis Molke absinkt. Reines Butterfett abgiessen. Kein Wasseranteil: bessere Extraktion, länger haltbar.'},
    {t:'Magnetrührer',b:'Heizplatte mit Magnetrührer (~40€): konstante Temp, automatisches Rühren. 3h ohne Eingriff.'},
    {t:'Freeze-Thaw',b:'8h einfrieren, auftauen, wiederholen. 2–3 Zyklen. Erhöht Bioverfügbarkeit nachweislich.'},
    {t:'Winterization',b:'Rohextrakt in –20°C Ethanol (10:1), 24–48h. Wachse flocken aus. Klar, rein, weniger Eigengeschmack.'},
    {t:'QWET: –22°C',b:'Bei –22°C flocken Wachse und Lipide deutlich effektiver aus als bei –18°C. Unter –18°C kaum bis kein sichtbares Ausfallen. Tiefkühler auf Maximum oder Trockeneis verwenden.'},
    {t:'Gummies: Bloom verhindern',b:'Vollständige Emulgierung + langsames Abkühlen + 5–10% Glycerin.'},
    {t:'Schokolade temperieren',b:'Zartbitter: 50°C→28°C→32°C. Vollmilch: 45°C→27°C→30°C. Weiss: 40°C→26°C→28°C.'},
    {t:'Terp Sauce zurückführen',b:'Terpen-Fraktion aus Destillation oder Zentrifugation zum fertigen Destillat zurückführen → Vollspektrum-Produkt mit Entourage-Effekt.'}
  ]},
  dekarb:{cat:'Dekarboxylierung',items:[
    {t:'Warum Dekarb?',b:'THCA zu THC durch Hitze. Ohne Dekarb kaum Wirkung. Auch CBDA zu CBD. THCA-Kristalle besonders wichtig!'},
    {t:'Temperaturen',b:'THC: 110°C / 30 Min. CBD: 120°C / 40 Min. THCA-Kristalle: 120°C / 45–60 Min. Terpene ab 100°C flüchtig.'},
    {t:'Mason Jar',b:'Im verschlossenen Glas: weniger Geruch, Terpene kondensieren zurück. +10 Min.'},
    {t:'Sous-Vide',b:'Vakuumversiegelt, 93°C / 2h. Minimale Terpenverluste, kein Geruch.'}
  ]},
  fehler:{cat:'Troubleshooting',items:[
    {t:'Kein Effekt',b:'1) Dekarb fehlt. 2) Infusion zu heiss. 3) Onset abwarten (bis 2h!). 4) Fettigen Snack essen.'},
    {t:'Hot Spots',b:'Emulgator fehlt, ungleichmässig gemischt. Immer Lecithin + Stabmixer + Waage.'},
    {t:'Trübe Tinktur',b:'Kontaktzeit zu lang. Kürzer waschen, Aktivkohle, Winterization.'},
    {t:'Klebrige Hard Candies',b:'Zu wenig Glukosesirup. Sofort verpacken, Silica Gel.'}
  ]},
  extrakte:{cat:'Extrakt-Begriffe & Konzentrate',items:[
    {t:'Shatter',b:'<span class="lex-term">Shatter</span><span class="lex-tag conc">BHO</span><span class="lex-tag adv">Fortgeschritten</span><br>Transparentes, glasartiges BHO-Konzentrat. 70–90% THC.'},
    {t:'Wax / Budder',b:'<span class="lex-term">Wax / Budder</span><span class="lex-tag conc">BHO</span><br>Cremige, opake Konsistenz. 65–85% THC.'},
    {t:'Live Resin',b:'<span class="lex-term">Live Resin</span><span class="lex-tag conc">BHO</span><br>BHO aus frisch gefrorenem Material. Maximale Terpene.'},
    {t:'Sauce / HTFSE',b:'<span class="lex-term">Sauce / HTFSE</span><span class="lex-tag conc">BHO</span><br>High Terpene Full Spectrum Extract. Flüssig, terpenreich, oft mit THCA-Kristallen.'},
    {t:'Diamonds / THCA-Kristalle',b:'<span class="lex-term">Diamonds</span><span class="lex-tag conc">Kristalle</span><br>THCA-Kristalle bis 99%. Nicht aktiv ohne Dekarb!'},
    {t:'Rosin',b:'<span class="lex-term">Rosin</span><span class="lex-tag conc">Lösungsmittelfrei</span><br>Hitzepresse-Extrakt, 60–80%. Kein Lösungsmittel.'},
    {t:'RSO',b:'<span class="lex-term">RSO</span><span class="lex-tag conc">Vollspektrum</span><span class="lex-tag adv">Fortgeschritten</span><br>Rick Simpson Oil. Vollspektrum-Warmextrakt. 40–70%.'},
    {t:'FECO',b:'<span class="lex-term">FECO</span><span class="lex-tag conc">Vollspektrum</span><br>Full Extract Cannabis Oil. Kaltextrakt + Winterization. 50–80%.'},
    {t:'Destillat',b:'<span class="lex-term">Destillat</span><span class="lex-tag conc">Reinprodukt</span><span class="lex-tag adv">Fortgeschritten</span><br>Vakuumdestillation. 85–99%. Geschmacksneutral.'},
    {t:'Entourage-Effekt',b:'<span class="lex-term">Entourage-Effekt</span><span class="lex-tag base">Konzept</span><br>Synergistische Wirkung aller Cannabinoide + Terpene. Vollspektrum > Isolat für ganzheitliche Wirkung.'},
    {t:'Winterization',b:'<span class="lex-term">Winterization</span><span class="lex-tag base">Prozessschritt</span><br>Rohextrakt bei –20°C: Wachse flocken aus. Ergebnis: klar, rein.'},
    {t:'Purging',b:'<span class="lex-term">Purging</span><span class="lex-tag adv">BHO</span><br>Entfernung von Restbutan im Vakuumofen. Temp + Zeit = Konsistenz.'},
    {t:'Closed Loop',b:'<span class="lex-term">Closed Loop</span><span class="lex-tag adv">Fortgeschritten</span><br>Geschlossenes BHO-System. Einzige sichere Methode. Open Blast = lebensgefährlich.'},
    {t:'Dekarboxylierung',b:'<span class="lex-term">Dekarboxylierung</span><span class="lex-tag base">Grundprozess</span><br>THCA→THC, CBDA→CBD durch Hitze. Pflicht für alle Edibles.'}
  ]},"""

new4 = """var LIB = {
  extrakte:{cat:'Extrakt-Begriffe & Konzentrate',items:[
    {t:'Shatter',b:'<span class="lex-term">Shatter</span><span class="lex-tag conc">BHO</span><span class="lex-tag adv">Fortgeschritten</span><br>Transparentes, glasartiges BHO-Konzentrat. 70–90% THC.'},
    {t:'Wax / Budder',b:'<span class="lex-term">Wax / Budder</span><span class="lex-tag conc">BHO</span><br>Cremige, opake Konsistenz. 65–85% THC.'},
    {t:'Live Resin',b:'<span class="lex-term">Live Resin</span><span class="lex-tag conc">BHO</span><br>BHO aus frisch gefrorenem Material. Maximale Terpene.'},
    {t:'Sauce / HTFSE',b:'<span class="lex-term">Sauce / HTFSE</span><span class="lex-tag conc">BHO</span><br>High Terpene Full Spectrum Extract. Flüssig, terpenreich, oft mit THCA-Kristallen.'},
    {t:'Diamonds / THCA-Kristalle',b:'<span class="lex-term">Diamonds</span><span class="lex-tag conc">Kristalle</span><br>THCA-Kristalle bis 99%. Nicht aktiv ohne Dekarb!'},
    {t:'Rosin',b:'<span class="lex-term">Rosin</span><span class="lex-tag conc">Lösungsmittelfrei</span><br>Hitzepresse-Extrakt, 60–80%. Kein Lösungsmittel.'},
    {t:'RSO',b:'<span class="lex-term">RSO</span><span class="lex-tag conc">Vollspektrum</span><span class="lex-tag adv">Fortgeschritten</span><br>Rick Simpson Oil. Vollspektrum-Warmextrakt. 40–70%.'},
    {t:'FECO',b:'<span class="lex-term">FECO</span><span class="lex-tag conc">Vollspektrum</span><br>Full Extract Cannabis Oil. Kaltextrakt + Winterization. 50–80%.'},
    {t:'Destillat',b:'<span class="lex-term">Destillat</span><span class="lex-tag conc">Reinprodukt</span><span class="lex-tag adv">Fortgeschritten</span><br>Vakuumdestillation. 85–99%. Geschmacksneutral.'},
    {t:'Entourage-Effekt',b:'<span class="lex-term">Entourage-Effekt</span><span class="lex-tag base">Konzept</span><br>Synergistische Wirkung aller Cannabinoide + Terpene. Vollspektrum > Isolat für ganzheitliche Wirkung.'},
    {t:'Winterization',b:'<span class="lex-term">Winterization</span><span class="lex-tag base">Prozessschritt</span><br>Rohextrakt bei –20°C: Wachse flocken aus. Praktisch: Rohextrakt in –20°C Ethanol (10:1) 24–48h ansetzen — Ergebnis: klar, rein, weniger Eigengeschmack.'},
    {t:'Purging',b:'<span class="lex-term">Purging</span><span class="lex-tag adv">BHO</span><br>Entfernung von Restbutan im Vakuumofen. Temp + Zeit = Konsistenz.'},
    {t:'Closed Loop',b:'<span class="lex-term">Closed Loop</span><span class="lex-tag adv">Fortgeschritten</span><br>Geschlossenes BHO-System. Einzige sichere Methode. Open Blast = lebensgefährlich.'},
    {t:'Dekarboxylierung',b:'<span class="lex-term">Dekarboxylierung</span><span class="lex-tag base">Grundprozess</span><br>THCA→THC, CBDA→CBD durch Hitze. Pflicht für alle Edibles.'},
    {sub:'Herstellung & Technik'},
    {t:'Magnetrührer',b:'Heizplatte mit Magnetrührer (~40€): konstante Temp, automatisches Rühren. 3h ohne Eingriff.'},
    {t:'Freeze-Thaw',b:'8h einfrieren, auftauen, wiederholen. 2–3 Zyklen. Erhöht Bioverfügbarkeit nachweislich.'},
    {t:'QWET: –22°C',b:'Bei –22°C flocken Wachse und Lipide deutlich effektiver aus als bei –18°C. Unter –18°C kaum bis kein sichtbares Ausfallen. Tiefkühler auf Maximum oder Trockeneis verwenden.'},
    {t:'Terp Sauce zurückführen',b:'Terpen-Fraktion aus Destillation oder Zentrifugation zum fertigen Destillat zurückführen → Vollspektrum-Produkt mit Entourage-Effekt.'}
  ]},"""

if old4 not in content:
    print("WARNUNG 4: LIB-Block (4 Kategorien + extrakte) nicht (exakt) gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: 4 Kategorien entfernt, Inhalte in 'Extrakte' einsortiert (inkl. Winterization-Zusammenführung).")

# ─────────────────────────────────────────────────────────────────────────
# 5) "produkte": Zutaten/Lösungsmittel + Troubleshooting anhängen
# ─────────────────────────────────────────────────────────────────────────
old5 = """    {t:'Tinktur (Alkohol-Extrakt)',b:'<span class="lex-term">Tinktur</span><span class="lex-tag base">Lebensmittelauszug</span><br>Eine Tinktur ist ein Lebensmittelauszug: Cannabis wird in trinkfähigem Alkohol (z.B. Wodka 40 Vol.%, Rum) angesetzt — ähnlich wie kräuterbasierte Hausmittel. Der Alkoholgehalt liegt im trinkfähigen Bereich und extrahiert Cannabinoide und Terpene schonend. Onset sublingual (unter die Zunge): 15–45 Minuten — schneller als Edibles, gut dosierbar. Bei Schlucken wirkt sie wie ein Edible (längerer Onset durch Leberpassage). Hochprozentiger Laborethanol (≥60 Vol.%) gehört zur Wirkstoffextraktion — das ist eine andere Kategorie.'}
  ]},
  konsum:{cat:'Konsum & Methoden',items:["""

new5 = """    {t:'Tinktur (Alkohol-Extrakt)',b:'<span class="lex-term">Tinktur</span><span class="lex-tag base">Lebensmittelauszug</span><br>Eine Tinktur ist ein Lebensmittelauszug: Cannabis wird in trinkfähigem Alkohol (z.B. Wodka 40 Vol.%, Rum) angesetzt — ähnlich wie kräuterbasierte Hausmittel. Der Alkoholgehalt liegt im trinkfähigen Bereich und extrahiert Cannabinoide und Terpene schonend. Onset sublingual (unter die Zunge): 15–45 Minuten — schneller als Edibles, gut dosierbar. Bei Schlucken wirkt sie wie ein Edible (längerer Onset durch Leberpassage). Hochprozentiger Laborethanol (≥60 Vol.%) gehört zur Wirkstoffextraktion — das ist eine andere Kategorie.'},
    {sub:'Zutaten & Lösungsmittel'},
    {t:'Vergleichstabelle',b:'<table class="solvent-table"><tr><th>Medium</th><th>Bindung</th><th>Alkohol</th><th>Best for</th></tr><tr><td>Kokosöl nativ</td><td><span class="dot dot-g"></span>~90%</td><td>Nein</td><td>Butter, Backwaren</td></tr><tr><td>Ghee</td><td><span class="dot dot-g"></span>~88%</td><td>Nein</td><td>Backwaren, lang haltbar</td></tr><tr><td>MCT C8/C10</td><td><span class="dot dot-g"></span>~85%</td><td>Nein</td><td>Kapseln, Tropfen</td></tr><tr><td>Butter</td><td><span class="dot dot-a"></span>~78%</td><td>Nein</td><td>Klassische Rezepte</td></tr><tr><td>Glycerin (VG)</td><td><span class="dot dot-a"></span>~55%</td><td>Nein</td><td>Alkoholfrei</td></tr><tr><td>Ethanol 95%</td><td><span class="dot dot-g"></span>~92%</td><td>Ja</td><td>Tinktur, FECO, RSO</td></tr><tr><td>N-Butan</td><td><span class="dot dot-g"></span>~90%</td><td>Nein*</td><td>BHO, Shatter, Wax</td></tr></table><p style="font-size:11px;color:var(--text3);margin-top:6px">* N-Butan ist kein Alkohol, aber brennbar/explosiv</p>'},
    {t:'MCT vs. Kokosöl',b:'MCT immer flüssig: Kapseln, Tropfen. Kokosöl wird fest: Butter-Ersatz. MCT C8 schnellste Absorption ohne Gallensalze.'},
    {t:'Glycerin: Vor/Nachteile',b:'Vorteile: Alkoholfrei, süsslich. Nachteile: 40–60% der Ethanol-Ausbeute, sehr viskös.'},
    {t:'Ethanol-Qualitätsstufen',b:'96% Lebensmittel: Standard. 99.9% anhydrous: reinste Extraktion. Niemals Isopropanol!'},
    {t:'Materialwahl bei Lösungsmitteln',b:'Bei organischen Lösungsmitteln (Ethanol, Ether, Butan, Propanol) ausschliesslich Glas oder Edelstahl verwenden. Plastik und Silikon können bei längerem Kontakt Moleküle abgeben. Silikonmatten erst nach vollständigem Lösungsmittelentzug verwenden.'},
    {t:'Ghee selbst klären',b:'Butter langsam schmelzen bis Molke absinkt. Reines Butterfett abgiessen. Kein Wasseranteil: bessere Extraktion, länger haltbar.'},
    {t:'Schokolade temperieren',b:'Zartbitter: 50°C→28°C→32°C. Vollmilch: 45°C→27°C→30°C. Weiss: 40°C→26°C→28°C.'},
    {t:'Gummies: Bloom verhindern',b:'Vollständige Emulgierung + langsames Abkühlen + 5–10% Glycerin.'},
    {sub:'Troubleshooting'},
    {t:'Kein Effekt',b:'1) Dekarb fehlt. 2) Infusion zu heiss. 3) Onset abwarten (bis 2h!). 4) Fettigen Snack essen.'},
    {t:'Hot Spots',b:'Emulgator fehlt, ungleichmässig gemischt. Immer Lecithin + Stabmixer + Waage.'},
    {t:'Trübe Tinktur',b:'Kontaktzeit zu lang. Kürzer waschen, Aktivkohle, Winterization.'},
    {t:'Klebrige Hard Candies',b:'Zu wenig Glukosesirup. Sofort verpacken, Silica Gel.'}
  ]},
  konsum:{cat:'Konsum & Methoden',items:["""

if old5 not in content:
    print("WARNUNG 5: Einfügepunkt in 'produkte' nicht gefunden.")
else:
    content = content.replace(old5, new5)
    changes += 1
    print(f"5/{total}: 'Zutaten & Lösungsmittel' und 'Troubleshooting' in 'Produkte' eingefügt.")

# ─────────────────────────────────────────────────────────────────────────
# 6) "konsum": Dekarboxylierungs-Grundlagen neben die bestehenden Decarb-
#    Einträge stellen
# ─────────────────────────────────────────────────────────────────────────
old6 = """    {t:'Decarb bei Extrakten & Konzentraten',b:'<span class="lex-term">Decarb bei Extrakten</span><span class="lex-tag adv">Fortgeschritten</span><br>[ROHENTWURF – bitte prüfen] Ob ein Extrakt bereits decarboxyliert ist, hängt vom Herstellungsprozess ab – nicht vom Produktnamen. Entscheidend ist, ob dabei über längere Zeit Temperaturen um ~115 °C erreicht wurden. Vakuumdestillation trennt das Lösungsmittel bei ~50 °C ab – dabei wird nichts aktiviert. FECO muss aktiv decarboxyliert werden. RSO erreicht auf üblichen Wegen die nötige Temperatur meist nicht – im Zweifel decarboxylieren. Bei der Fraktionsdestillation von FECO zu Cannabinoïdöl muss bereits vorher decarbt werden, sonst entsteht bei der Fraktionierung zu viel CO₂. Faustregel: Bist du unsicher, behandle den Extrakt als Rohwert und decarboxyliere. Kalt eingerührtes Roh-Konzentrat wirkt kaum – und verleitet beim nächsten Versuch zur gefährlichen Überdosierung.'},
    {t:'Inhalation — Grundlagen',b:'<span class="lex-term">Inhalation</span><span class="lex-tag base">Konsummethode</span><br>Bei der Inhalation gelangen Cannabinoide über die Lungen direkt ins Blut. Wirkungseintritt: 30–90 Sekunden, Peak: 10–30 Minuten, Dauer: 1–3 Stunden. Im Vergleich zu Edibles ist die Wirkung kürzer und besser steuerbar. Beim Verbrennen entstehen Verbrennungsprodukte wie Benzol, Kohlenmonoxid und Teer — ähnlich wie beim Tabakrauchen.'},"""

new6 = """    {t:'Decarb bei Extrakten & Konzentraten',b:'<span class="lex-term">Decarb bei Extrakten</span><span class="lex-tag adv">Fortgeschritten</span><br>[ROHENTWURF – bitte prüfen] Ob ein Extrakt bereits decarboxyliert ist, hängt vom Herstellungsprozess ab – nicht vom Produktnamen. Entscheidend ist, ob dabei über längere Zeit Temperaturen um ~115 °C erreicht wurden. Vakuumdestillation trennt das Lösungsmittel bei ~50 °C ab – dabei wird nichts aktiviert. FECO muss aktiv decarboxyliert werden. RSO erreicht auf üblichen Wegen die nötige Temperatur meist nicht – im Zweifel decarboxylieren. Bei der Fraktionsdestillation von FECO zu Cannabinoïdöl muss bereits vorher decarbt werden, sonst entsteht bei der Fraktionierung zu viel CO₂. Faustregel: Bist du unsicher, behandle den Extrakt als Rohwert und decarboxyliere. Kalt eingerührtes Roh-Konzentrat wirkt kaum – und verleitet beim nächsten Versuch zur gefährlichen Überdosierung.'},
    {t:'Warum Dekarb?',b:'THCA zu THC durch Hitze. Ohne Dekarb kaum Wirkung. Auch CBDA zu CBD. THCA-Kristalle besonders wichtig!'},
    {t:'Dekarb-Temperaturen im Überblick',b:'THC: 110°C / 30 Min. CBD: 120°C / 40 Min. THCA-Kristalle: 120°C / 45–60 Min. Terpene ab 100°C flüchtig.'},
    {t:'Dekarb im Mason Jar',b:'Im verschlossenen Glas: weniger Geruch, Terpene kondensieren zurück. +10 Min.'},
    {t:'Dekarb Sous-Vide',b:'Vakuumversiegelt, 93°C / 2h. Minimale Terpenverluste, kein Geruch.'},
    {t:'Inhalation — Grundlagen',b:'<span class="lex-term">Inhalation</span><span class="lex-tag base">Konsummethode</span><br>Bei der Inhalation gelangen Cannabinoide über die Lungen direkt ins Blut. Wirkungseintritt: 30–90 Sekunden, Peak: 10–30 Minuten, Dauer: 1–3 Stunden. Im Vergleich zu Edibles ist die Wirkung kürzer und besser steuerbar. Beim Verbrennen entstehen Verbrennungsprodukte wie Benzol, Kohlenmonoxid und Teer — ähnlich wie beim Tabakrauchen.'},"""

if old6 not in content:
    print("WARNUNG 6: Einfügepunkt in 'konsum' nicht gefunden.")
else:
    content = content.replace(old6, new6)
    changes += 1
    print(f"6/{total}: Dekarb-Grundlagen zu den bestehenden Decarb-Einträgen in 'Konsum & Methoden' gestellt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
