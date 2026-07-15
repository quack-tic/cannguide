#!/usr/bin/env python3
# Patch 050: Der bisherige einzelne "Live Resin"-Lexikoneintrag (nur BHO)
# wird durch 4 Eintraege ersetzt: ein Grundprinzip-Eintrag (inkl. der
# Zusatzinfo zum erhoehten Terpenanteil, 5-15%) plus die 3 spezifischen
# Herstellungsvarianten, die bereits als Rechner-Optionen existieren
# (Patch 049) -- BHO, Live Rosin/Bubble Hash, Live Dry Sift.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """{t:'Live Resin',b:'<span class="lex-term">Live Resin</span><span class="lex-tag conc">BHO</span><br>BHO aus frisch gefrorenem Material. Maximale Terpene.'},"""

new1 = """{t:'Live Resin (Grundprinzip)',b:'<span class="lex-term">Live Resin</span><span class="lex-tag conc">Konzept</span><br>"Live" bezeichnet die Verwendung von frisch geerntetem, sofort schockgefrorenem Pflanzenmaterial statt getrocknetem/kuriertem Ausgangsmaterial. Dadurch bleiben deutlich mehr Terpene erhalten — oft 5–15% Terpenanteil im fertigen Extrakt, statt der geringeren Menge bei Standardware. Das drückt den relativen THC-Wert gegenüber komplett isolierten Produkten (Shatter, Destillat) leicht nach unten, sorgt aber für ein intensiveres, authentischeres Aroma- und Geschmackserlebnis (Entourage-Effekt). Je nach Extraktionsmethode entstehen unterschiedliche Live-Produkte mit sehr unterschiedlicher Potenz — siehe die einzelnen Varianten unten.'},
    {t:'Live Resin – BHO',b:'<span class="lex-term">Live Resin (BHO)</span><span class="lex-tag conc">BHO</span><span class="lex-tag adv">Fortgeschritten</span><br>Butan-Extraktion aus frisch gefrorenem Material — gilt unter erfahrenen Extrakteuren als eine der anspruchsvollsten BHO-Disziplinen. Typische Potenz: 65–85% THC. Bilden sich dabei THCA-Diamonds (Kristalle in terpenreicher Sauce), kann der isolierte Diamond-Anteil bis an die 90%-Marke reichen — der hohe Terpenanteil bleibt dabei der umgebenden Sauce vorbehalten.'},
    {t:'Live Rosin / Live Bubble Hash',b:'<span class="lex-term">Live Rosin</span><span class="lex-tag conc">Lösungsmittelfrei</span><br>Eiswasser-Extraktion (Bubble Hash) aus frisch gefrorenem Material, bei der gezielt nur die Trichomköpfe (meist 73–159 Mikron) isoliert werden — das ergibt "Full-Melt"-Qualität. Wird dieses Eishasch anschliessend unter Druck und leichter Hitze gepresst (Pflanzenwachse bleiben im Filtertuch zurück), entsteht Live Rosin mit typischerweise 50–85% THC — hochwertige Premium-Chargen erreichen dabei ähnliche Potenzen wie BHO-Produkte, vollständig ohne Lösungsmittel.'},
    {t:'Live Dry Sift',b:'<span class="lex-term">Live Dry Sift</span><span class="lex-tag conc">Lösungsmittelfrei</span><br>Trockensieb-Verfahren (oft mit Trockeneis unterstützt) aus frisch gefrorenem Material, um Trichome mechanisch von Pflanzenmaterial zu trennen. Klassische Ware liegt bei 35–65% THC. Mit zusätzlicher Nachreinigung ("Static Tech" — statische Trennung von Trichomköpfen und Pflanzenresten) sind auch 70–80% erreichbar, das ist aber ein seltener, spezialisierter Veredelungsschritt.'},"""

if old1 not in content:
    print("WARNUNG 1: 'Live Resin'-Lexikoneintrag nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: 'Live Resin' auf 4 Einträge erweitert (Grundprinzip + BHO + Live Rosin + Live Dry Sift), inkl. Terpenanteil-Info.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
