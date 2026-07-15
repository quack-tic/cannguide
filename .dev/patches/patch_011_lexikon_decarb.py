#!/usr/bin/env python3
# Patch 6: Lexikon-Erweiterung Decarboxylierung (ROHENTWURF - Adrian ueberarbeitet Text).
# Fuegt zwei Eintraege am Anfang der Kategorie "konsum" ein.
import sys

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Anker: Beginn der items-Liste in der Kategorie konsum
anchor = "  konsum:{cat:'Konsum & Methoden',items:[\n"

entries = (
    "  konsum:{cat:'Konsum & Methoden',items:[\n"
    "    {t:'Decarboxylierung (Aktivierung)',b:'"
    "<span class=\\\"lex-term\\\">Decarboxylierung</span>"
    "<span class=\\\"lex-tag conc\\\">Grundlage</span>"
    "<span class=\\\"lex-tag adv\\\">Edibles-Pflicht</span><br>"
    "[ROHENTWURF \\u2013 bitte pruefen] Decarboxylierung ist der Erhitzungsschritt, "
    "der die saeurehaltige Vorstufe THCA in psychoaktives THC umwandelt (analog CBDA \\u2192 CBD). "
    "In der rohen Pflanze liegt der Wirkstoff fast vollstaendig als THCA vor \\u2013 roh gegessen "
    "berauscht Cannabis deshalb nicht. Beim Rauchen/Verdampfen geschieht die Aktivierung "
    "schlagartig durch die Hitze; fuer Edibles muss sie bewusst vorher erfolgen. "
    "<b>Richtwerte:</b> ca. 110\\u2013120\\u00b0C fuer 30\\u201345 Minuten (Werte je nach Quelle "
    "unterschiedlich \\u2013 hier deine eigenen Erfahrungswerte einsetzen). Zu heiss/zu lang baut "
    "THC wieder zu CBN ab (sedierend, schwaecher). <b>Massenverlust:</b> THCA verliert beim "
    "Abspalten der Carboxylgruppe CO\\u2082 \\u2013 aus der Masse THCA werden rund 87,7% THC "
    "(Molmassen 314,5 vs. 358,5 g/mol). Das erklaert, warum der Rechner bei Roh-Extrakten "
    "weniger aktives THC ausweist als der Rohgehalt vermuten laesst.'},\n"
    "    {t:'Decarb bei Extrakten & Konzentraten',b:'"
    "<span class=\\\"lex-term\\\">Decarb bei Extrakten</span>"
    "<span class=\\\"lex-tag adv\\\">Fortgeschritten</span><br>"
    "[ROHENTWURF \\u2013 bitte pruefen] Nicht jeder Extrakt ist gleich. "
    "<b>Bereits aktiv (decarboxyliert):</b> Destillat, FECO und meist RSO \\u2013 sie durchlaufen "
    "im Herstellungsprozess Hitze und koennen direkt in Edibles verwendet werden. "
    "<b>Roh (nicht decarboxyliert):</b> Rosin, Kief/Pollen, THCA-Kristalle und frisches BHO "
    "enthalten ueberwiegend THCA. Wer sie kalt in Butter oder Oel ruehrt, erhaelt ein "
    "kaum wirksames Edible \\u2013 und dosiert beim naechsten Versuch leicht zu hoch, weil "
    "das Produkt faelschlich als \\u201eschwach\\u201c eingeschaetzt wird. Roh-Extrakte "
    "deshalb vor der Verarbeitung decarboxylieren. Im Rechner den Schalter "
    "\\u201eBereits decarboxyliert?\\u201c korrekt setzen \\u2013 er beruecksichtigt den "
    "~12%-Massenverlust automatisch.'},\n"
)

if 'Decarboxylierung (Aktivierung)' in html:
    print('  [skip] 6: Decarb-Eintraege existieren bereits.')
elif anchor in html:
    html = html.replace(anchor, entries, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('  [ok]   6: Zwei Decarb-Lexikon-Eintraege eingefuegt (ROHENTWURF).')
else:
    sys.exit('  [FAIL] 6: konsum-Kategorie-Anker nicht gefunden.')
print('Patch 6 geschrieben.')
