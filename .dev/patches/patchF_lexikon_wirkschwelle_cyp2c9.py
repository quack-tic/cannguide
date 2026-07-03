#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Patch F - Zwei Lexikon-Rohentwuerfe in Kategorie "Medizin & Pharmazie":
#   * "Wirkschwelle & Koerpergewicht"  (belegte orale Wirkschwelle vs. Startdosis)
#   * "CYP2C9 & individuelle Variabilitaet" (Metabolismus als eigentlicher Streufaktor)
# Beide als [ROHENTWURF - bitte pruefen]; Adrian schreibt final um.
import io

PATH = "index.html"
s = io.open(PATH, encoding="utf-8").read()

ANCHOR = "  medizin:{cat:'Medizin & Pharmazie',items:[\n"
ENTRIES = '    {t:\'Wirkschwelle & Körpergewicht\',b:\'<span class="lex-term">Wirkschwelle</span><span class="lex-tag med">Pharmazie</span><span class="lex-tag base">Dosierung</span><br>[ROHENTWURF – bitte prüfen] Für den Beginn einer spürbaren psychotropen Wirkung nennen medizinische Leitlinien bei oraler Gabe eine Schwelle von rund 0,2–0,3 mg THC pro kg Körpergewicht — bei einem Erwachsenen also etwa 10–15 mg (teils wird ein weiterer Bereich bis 0,2–3 mg/kg angegeben). Entscheidend: Das ist die <b>Wirkschwelle</b>, nicht die empfohlene Einstiegsdosis. Genau deshalb liegt die Einstiegsempfehlung im Rechner mit ~2,5 mg bewusst ein Vielfaches darunter — man tastet die Schwelle vorsichtig von unten an, statt sie direkt zu treffen. Trotz dieser gewichtsbezogenen Zahl raten dieselben Quellen von starren Dosis-Korrekturfaktoren nach Gewicht ausdrücklich ab: die individuelle Verträglichkeit schwankt so stark, dass „start low, go slow" — langsame Titration ab einer festen, tiefen Startdosis — verlässlicher ist als jede Umrechnung aufs Körpergewicht.\'},\n    {t:\'CYP2C9 & individuelle Variabilität\',b:\'<span class="lex-term">CYP2C9</span><span class="lex-tag med">Pharmazie</span><span class="lex-tag adv">Metabolismus</span><br>[ROHENTWURF – bitte prüfen] Warum dieselbe Dosis Menschen so unterschiedlich trifft, liegt weniger an Geschlecht oder Gewicht als am Leberstoffwechsel. Das Enzym <b>CYP2C9</b> ist wesentlich für den Abbau von THC (und CBD) zuständig. Bei oraler Aufnahme baut die Leber im ersten Durchgang (First-Pass) über 90 % des geschluckten THC ab, bevor es systemisch wirken kann — dabei entsteht das aktive, stärkere <b>11-Hydroxy-THC</b>. Wie schnell und vollständig das geschieht, ist von Person zu Person sehr verschieden [Umfang der genetischen CYP2C9-Varianten mit eigener Quelle prüfen — „langsame Metabolisierer" können deutlich höhere Wirkspiegel erreichen]. Hinzu kommt, dass Cannabinoide CYP2C9 und CYP3A4 teilweise selbst hemmen — das erklärt Wechselwirkungen mit anderen Medikamenten. Praktische Folge: Es gibt keine allgemeingültige „richtige" mg-Dosis; die individuelle Austestung ab einer tiefen Startdosis bleibt unersetzlich.\'},\n'

if "Wirkschwelle & K\u00f6rpergewicht" in s or "Wirkschwelle & Körpergewicht" in s:
    print("  [skip] Eintraege bereits vorhanden.")
elif ANCHOR in s:
    s = s.replace(ANCHOR, ANCHOR + ENTRIES, 1)
    io.open(PATH, "w", encoding="utf-8").write(s)
    print("  [ok]   2 Eintraege in medizin eingefuegt.")
    print("Patch F geschrieben.")
else:
    print("  [WARN] Anker 'medizin:{...}' nicht gefunden -> manuell pruefen.")
