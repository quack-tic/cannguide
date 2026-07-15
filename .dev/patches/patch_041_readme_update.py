#!/usr/bin/env python3
# Patch 041: readme.md aktualisiert -- veraltete Beschreibungen entfernt/korrigiert:
# - Inhalationsrechner existiert nicht mehr (entfernt)
# - Koerpergewicht/Geschlecht im Rechner existiert nicht mehr (entfernt)
# - Bibliothek: aufgeloeste Kategorien (Loesungsmittel/Profi-Tricks/Dekarb/
#   Troubleshooting als eigene Tabs) durch aktuelle Struktur ersetzt, neue
#   Kapitel (Wechselwirkungen, Vertiefungsartikel) ergaenzt
# - Onboarding-Tour: von "geplant" zu "umgesetzt" verschoben (ist jetzt fertig)
# - Einheiten-Umschalter im Rechner ergaenzt
#
# Idempotent: prueft vor jeder Aenderung, ob der alte String noch vorhanden ist.

with open('readme.md', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 4

# ─────────────────────────────────────────────────────────────────────────
# 1) Dosierungsrechner-Beschreibung aktualisieren
# ─────────────────────────────────────────────────────────────────────────
old1 = """### ∑ Dosierungsrechner
Körpergewicht, Toleranzstufen, Geschlecht und Metabolismus, Intensitätsbewertung, Plausibilitätsprüfung. Zwei Modi: Rohmaterial oder Extrakt. Weil der häufigste Fehler bei Edibles eine falsch eingeschätzte Dosis ist."""

new1 = """### ∑ Dosierungsrechner
Zwei Modi (Blüten oder Extrakt/Konzentrat), Einheiten-Umschalter (g/kg, ml/l), Toleranzstufen als Pflichtangabe, Intensitätsbewertung, Plausibilitätsprüfung, geführte Onboarding-Tour für Erstnutzer. Weil der häufigste Fehler bei Edibles eine falsch eingeschätzte Dosis ist."""

if old1 not in content:
    print("WARNUNG 1: Dosierungsrechner-Abschnitt nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Dosierungsrechner-Beschreibung aktualisiert (kein Inhalationsrechner/Körpergewicht mehr).")

# ─────────────────────────────────────────────────────────────────────────
# 2) Bibliothek & Lexikon-Beschreibung aktualisieren
# ─────────────────────────────────────────────────────────────────────────
old2 = """### ⊞ Bibliothek & Lexikon
Extraktionskunde, Lösungsmittelvergleich, Dekarboxylierungstabellen, Troubleshooting, Fachbegriffe. Weil ein gemeinsames Vokabular Voraussetzung für einen informierten Umgang ist."""

new2 = """### ⊞ Bibliothek & Lexikon
Extraktionskunde, Cannabinoide & Wirkstoffe, Wechselwirkungen mit Medikamenten, Vertiefungsartikel (pharmakologische Hintergründe mit Quellenangaben), Fachbegriffe. Weil ein gemeinsames Vokabular Voraussetzung für einen informierten Umgang ist."""

if old2 not in content:
    print("WARNUNG 2: Bibliothek-Abschnitt nicht (exakt) gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print(f"2/{total}: Bibliothek-Beschreibung um Wechselwirkungen & Vertiefungsartikel ergänzt.")

# ─────────────────────────────────────────────────────────────────────────
# 3) "Aktueller Stand" -- Umgesetzt-Liste aktualisieren
# ─────────────────────────────────────────────────────────────────────────
old3 = """### ✅ Umgesetzt
- Prävention mit Anlaufstellen, Rechtslage und Greening-Out-Protokoll für D(A)CH
- Vollständiger Dosierungsrechner inkl. Inhalationsrechner
- Prozess-Guide für alle Standard- und Fortgeschrittenen-Methoden
- Chargenverwaltung mit Charts, Vergleich und Export
- Bibliothek, Lexikon, Troubleshooting
- PWA (offline-fähig, installierbar auf Android & iOS)
- DE/EN Sprachumschalter (Basis)"""

new3 = """### ✅ Umgesetzt
- Prävention ("Know before you go") mit Anlaufstellen, Rechtslage und Greening-Out-Protokoll für D(A)CH
- Dosierungsrechner (Blüten/Extrakt) mit Einheiten-Umschalter (g/kg, ml/l) und Pflicht-Toleranzangabe
- Geführte Onboarding-Tour für Erstnutzer im Rechner
- Prozess-Guide für alle Standard- und Fortgeschrittenen-Methoden
- Chargenverwaltung mit Charts, Vergleich und Export
- Bibliothek, Lexikon inkl. Wechselwirkungen-Kapitel und Vertiefungsartikel
- PWA (offline-fähig, installierbar auf Android & iOS)
- DE/EN Sprachumschalter (Basis)"""

if old3 not in content:
    print("WARNUNG 3: 'Umgesetzt'-Liste nicht (exakt) gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print(f"3/{total}: 'Umgesetzt'-Liste aktualisiert.")

# ─────────────────────────────────────────────────────────────────────────
# 4) "In Arbeit / Geplant" -- Onboarding-Tour entfernen (ist fertig)
# ─────────────────────────────────────────────────────────────────────────
old4 = """### 🔧 In Arbeit / Geplant
- Lexikon: Erweiterung mit Inhalationsbegriffen
- Kosten & Zeitaufwand pro Methode
- Onboarding-Tour für Erstnutzer
- Play Store: TWA-Integration, Geo-Beschränkung CH + DE, Alterstor
- Community-Rezeptteilen (Phase 3)
- Vollständige DE/EN Übersetzung (Abschluss)"""

new4 = """### 🔧 In Arbeit / Geplant
- Kosten & Zeitaufwand pro Methode
- Play Store: TWA-Integration, Geo-Beschränkung CH + DE, Alterstor
- Community-Rezeptteilen (Phase 3)
- Vollständige DE/EN Übersetzung (Abschluss)"""

if old4 not in content:
    print("WARNUNG 4: 'In Arbeit / Geplant'-Liste nicht (exakt) gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print(f"4/{total}: Onboarding-Tour aus 'Geplant' entfernt (ist jetzt umgesetzt).")

with open('readme.md', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
