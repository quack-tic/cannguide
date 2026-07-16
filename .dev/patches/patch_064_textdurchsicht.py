#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch 64 — Systematische Textdurchsicht (CannGuide)
Idempotent. Explizites String-Matching (keine Regex).
Teile A (Fehler), B (Präventionstexte), C (Wizard/Troubleshooting/Herstellung
ausformuliert), D (Beispielsatz), E (Konventionen, gezielt).

Regeln:
- Jede Ersetzung wird nur ausgeführt, wenn das OLD genau 1× vorkommt.
- Kommt OLD 0× und NEW bereits vor  -> ALREADY (idempotent, übersprungen).
- Kommt OLD 0× und NEW nicht vor     -> MISSING (Report, nichts geändert).
- Kommt OLD >1× vor                   -> AMBIGUOUS (Report, nichts geändert).
"""
import sys, io

TARGET = sys.argv[1] if len(sys.argv) > 1 else "index.html"

# (id, old, new)
REPL = []

# ─────────────────────────────────────────────────────────────────────────
# TEIL A — Echte Fehler (Tippfehler & Grammatik)
# ─────────────────────────────────────────────────────────────────────────
REPL += [
("A1 hauptso",
 "Beobachtet hauptso bei täglichem Konsum",
 "Beobachtet wird es hauptsächlich bei täglichem Konsum"),

("A2 Amotiv es-sich",
 "Ob direkter Cannabiseffekt oder Folge vorbestehender psychischer Erkrankungen ist wissenschaftlich umstritten.",
 "Ob es sich um einen direkten Cannabis-Effekt oder um die Folge vorbestehender psychischer Erkrankungen handelt, ist wissenschaftlich umstritten."),

("A3a Vaporer->Vaporizer (Lexikon)",
 "reduzierte Atemwegssymptome bei Vaporer-Nutzung.",
 "reduzierte Atemwegssymptome bei Vaporizer-Nutzung."),

("A3b Vaporer->Vape (Safety)",
 "reduzierte Atemwegssymptome bei Vaporer-Nutzern im Vergleich zu Rauchern.",
 "reduzierte Atemwegssymptome bei Vape-Nutzern im Vergleich zu Rauchern."),

("A4 lohnt ein ehrlicherer Blick",
 "Wer bei einer oder mehreren Fragen zögert, lohnt ein ehrlicherer Blick.",
 "Wenn du bei einer oder mehreren Fragen zögerst, lohnt sich ein ehrlicher Blick."),

("A5 Ersatzhandlungen Komma",
 "Ersatzhandlungen finden die auch Freude bereiten.",
 "Ersatzhandlungen finden, die auch Freude bereiten."),

("A6a hero ersten Mal konsum",
 "besonders wichtig beim ersten Mal konsum!.",
 "besonders wichtig beim ersten Mal!"),

("A6b hero z.B (Kontraindikationen bleibt)",
 "informiere dich über Wirkung, Dauer und Kontraindikationen wie z.B Medikamente oder Vorerkrankungen.",
 "informiere dich über Wirkung, Dauer und Kontraindikationen, zum Beispiel Medikamente oder Vorerkrankungen."),

("A6c hero Umfeld-Satz",
 "Vertraute Umgebung, kein Alkohol, keine Medikamente, nicht am Steuer, nie Konsumieren in anwesenheit von Minderjährigen.",
 "Sorge für eine vertraute Umgebung, verzichte auf Alkohol und Medikamente, setz dich nicht ans Steuer und konsumiere nie in Anwesenheit von Minderjährigen."),
]

# ─────────────────────────────────────────────────────────────────────────
# TEIL B — Kern-Präventionstexte
# ─────────────────────────────────────────────────────────────────────────
REPL += [
("B2 hero Regel 4",
 "Wirkung erst nach 30–120&nbsp;Min. Niemals nachlegen, weil „nichts passiert“.",
 "Die Wirkung setzt erst nach 30–120&nbsp;Minuten ein. Leg niemals nach, nur weil scheinbar „nichts passiert“."),

("B3 Wirkungsdauer",
 "Onset: 30–120 Min. Peak: 2–4h. Dauer: 4–8h. Leerer Magen: schneller + stärker.",
 "Die Wirkung setzt nach 30–120 Minuten ein (Onset), erreicht ihr Maximum nach 2–4 Stunden (Peak) und hält insgesamt 4–8 Stunden an. Auf leeren Magen wirkt sie schneller und stärker."),

("B4 Sichere Lagerung",
 "Kindersichere, beschriftete Behälter. Klar von normalen Lebensmitteln trennen. Kühl, dunkel, trocken. Haustiere ebenfalls empfindlich.",
 "Bewahre Edibles in kindersicheren, beschrifteten Behältern auf und trenne sie klar von normalen Lebensmitteln. Lagere sie kühl, dunkel und trocken. Denk daran: Auch Haustiere reagieren empfindlich auf Cannabis."),

("B5 Risikogruppen",
 "Jugendliche (Gehirn bis ~25 J.), Schwangere, Herzerkrankungen, psychische Erkrankungen. CYP450-Wechselwirkungen mit Medikamenten möglich — Arzt fragen!",
 "Besonders vorsichtig sein sollten Jugendliche (das Gehirn entwickelt sich bis etwa 25), Schwangere sowie Menschen mit Herz- oder psychischen Erkrankungen. Mit Medikamenten sind Wechselwirkungen über das Enzymsystem CYP450 möglich — im Zweifel ärztlichen Rat einholen."),

("B6 od Zeichen",
 "Angst, Panik, Herzrasen, Schwindel, Dissoziation.<br><b style=\"color:var(--warn)\">Bei Bewusstlosigkeit / Atemstörung: 112 / 144!</b>",
 "Mögliche Zeichen sind Angst, Panik, Herzrasen, Schwindel und ein Gefühl der Loslösung von sich selbst (Dissoziation).<br><b style=\"color:var(--warn)\">Bei Bewusstlosigkeit oder Atemproblemen sofort den Notruf wählen: 112 (DE) / 144 (CH & AT)!</b>"),

("B7 od Erste Hilfe",
 "1. Sichern & hinlegen. 2. Beruhigen. 3. Wasser. 4. Frische Luft. 5. 4-7-8 Atemtechnik. 6. Nicht alleine lassen. 7. CBD kann helfen.",
 "1. Die Person sichern und hinlegen. 2. Ruhig zusprechen. 3. Wasser anbieten. 4. Für frische Luft sorgen. 5. Gemeinsam ruhig atmen — 4 Sekunden einatmen, 7 Sekunden halten, 8 Sekunden ausatmen (4-7-8-Technik). 6. Die Person nicht allein lassen. 7. CBD kann die Wirkung abmildern."),

("B8 od 7W",
 "<b style=\"color:var(--accent)\">WO · WAS · WIE VIELE · WELCHER Zustand · WARTEN · WANN · WER</b><br><br>Ehrlich sein — Sanitäter sind keine Polizei.",
 "<b style=\"color:var(--accent)\">WO ist der Notfall? · WAS ist passiert? · WIE VIELE Betroffene? · WELCHER Zustand (ansprechbar, Atmung)? · WARTEN auf Rückfragen · WANN hat es begonnen? · WER ruft an?</b><br><br>Sei ehrlich: Sanitäter sind nicht die Polizei und melden dich nicht an."),

("B9 od Nicht wirken",
 "Mind. 2h warten. Fettigen Snack essen.<br><b style=\"color:var(--warn)\">Niemals doppelte Dosis!</b>",
 "Wenn scheinbar nichts passiert: mindestens 2 Stunden warten und einen fettigen Snack essen — Fett verbessert die Aufnahme.<br><b style=\"color:var(--amber)\">Nimm niemals eine zweite Dosis nach!</b>"),

("B10 sucht Fakten",
 "~9% entwickeln Abhängigkeit. Jugendalter täglich: bis 17%. CUD anerkannte Diagnose. Entzug 1–2 Wochen.",
 "Etwa 9 % aller Konsumierenden entwickeln eine Abhängigkeit; bei täglichem Konsum im Jugendalter sind es bis zu 17 %. Die Cannabis-Abhängigkeit (CUD) ist eine anerkannte Diagnose. Entzugssymptome dauern meist 1–2 Wochen."),

("B11 sucht Warnzeichen",
 "Konsum trotz negativer Folgen. Schwierigkeiten aufzuhören. Stimmungstiefs ohne Konsum. Steigende Toleranz.<br>Selbsttest: CUDIT kostenlos online.",
 "Warnzeichen sind: Konsum trotz negativer Folgen, Schwierigkeiten aufzuhören, Stimmungstiefs ohne Konsum und eine steigende Toleranz. Ein anonymer Selbsttest (CUDIT) ist kostenlos online verfügbar."),

("B12 recht CH",
 "THC illegal. Bis 10g: CHF 100. CBD unter 1% THC legal. Pilotversuche: Basel, Bern, Zürich, Genf.",
 "THC ist illegal. Beim Besitz von bis zu 10 g droht eine Ordnungsbusse von CHF 100. CBD mit weniger als 1 % THC ist legal. Kontrollierte Pilotversuche laufen in Basel, Bern, Zürich und Genf."),

("B12 recht DE",
 "CanG April 2024: 25g/50g/3 Pflanzen (18+). Social Clubs. THC Strassenverkehr: 3.5 ng/ml.",
 "Seit dem Cannabisgesetz (CanG) vom April 2024 sind für Erwachsene ab 18 Jahren 25 g unterwegs, 50 g zu Hause und 3 Pflanzen erlaubt. Anbauvereinigungen (Social Clubs) sind zulässig. Im Strassenverkehr gilt ein THC-Grenzwert von 3,5 ng/ml."),

("B12 recht AT",
 "Illegal (SMG). Eigenkonsum: Diversion möglich. CBD unter 0.3% legal.",
 "Cannabis ist nach dem Suchtmittelgesetz (SMG) illegal. Beim Eigenkonsum ist statt einer Strafe eine Diversion möglich — ein Verfahren mit Auflagen statt Verurteilung. CBD mit weniger als 0,3 % THC ist legal."),

("B12 recht Hinweis",
 "<b style=\"color:var(--amber)\">Keine Rechtsberatung.</b> Stand Mitte 2025. Lokal prüfen.",
 "<b style=\"color:var(--amber)\">Dies ist keine Rechtsberatung.</b> Stand: Mitte 2025 — bitte die aktuelle Rechtslage vor Ort prüfen."),

("B12 anlaufstellen DE CanG",
 "CanG (2024): 25g/50g/3 Pflanzen (18+).",
 "Seit dem CanG (2024): 25 g unterwegs, 50 g zu Hause, 3 Pflanzen — erlaubt ab 18 Jahren."),

("B13 calc sublingual",
 "Onset: <b>15–45 Min</b>. Lösung mindestens 60–90 Sek unter der Zunge halten.",
 "Der Wirkungseintritt liegt bei <b>15–45 Minuten</b>. Halte die Lösung mindestens 60–90 Sekunden unter der Zunge."),
]

# ─────────────────────────────────────────────────────────────────────────
# TEIL D — Beispielsatz + Edibles-Komma
# ─────────────────────────────────────────────────────────────────────────
REPL += [
("D1 calc Oral/Edibles",
 "Die mg-Zahl hier ist nicht gleich wie beim Rauchen. THC wird in der Leber zu <b>11-Hydroxy-THC</b> umgewandelt — wirkt stärker und länger als inhaliertes THC. Wirkungseintritt: <b>30–120 Min</b>. Nichts nachnehmen bevor die Wirkung spürbar ist.",
 "Die mg-Zahl ist hier nicht dasselbe wie beim Rauchen. THC wird in der Leber zu <b>11-Hydroxy-THC</b> umgewandelt — es wirkt stärker und länger als inhaliertes THC. Der Wirkungseintritt liegt bei <b>30–120 Minuten</b>. Nimm nichts nach, bevor die Wirkung spürbar ist oder bevor 120 Minuten vergangen sind."),

("D2 Edibles lexikon Komma",
 "<b>Grösste Gefahr:</b> Nachdosieren bevor die Wirkung spürbar ist. Regel: mit 2,5–5 mg THC starten, mindestens 2 Stunden warten.",
 "<b>Grösste Gefahr:</b> Nachdosieren, bevor die Wirkung spürbar ist — oder bevor mindestens 2 Stunden vergangen sind. Regel: mit 2,5–5 mg THC starten und mindestens 2 Stunden warten."),
]

# ─────────────────────────────────────────────────────────────────────────
# TEIL C — Wizard-Schritte (W) ausformuliert
# ─────────────────────────────────────────────────────────────────────────
REPL += [
# --- butter ---
("C butter Dekarb",
 "110–120°C, 30–45 Min. Dünn auf Backpapier, halbzeit wenden.",
 "Bei 110–120 °C für 30–45 Minuten. Das Material dünn auf Backpapier verteilen und zur Halbzeit einmal wenden."),
("C butter Fett",
 "1g Material auf 10–20g Fett. Kokosöl: höchste Bindung. Ghee: kein Wasser. Kokosfett: neutral.",
 "1 g Material auf 10–20 g Fett. Kokosöl bindet am besten, Ghee enthält kein Wasser, Kokosfett ist geschmacksneutral."),
("C butter Infusion",
 "65–75°C, mind. 2–4h. Slow Cooker Low ideal.",
 "Bei 65–75 °C mindestens 2–4 Stunden ziehen lassen. Ein Slow Cooker auf Stufe „Low“ ist dafür ideal."),
("C butter Filtern",
 "Doppelt Musselintuch. Rückstand ausdrücken. Nur Glas oder Edelstahl!",
 "Durch ein doppelt gelegtes Musselintuch filtern und den Rückstand gut ausdrücken. Nur Glas oder Edelstahl verwenden!"),
("C butter Kuehlen",
 "2h kühlen, Wasser abgiessen, beschriften.",
 "2 Stunden kühlen, das Wasser abgiessen und den Behälter beschriften."),
# --- mct ---
("C mct Dekarb+tip",
 "110–120°C, 30–45 Min.',tip:'Mason Jar: weniger Geruch.",
 "Bei 110–120 °C für 30–45 Minuten.',tip:'Im Mason Jar entsteht weniger Geruch."),
("C mct Infusion",
 "60–70°C, 2–3h. Magnetrührer empfohlen.",
 "Bei 60–70 °C für 2–3 Stunden. Ein Magnetrührer wird empfohlen."),
("C mct Filtern",
 "Musselintuch filtern. 5–10% Lecithin bei 50°C einrühren. Nur Glas/Edelstahl!",
 "Durch ein Musselintuch filtern. Anschliessend 5–10 % Lecithin bei 50 °C einrühren. Nur Glas oder Edelstahl verwenden!"),
("C mct Lagern",
 "Dunkle Flaschen, kühl. 6–12 Monate.",
 "In dunklen Flaschen kühl lagern — 6–12 Monate haltbar."),
# --- glycerin (Dekarb via Paar mit Warmextraktion) ---
("C glycerin Dekarb",
 "b:'110–120°C, 30–45 Min.',timer:2400}",
 "b:'Bei 110–120 °C für 30–45 Minuten.',timer:2400}"),
("C glycerin Warm",
 "Wasserbad 70–75°C, 4–8h, täglich schütteln.',warn:'Nicht über 80°C.",
 "Im Wasserbad bei 70–75 °C für 4–8 Stunden, täglich schütteln.',warn:'Nicht über 80 °C erhitzen."),
("C glycerin Filtern",
 "Warm filtern (50°C). Nur Glas/Edelstahl!",
 "Warm bei 50 °C filtern. Nur Glas oder Edelstahl!"),
# --- lecithin ---
("C lecithin Basis",
 "Fertige Öl-Infusion + 5–10% Sonnenblumen-Lecithin.",
 "Zur fertigen Öl-Infusion 5–10 % Sonnenblumen-Lecithin geben."),
("C lecithin Emulgieren",
 "50°C, Stabmixer mind. 2 Min.',tip:'Ultraschallbad 3–5 Min.",
 "Bei 50 °C mit dem Stabmixer mindestens 2 Minuten mixen.',tip:'Alternativ 3–5 Minuten ins Ultraschallbad."),
("C lecithin Freeze",
 "8h einfrieren, auftauen. 2–3 Zyklen.',tip:'Erhöht Bioverfügbarkeit nachweislich.",
 "8 Stunden einfrieren, wieder auftauen — 2–3 Zyklen wiederholen.',tip:'Das erhöht die Bioverfügbarkeit nachweislich."),
("C lecithin Lagern",
 "Kühlschrank, dunkel. 4–8 Wochen.",
 "Im Kühlschrank dunkel lagern — 4–8 Wochen haltbar."),
# --- tinktur ---
("C tinktur Vorb",
 "Ethanol 95%+ und Material auf –22°C einfrieren.',warn:'Nur Ethanol Lebensmittelqualität! Niemals Isopropanol.",
 "Ethanol (95 % oder mehr) und Material auf –22 °C einfrieren.',warn:'Nur Ethanol in Lebensmittelqualität verwenden! Niemals Isopropanol."),
("C tinktur QWET",
 "Max. 3 Min Kontaktzeit bei –22°C. Bei –22°C flocken Wachse effektiv aus. Sofort filtern.',tip:'–22°C ist der Praxis-Richtwert für sichtbares Ausfallen — unter –18°C kaum beobachtbar.",
 "Maximal 3 Minuten Kontaktzeit bei –22 °C — bei dieser Temperatur flocken die Wachse effektiv aus. Sofort filtern.',tip:'–22 °C ist der Praxis-Richtwert für sichtbares Ausflocken — unter –18 °C ist es kaum zu beobachten."),
("C tinktur Feinfiltern",
 "Kaffeefilter, zweimal. Nur Glas-Auffanggefäss — kein Plastik, kein Silikon bei Lösungsmitteln!',warn:'Silikon und Plastik können bei org. Lösungsmitteln Moleküle abgeben.",
 "Zweimal durch einen Kaffeefilter filtern. Nur ein Auffanggefäss aus Glas verwenden — bei Lösungsmitteln weder Plastik noch Silikon!',warn:'Silikon und Plastik können bei organischen Lösungsmitteln Moleküle abgeben."),
("C tinktur Reduzieren",
 "Wasserbad max. 70°C. Gut belüfteter Raum.",
 "Im Wasserbad bei maximal 70 °C reduzieren, in einem gut belüfteten Raum."),
("C tinktur Lagern",
 "Dunkle Tropfflaschen, kühl. 12+ Monate.",
 "In dunklen Tropfflaschen kühl lagern — über 12 Monate haltbar."),
# --- feco ---
("C feco Was",
 "Vollspektrum-Kaltextrakt + Winterization. Reineres Produkt als RSO. Alle Cannabinoide + Terpene, ohne schwere Wachse.',tip:'FECO ist die verfeinerte Version von RSO.',warn:'Hochpotent — Startdosis Reiskorn (~5mg)!",
 "Ein Vollspektrum-Kaltextrakt mit anschliessender Winterization — reiner als RSO. Er enthält alle Cannabinoide und Terpene, aber keine schweren Wachse.',tip:'FECO ist die verfeinerte Version von RSO.',warn:'Sehr hochpotent — als Startdosis eine reiskorngrosse Menge (~5 mg)!"),
("C feco Dekarb",
 "b:'110–115°C, 45 Min.',timer:2700",
 "b:'Bei 110–115 °C für 45 Minuten.',timer:2700"),
("C feco Kalt",
 "Material und Ethanol auf –22°C. 3–5 Min rühren. Sofort filtern.',warn:'Nur Ethanol Lebensmittelqualität! Nur Glas/Edelstahl.",
 "Material und Ethanol auf –22 °C bringen, 3–5 Minuten rühren und sofort filtern.',warn:'Nur Ethanol in Lebensmittelqualität! Nur Glas oder Edelstahl."),
("C feco Winter",
 "24–48h bei –20°C. Wachse flocken aus. Kaffeefilter.',tip:'Winterization = Schlüsselschritt FECO vs. RSO.",
 "24–48 Stunden bei –20 °C: Die Wachse flocken aus. Anschliessend durch einen Kaffeefilter geben.',tip:'Die Winterization ist der entscheidende Schritt, der FECO von RSO unterscheidet."),
("C feco Reduzieren",
 "Wasserbad max. 70°C. Schonend — Terpene erhalten.",
 "Im Wasserbad bei maximal 70 °C schonend reduzieren, damit die Terpene erhalten bleiben."),
("C feco Dosierung",
 "Sublingual: 1–2 Tropfen (~2.5–5mg). Kapseln: FECO + MCT 1:10. Edibles: direkt einarbeiten.',warn:'Onset sublingual: 15–45 Min. Abwarten!",
 "Sublingual: 1–2 Tropfen (~2,5–5 mg). Für Kapseln FECO und MCT im Verhältnis 1:10 mischen. In Edibles direkt einarbeiten.',warn:'Wirkungseintritt sublingual: 15–45 Minuten — unbedingt abwarten!"),
("C feco Lagern",
 "Kühlschrank: 12–18 Mon. Tiefkühl: 3 Jahre.",
 "Im Kühlschrank 12–18 Monate haltbar, tiefgekühlt bis zu 3 Jahre."),
# --- rosin ---
("C rosin Ueberblick",
 "Lösungsmittelfrei — Hitze + Druck. Hitzepresse ab ~200€, Rosin-Bags (25–220 Mikron), Pergaminpapier, Edelstahl-Tool.\\n\\nTypen: Flower Rosin, Hash Rosin, Live Rosin (frisch gefroren), Fresh Press.',tip:'Haarglätter + C-Klemmen für kleine Mengen.",
 "Lösungsmittelfrei — nur mit Hitze und Druck. Du brauchst eine Hitzepresse (ab ~200 €), Rosin-Bags (25–220 Mikron), Pergaminpapier und ein Edelstahl-Werkzeug.\\n\\nTypen: Flower Rosin, Hash Rosin, Live Rosin (aus frisch gefrorenem Material) und Fresh Press.',tip:'Für kleine Mengen genügen ein Haarglätter und C-Klemmen."),
("C rosin Ausgang",
 "Flower Rosin: 55–62% Feuchte. In Bag (115–160 Mikron) füllen, max. 60–70%.\\nLive Rosin: direkt nach Ernte einfrieren, kein Trocknen.",
 "Flower Rosin: 55–62 % Restfeuchte. In einen Bag (115–160 Mikron) füllen, aber nur zu 60–70 %.\\nLive Rosin: direkt nach der Ernte einfrieren, nicht trocknen."),
("C rosin Temp",
 "55–65°C: Live Rosin — max. Terpene, flüssig.\\n75–85°C: Hash Rosin — Balance.\\n90–105°C: Flower Rosin — höchste Ausbeute.',tip:'Niedrigere Temp = mehr Terpene = besser für Edibles.",
 "55–65 °C: Live Rosin — maximale Terpene, flüssige Konsistenz.\\n75–85 °C: Hash Rosin — ausgewogen.\\n90–105 °C: Flower Rosin — höchste Ausbeute.',tip:'Eine niedrigere Temperatur bedeutet mehr Terpene und ist besser für Edibles."),
("C rosin Pressen",
 "Pergamin um Bag. Langsam Druck aufbauen. 45–90 Sek. Rosin mit Edelstahl-Tool abschaben.",
 "Den Bag in Pergaminpapier einschlagen, langsam Druck aufbauen und 45–90 Sekunden pressen. Das Rosin anschliessend mit dem Edelstahl-Werkzeug abschaben."),
("C rosin DekarbEdibles",
 "Option A: Material vorher dekarboxylieren (110°C, 30 Min).\\nOption B: Rosin nach dem Pressen bei 110°C, 20–30 Min.\\nOption C: Rosin in heisses Öl (110°C) geben, 20 Min — Dekarb + Infusion in einem Schritt.',tip:'Option C am effizientesten.",
 "Option A: Das Material vorher dekarboxylieren (110 °C, 30 Minuten).\\nOption B: Das Rosin nach dem Pressen bei 110 °C für 20–30 Minuten dekarboxylieren.\\nOption C: Das Rosin in heisses Öl (110 °C) geben und 20 Minuten erhitzen — Dekarboxylierung und Infusion in einem Schritt.',tip:'Option C ist am effizientesten."),
("C rosin Lagern",
 "Kühlschrank oder Tiefkühl in Silikonbehälter (nach dem Pressen ist Silikon ok). 3–6 Monate.',tip:'Kurz anwärmen vor der Verarbeitung.",
 "Im Kühlschrank oder tiefgekühlt in einem Silikonbehälter aufbewahren (nach dem Pressen ist Silikon unbedenklich) — 3–6 Monate haltbar.',tip:'Vor der Verarbeitung kurz anwärmen."),
# --- hard_candy ---
("C hc Ausgang",
 "MCT-Öl oder reduzierte Tinktur (kein Restalkohol).',warn:'Wasser in der Masse: trüb, klebrig.",
 "MCT-Öl oder reduzierte Tinktur verwenden (ohne Restalkohol).',warn:'Wasser in der Masse macht die Bonbons trüb und klebrig."),
("C hc Zucker",
 "Zucker + Glukosesirup + Wasser (3:2:1). 150–160°C. Nicht rühren!',warn:'Über 160°C: Karamellisierung.",
 "Zucker, Glukosesirup und Wasser im Verhältnis 3:2:1 auf 150–160 °C kochen. Dabei nicht rühren!',warn:'Über 160 °C beginnt die Karamellisierung."),
("C hc Wirkstoff",
 "Auf ~120°C abkühlen. Öl + Lecithin einrühren.',warn:'Immer unter 130°C!",
 "Auf ~120 °C abkühlen lassen, dann Öl und Lecithin einrühren.',warn:'Immer unter 130 °C bleiben!"),
("C hc Formen",
 "Zügig giessen. 30 Min abkühlen. Sofort einwickeln.',warn:'Nicht im Kühlschrank kühlen.",
 "Zügig in die Formen giessen, 30 Minuten abkühlen lassen und sofort einwickeln.',warn:'Nicht im Kühlschrank abkühlen lassen."),
# --- gummies ---
("C gum Gelatine",
 "Gelatine in Saft, erhitzen bis 70–75°C. Agar vegan.',tip:'10–15% Glycerin: weichere Textur.',warn:'Gelatine nie über 80°C.",
 "Gelatine in Saft einweichen und auf 70–75 °C erhitzen. Agar ist die vegane Alternative.',tip:'10–15 % Glycerin ergeben eine weichere Textur.',warn:'Gelatine nie über 80 °C erhitzen."),
("C gum Emulsion",
 "Öl + Lecithin (1:1) mit Stabmixer.',warn:'Ohne Emulgator: Hot Spots!",
 "Öl und Lecithin im Verhältnis 1:1 mit dem Stabmixer emulgieren.',warn:'Ohne Emulgator entstehen Hot Spots (Wirkstoff-Klumpen)!"),
("C gum Mischen",
 "Gelatine auf 60°C. Emulsion einrühren. Dosierflasche.",
 "Die Gelatine auf 60 °C bringen, die Emulsion einrühren und mit einer Dosierflasche in die Formen füllen."),
("C gum Kuehlen",
 "2h Kühlschrank. 12–24h trocknen.',tip:'Zitronensäure-Zucker gegen Zusammenkleben.",
 "2 Stunden in den Kühlschrank, danach 12–24 Stunden trocknen lassen.',tip:'Zitronensäure-Zucker verhindert das Zusammenkleben."),
# --- baked ---
("C baked Fett",
 "1:1 Ersatz. Unter 70°C einrühren. Nach Gewicht portionieren.',warn:'Max. 175°C. Hot Spots!",
 "Das Fett 1:1 ersetzen, unter 70 °C einrühren und nach Gewicht portionieren.',warn:'Maximal 175 °C — sonst drohen Hot Spots!"),
("C baked Backen",
 "160–175°C.',warn:'Über 180°C: Wirkstoffverlust.",
 "Bei 160–175 °C backen.',warn:'Über 180 °C geht Wirkstoff verloren."),
("C baked Lagern",
 "Einzeln einwickeln. Beschriften.',warn:'Nie offen — Verwechslungsgefahr!",
 "Jedes Stück einzeln einwickeln und beschriften.',warn:'Nie offen liegen lassen — Verwechslungsgefahr!"),
# --- kapseln ---
("C kaps Fuellmasse",
 "MCT + 5–10% Lecithin, 35–40°C. Grösse 00.",
 "MCT mit 5–10 % Lecithin bei 35–40 °C mischen. Kapselgrösse 00 verwenden."),
("C kaps Fuellen",
 "Pipette oder Füllbrett. Lekkage-Test 15 Min.",
 "Mit Pipette oder Füllbrett befüllen. Anschliessend 15 Minuten auf Leckagen prüfen."),
# --- exotic ---
("C exo Emulsion",
 "Öl + Lecithin emulgieren.',warn:'Ohne Emulgation: Hot Spots!",
 "Öl und Lecithin emulgieren.',warn:'Ohne Emulgierung entstehen Hot Spots!"),
("C exo Honig",
 "Honig: 40°C. Schokolade: 45°C→27°C→31–32°C.',warn:'Schokolade über 34°C: Temperierung verloren.",
 "Honig auf 40 °C erwärmen. Schokolade temperieren: 45 °C → 27 °C → 31–32 °C.',warn:'Über 34 °C verliert die Schokolade ihre Temperierung."),
("C exo Portionieren",
 "Einzelportionen in Silikonformen. Beschriften.",
 "In Einzelportionen in Silikonformen giessen und beschriften."),
# --- rso ---
("C rso Sicherheit",
 "Originales RSO wurde mit Naphtha hergestellt — für konsumierbares RSO ausschliesslich Ethanol 95%+ Lebensmittelqualität verwenden! Naphtha nur dokumentiert zu Wissenszwecken — toxische Rückstände möglich.",
 "Das originale RSO wurde mit Naphtha hergestellt — für konsumierbares RSO ausschliesslich Ethanol (95 % oder mehr) in Lebensmittelqualität verwenden! Naphtha ist hier nur zu Wissenszwecken dokumentiert, da toxische Rückstände möglich sind."),
("C rso Dekarb",
 "b:'110–115°C, 45 Min.',timer:2400",
 "b:'Bei 110–115 °C für 45 Minuten.',timer:2400"),
("C rso Warm",
 "Raumtemperatur, 3–4 Min rühren. Nur Glas/Edelstahl!',warn:'Ethanol 95%+, Lebensmittelqualität.",
 "Bei Raumtemperatur 3–4 Minuten rühren. Nur Glas oder Edelstahl!',warn:'Ethanol mit 95 % oder mehr, in Lebensmittelqualität."),
("C rso Filtern",
 "Musselintuch. Dann Rice Cooker max. 110°C.',warn:'Nur im Freien oder Absaugung. Keine Flamme!",
 "Durch ein Musselintuch filtern, dann im Rice Cooker bei maximal 110 °C reduzieren.',warn:'Nur im Freien oder mit Absaugung. Keine offene Flamme!"),
("C rso Finish",
 "Auf 70°C senken bis blasenfrei. Warm in 1ml Luerlock-Spritzen.',tip:'1ml ≈ 600–900mg RSO.",
 "Auf 70 °C senken, bis keine Blasen mehr aufsteigen. Warm in 1-ml-Luerlock-Spritzen abfüllen.',tip:'1 ml entspricht etwa 600–900 mg RSO."),
("C rso Dosierung",
 "Sublingual: Reiskorngrosse Menge (~5mg). Oral: auf Brot oder in Kapsel.',warn:'Sehr hochpotent. Immer abwarten!",
 "Sublingual: eine reiskorngrosse Menge (~5 mg). Oral: auf Brot streichen oder in eine Kapsel füllen.',warn:'Sehr hochpotent — immer abwarten!"),
# --- bho ---
("C bho Gefahr",
 "Closed-Loop-Anlage: 500€–5000€+. Vakuumofen: 300€–1500€. N-Butan 99.5%+.\\n\\nOpen-Blast ist lebensgefährlich und darf niemals angewendet werden!",
 "Closed-Loop-Anlage: 500–5000 € und mehr. Vakuumofen: 300–1500 €. N-Butan mit 99,5 % Reinheit oder höher.\\n\\nOpen-Blast ist lebensgefährlich und darf niemals angewendet werden!"),
("C bho Extraktion",
 "Material in Rohr. N-Butan durch Material drücken. Extrakt im Sammelkolben auffangen. Nur Glas/Edelstahl für alle Kontaktflächen mit Lösungsmittel!",
 "Das Material in das Rohr füllen und N-Butan hindurchdrücken. Den Extrakt im Sammelkolben auffangen. Für alle Flächen, die das Lösungsmittel berühren, nur Glas oder Edelstahl verwenden!"),
("C bho Vorpurging",
 "Extrakt bei 35–40°C auf Silikonmatte. Silikon erst nach dem Vorpurging verwenden — während Extraktion nur Edelstahl/Glas!',warn:'Butan-Dämpfe: aussen oder Abluft.",
 "Den Extrakt bei 35–40 °C auf eine Silikonmatte geben. Silikon erst ab dem Vorpurging verwenden — während der Extraktion nur Edelstahl oder Glas!',warn:'Butan-Dämpfe nur im Freien oder mit Abluft."),
("C bho Vakuum",
 "35–45°C, –29 inHg, 24–72h je nach Konsistenz.\\nShatter: niedrige Temp, wenig Rühren.\\nWax/Budder: höhere Temp + Rühren.',warn:'Feuerzeug-Test: kein Entzünden = fertig.",
 "Bei 35–45 °C und –29 inHg für 24–72 Stunden, je nach gewünschter Konsistenz.\\nShatter: niedrige Temperatur, wenig rühren.\\nWax/Budder: höhere Temperatur und rühren.',warn:'Feuerzeug-Test: Entzündet sich nichts mehr, ist es fertig."),
("C bho Typen",
 "Shatter: transparent, 70–90%.\\nWax/Budder: cremig, 65–85%.\\nCrumble: bröckelig, 60–80%.\\nSauce/HTFSE: flüssig, terpenreich, 50–70%.\\nLive Resin: aus gefrorenem Material, 60–85%.",
 "Shatter: transparent, 70–90 %.\\nWax/Budder: cremig, 65–85 %.\\nCrumble: bröckelig, 60–80 %.\\nSauce/HTFSE: flüssig und terpenreich, 50–70 %.\\nLive Resin: aus gefrorenem Material, 60–85 %."),
# --- thca ---
("C thca Grundlagen",
 "THCA-Kristalle bis 99% Reinheit. NICHT psychoaktiv ohne Dekarb! Für Edibles: Dekarb zwingend.\\n\\n3 Methoden:\\n1. Diamantmining (aus BHO-Sauce)\\n2. Heat Press / Rosin-Chips\\n3. Zentrifugen-Separation',warn:'THCA-Kristalle extrem potent. 0.01g = 10mg!",
 "THCA-Kristalle mit bis zu 99 % Reinheit. Ohne Dekarboxylierung sind sie NICHT psychoaktiv — für Edibles ist die Dekarboxylierung also zwingend.\\n\\nDrei Methoden:\\n1. Diamantmining (aus BHO-Sauce)\\n2. Heat Press / Rosin-Chips\\n3. Zentrifugen-Separation',warn:'THCA-Kristalle sind extrem potent: 0,01 g entsprechen bereits 10 mg!"),
("C thca Diamant",
 "Frischer BHO-Extrakt bei ~21°C in Glas. 1–3 Wochen kristallisieren lassen. Terp Sauce abgiessen.',tip:'Geduld. Temp konstant halten.',warn:'Druck kann entstehen — geschlossenes System!",
 "Frischen BHO-Extrakt bei ~21 °C in einem Glas 1–3 Wochen kristallisieren lassen, dann die Terp Sauce abgiessen.',tip:'Geduld haben und die Temperatur konstant halten.',warn:'Es kann Druck entstehen — nur im geschlossenen System!"),
("C thca Heat",
 "Rosin-Chips in Ethanol lösen, filtern, Lösungsmittel verdampfen. THCA kristallisiert beim Abkühlen.",
 "Rosin-Chips in Ethanol lösen, filtern und das Lösungsmittel verdampfen. Das THCA kristallisiert beim Abkühlen."),
("C thca Zentrifuge",
 "Extrakt auf 30–35°C erwärmen. 3000–5000 RPM, 10–15 Min. Terp Sauce trennt sich von THCA-Kristallen.',tip:'Zentrifuge ab ~200€.",
 "Den Extrakt auf 30–35 °C erwärmen und bei 3000–5000 U/min für 10–15 Minuten zentrifugieren. Die Terp Sauce trennt sich dabei von den THCA-Kristallen.',tip:'Eine Zentrifuge gibt es ab ~200 €."),
("C thca Dekarb",
 "120°C, 45–60 Min. Kristalle schmelzen — auf Silikonmatte oder in Glas.',warn:'Dekarb zwingend für Edibles!",
 "Bei 120 °C für 45–60 Minuten. Die Kristalle schmelzen dabei — auf einer Silikonmatte oder in einem Glas.',warn:'Für Edibles zwingend erforderlich!"),
("C thca Edibles",
 "Mit MCT + Lecithin bei 50°C auflösen. Dann wie normales Konzentrat. Kein Eigengeschmack.',tip:'1mg-Waage Pflicht!",
 "Mit MCT und Lecithin bei 50 °C auflösen, dann wie ein normales Konzentrat verwenden. Kein Eigengeschmack.',tip:'Eine Waage mit 1-mg-Genauigkeit ist Pflicht!"),
# --- vakuum ---
("C vak Aufwand",
 "Kurzwegdestillationsanlage: 500€–5000€+. Vakuumpumpe: 200€–800€. Heizbad: 200€–500€.\\nGesamtinvestition: ab ~1500€.",
 "Kurzwegdestillationsanlage: 500–5000 € und mehr. Vakuumpumpe: 200–800 €. Heizbad: 200–500 €.\\nGesamtinvestition: ab ~1500 €."),
("C vak Siedepunkte",
 "CBG: 120–140°C. THC: 155–175°C. CBD: 160–180°C. Terpene: unter 100°C.',tip:'Niedrigerer Druck = niedrigerer Siedepunkt.",
 "CBG: 120–140 °C. THC: 155–175 °C. CBD: 160–180 °C. Terpene: unter 100 °C.',tip:'Niedrigerer Druck bedeutet einen niedrigeren Siedepunkt."),
("C vak Vorb",
 "Winterisiertes FECO oder BHO. Dekarboxylieren. Restethanol vollständig entfernen.',warn:'Kein Restethanol — Druck im System!",
 "Winterisiertes FECO oder BHO verwenden, dekarboxylieren und das Restethanol vollständig entfernen.',warn:'Kein Restethanol — sonst entsteht Druck im System!"),
("C vak Destillation",
 "Fraktion 1 (80–120°C): Terpene — separat auffangen.\\nFraktion 2 (155–185°C): Cannabinoide — Hauptfraktion.',warn:'Temp langsam erhöhen.",
 "Fraktion 1 (80–120 °C): Terpene — separat auffangen.\\nFraktion 2 (155–185 °C): Cannabinoide — die Hauptfraktion.',warn:'Die Temperatur langsam erhöhen."),
("C vak Anwendung",
 "Sublingual: 1–2mg. Kapseln: MCT 1:10. Edibles: direkt, kein Eigengeschmack.',warn:'Startdosis: 1–2mg — potentestes Produkt!",
 "Sublingual: 1–2 mg. Für Kapseln mit MCT im Verhältnis 1:10 mischen. In Edibles direkt einarbeiten — kein Eigengeschmack.',warn:'Startdosis: 1–2 mg — das potenteste Produkt!"),
]

# ─────────────────────────────────────────────────────────────────────────
# TEIL C — Lexikon: Herstellung & Technik / Zutaten / Troubleshooting / Dekarb
# ─────────────────────────────────────────────────────────────────────────
REPL += [
("C lex Magnetruehrer",
 "Heizplatte mit Magnetrührer (~40€): konstante Temp, automatisches Rühren. 3h ohne Eingriff.",
 "Eine Heizplatte mit Magnetrührer (~40 €) hält die Temperatur konstant und rührt automatisch — bis zu 3 Stunden ohne Eingriff."),
("C lex FreezeThaw",
 "8h einfrieren, auftauen, wiederholen. 2–3 Zyklen. Erhöht Bioverfügbarkeit nachweislich.",
 "8 Stunden einfrieren, auftauen und wiederholen — 2–3 Zyklen. Das erhöht die Bioverfügbarkeit nachweislich."),
("C lex QWET",
 "Bei –22°C flocken Wachse und Lipide deutlich effektiver aus als bei –18°C. Unter –18°C kaum bis kein sichtbares Ausfallen. Tiefkühler auf Maximum oder Trockeneis verwenden.",
 "Bei –22 °C flocken Wachse und Lipide deutlich effektiver aus als bei –18 °C. Unter –18 °C ist kaum bis kein sichtbares Ausflocken zu beobachten. Den Tiefkühler auf Maximum stellen oder Trockeneis verwenden."),
("C lex TerpSauce",
 "Terpen-Fraktion aus Destillation oder Zentrifugation zum fertigen Destillat zurückführen → Vollspektrum-Produkt mit Entourage-Effekt.",
 "Die Terpen-Fraktion aus Destillation oder Zentrifugation zum fertigen Destillat zurückführen — so entsteht ein Vollspektrum-Produkt mit Entourage-Effekt."),
("C lex MCTvsKokos",
 "MCT immer flüssig: Kapseln, Tropfen. Kokosöl wird fest: Butter-Ersatz. MCT C8 schnellste Absorption ohne Gallensalze.",
 "MCT-Öl bleibt immer flüssig und eignet sich für Kapseln und Tropfen. Kokosöl wird fest und dient als Butter-Ersatz. MCT C8 wird am schnellsten aufgenommen, sogar ohne Gallensalze."),
("C lex Glycerin",
 "Vorteile: Alkoholfrei, süsslich. Nachteile: 40–60% der Ethanol-Ausbeute, sehr viskös.",
 "Vorteile: alkoholfrei und leicht süsslich. Nachteile: nur 40–60 % der Ethanol-Ausbeute und sehr zähflüssig."),
("C lex Ethanolstufen",
 "96% Lebensmittel: Standard. 99.9% anhydrous: reinste Extraktion. Niemals Isopropanol!",
 "96 % in Lebensmittelqualität ist der Standard. 99,9 % (wasserfrei, „anhydrous“) ergibt die reinste Extraktion. Niemals Isopropanol verwenden!"),
("C lex Ghee",
 "Butter langsam schmelzen bis Molke absinkt. Reines Butterfett abgiessen. Kein Wasseranteil: bessere Extraktion, länger haltbar.",
 "Butter langsam schmelzen, bis die Molke absinkt, dann das reine Butterfett abgiessen. Ohne Wasseranteil gelingt die Extraktion besser und das Ghee ist länger haltbar."),
("C lex Schoko",
 "Zartbitter: 50°C→28°C→32°C. Vollmilch: 45°C→27°C→30°C. Weiss: 40°C→26°C→28°C.",
 "Zartbitter: 50 °C → 28 °C → 32 °C. Vollmilch: 45 °C → 27 °C → 30 °C. Weiss: 40 °C → 26 °C → 28 °C."),
("C lex GummiesBloom",
 "Vollständige Emulgierung + langsames Abkühlen + 5–10% Glycerin.",
 "Vollständig emulgieren, langsam abkühlen lassen und 5–10 % Glycerin zugeben."),
("C lex KeinEffekt",
 "1) Dekarb fehlt. 2) Infusion zu heiss. 3) Onset abwarten (bis 2h!). 4) Fettigen Snack essen.",
 "Mögliche Ursachen: 1) Die Dekarboxylierung fehlt. 2) Die Infusion war zu heiss. 3) Der Wirkungseintritt (Onset) ist noch nicht erreicht — bis zu 2 Stunden abwarten. 4) Einen fettigen Snack essen, das verbessert die Aufnahme."),
("C lex HotSpots",
 "Emulgator fehlt, ungleichmässig gemischt. Immer Lecithin + Stabmixer + Waage.",
 "Der Wirkstoff ist ungleichmässig verteilt, weil ein Emulgator fehlt. Immer mit Lecithin, Stabmixer und Waage arbeiten."),
("C lex TruebeTinktur",
 "Kontaktzeit zu lang. Kürzer waschen, Aktivkohle, Winterization.",
 "Die Kontaktzeit war zu lang. Kürzer waschen, Aktivkohle einsetzen oder eine Winterization durchführen."),
("C lex KlebrigHC",
 "Zu wenig Glukosesirup. Sofort verpacken, Silica Gel.",
 "Zu wenig Glukosesirup. Die Bonbons sofort verpacken und Silica-Gel dazugeben."),
("C lex WarumDekarb",
 "THCA zu THC durch Hitze. Ohne Dekarb kaum Wirkung. Auch CBDA zu CBD. THCA-Kristalle besonders wichtig!",
 "Hitze wandelt THCA in THC um (und ebenso CBDA in CBD). Ohne Dekarboxylierung gibt es kaum Wirkung — bei THCA-Kristallen ist sie besonders wichtig!"),
("C lex DekarbTemp",
 "THC: 110°C / 30 Min. CBD: 120°C / 40 Min. THCA-Kristalle: 120°C / 45–60 Min. Terpene ab 100°C flüchtig.",
 "THC: 110 °C / 30 Minuten. CBD: 120 °C / 40 Minuten. THCA-Kristalle: 120 °C / 45–60 Minuten. Terpene werden ab 100 °C flüchtig."),
("C lex MasonJar",
 "Im verschlossenen Glas: weniger Geruch, Terpene kondensieren zurück. +10 Min.",
 "Im verschlossenen Glas entsteht weniger Geruch und die Terpene kondensieren zurück. Dafür 10 Minuten länger rechnen."),
("C lex SousVide",
 "Vakuumversiegelt, 93°C / 2h. Minimale Terpenverluste, kein Geruch.",
 "Vakuumversiegelt bei 93 °C für 2 Stunden. Minimale Terpenverluste und kein Geruch."),
("C lex Purging",
 "Entfernung von Restbutan im Vakuumofen. Temp + Zeit = Konsistenz.",
 "Entfernung von Restbutan im Vakuumofen. Temperatur und Zeit bestimmen die Konsistenz."),
("C lex ClosedLoop",
 "Geschlossenes BHO-System. Einzige sichere Methode. Open Blast = lebensgefährlich.",
 "Ein geschlossenes BHO-System — die einzige sichere Methode. Open Blast ist lebensgefährlich."),
("C lex DekarbEx",
 "THCA→THC, CBDA→CBD durch Hitze. Pflicht für alle Edibles.",
 "Hitze wandelt THCA in THC und CBDA in CBD um. Für alle Edibles Pflicht."),
("C lex Winterization",
 "Rohextrakt bei –20°C: Wachse flocken aus. Praktisch: Rohextrakt in –20°C Ethanol (10:1) 24–48h ansetzen — Ergebnis: klar, rein, weniger Eigengeschmack.",
 "Bei –20 °C flocken die Wachse aus dem Rohextrakt aus. Praktisch: den Rohextrakt in –20 °C kaltem Ethanol (10:1) 24–48 Stunden ansetzen — das Ergebnis ist klar, rein und hat weniger Eigengeschmack."),
]

# ═════════════════════════════════════════════════════════════════════════
def main():
    with io.open(TARGET, "r", encoding="utf-8") as f:
        content = f.read()
    applied, already, missing, ambiguous = [], [], [], []
    for pid, old, new in REPL:
        c = content.count(old)
        if c == 1:
            content = content.replace(old, new)
            applied.append(pid)
        elif c == 0:
            if content.count(new) >= 1:
                already.append(pid)
            else:
                missing.append(pid)
        else:
            ambiguous.append((pid, c))
    with io.open(TARGET, "w", encoding="utf-8") as f:
        f.write(content)
    print("APPLIED  (%d): %s" % (len(applied), ", ".join(applied)))
    print("ALREADY  (%d): %s" % (len(already), ", ".join(already)))
    print("MISSING  (%d): %s" % (len(missing), ", ".join(missing)))
    print("AMBIGUOUS(%d): %s" % (len(ambiguous), ", ".join("%s(%d)"%(a,b) for a,b in ambiguous)))
    if missing or ambiguous:
        print(">>> ACHTUNG: MISSING/AMBIGUOUS prüfen!")

if __name__ == "__main__":
    main()
