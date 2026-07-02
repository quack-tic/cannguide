#!/usr/bin/env python3
"""
CannGuide — Prävention-Ausbau + Tinktur-Fix
Im Repo-Root ausführen: python3 patch_praev.py
Idempotent.
"""
import re, subprocess, sys, tempfile, os

src = open('index.html', encoding='utf-8').read()
changes = 0

# ── [0] GPL-Header-Bug (falls noch nicht gepatcht) ───────────────────────
broken = 'var html = \'<!DOCTYPE html><html lang="de">\n<!-- CannGuide \u00a9 2024-2026 quack-tic\n     Licensed under GNU GPL v3 \u2014 https://github.com/quack-tic/CannGuide --><head>'
fixed  = 'var html = \'<!DOCTYPE html><html lang="de"><head>'
if broken in src:
    src = src.replace(broken, fixed); changes += 1; print('\u2714 [0] GPL-Fix')
else:
    print('\u00b7 [0] GPL-Fix (bereits OK)')

# ── [1] Tinktur-Eintrag korrigieren ──────────────────────────────────────
OLD_TINK = '<span class="lex-term">Tinktur</span><span class="lex-tag base">Extrakt</span><br>Tinkturen sind Alkohol-basierte Cannabis-Extrakte zur sublingualen Einnahme. Onset sublingual: 15\u201345 Minuten. Bei Schlucken wirken sie wie Edibles \u2014 langsamerer Onset durch Leberpassage. <b>Wichtig:</b> Ausschliesslich Lebensmittelethanol (mind. 90%) verwenden \u2014 Isopropanol und technische Alkohole sind giftig.'

NEW_TINK = '<span class="lex-term">Tinktur</span><span class="lex-tag base">Lebensmittelauszug</span><br>Eine Tinktur ist ein Lebensmittelauszug: Cannabis wird in trinkf\u00e4higem Alkohol (z.B. Wodka 40\u202fVol.%, Rum) angesetzt \u2014 \u00e4hnlich wie kr\u00e4uterbasierte Hausmittel. Der Alkoholgehalt liegt im trinkf\u00e4higen Bereich und extrahiert Cannabinoide und Terpene schonend. Onset sublingual (unter die Zunge): 15\u201345 Minuten \u2014 schneller als Edibles, gut dosierbar. Bei Schlucken wirkt sie wie ein Edible (l\u00e4ngerer Onset durch Leberpassage). Hochprozentiger Laborethanol (\u226560\u202fVol.%) geh\u00f6rt zur Wirkstoffextraktion \u2014 das ist eine andere Kategorie.'

if OLD_TINK in src:
    src = src.replace(OLD_TINK, NEW_TINK); changes += 1; print('\u2714 [1] Tinktur korrigiert')
elif 'Lebensmittelauszug' in src:
    print('\u00b7 [1] Tinktur (bereits gepatcht)')
else:
    print('\u2718 [1] Tinktur-Muster nicht gefunden')

# ── [2] renderSafety: neue Tabs in desc ──────────────────────────────────
OLD_DESC = "var desc={dosierung:'Start Low, Lagerung, Risikogruppen.',od:'Zeichen erkennen, Erste Hilfe, Notruf.',sucht:'Fakten, Warnzeichen, Hilfe.',anlaufstellen:'Adressen & Hotlines DACH.',recht:'Rechtslage DACH.'};"
NEW_DESC = "var desc={dosierung:'Start Low, Lagerung, Risikogruppen.',bewusst:'Alter, T-Break, THC/CBD, Fahren.',lunge:'Inhalation, Vaporizer, Tabak.',kontrolle:'Reduktion, Konsummuster, Selbsttest.',od:'Zeichen erkennen, Erste Hilfe, Notruf.',sucht:'Fakten, Warnzeichen, Hilfe.',anlaufstellen:'Adressen & Hotlines DACH.',recht:'Rechtslage DACH.'};"

if OLD_DESC in src:
    src = src.replace(OLD_DESC, NEW_DESC); changes += 1; print('\u2714 [2] renderSafety: 3 neue Tabs')
elif 'bewusst:' in src and 'lunge:' in src:
    print('\u00b7 [2] renderSafety (bereits gepatcht)')
else:
    print('\u2718 [2] renderSafety-Muster nicht gefunden')

# ── [3] SAFETY: 3 neue Kategorien ────────────────────────────────────────
OLD_END = "    {t:'Wirkungsdauer',b:'Onset: 30\u2013120 Min. Peak: 2\u20134h. Dauer: 4\u20138h. Leerer Magen: schneller + st\u00e4rker.'}\n  ]},\n  od:"

NEW_BLOCK = """    {t:'Wirkungsdauer',b:'Onset: 30\u2013120 Min. Peak: 2\u20134h. Dauer: 4\u20138h. Leerer Magen: schneller + st\u00e4rker.'}
  ]},
  bewusst:{cat:'Bewusst konsumieren',icon:'\U0001f9e0',items:[
    {t:'Konsumalter',b:'Das Gehirn ist bis etwa Mitte 20 in voller Entwicklung \u2014 fr\u00fcher Einstieg erh\u00f6ht das Risiko f\u00fcr Abh\u00e4ngigkeit, Aufmerksamkeitsst\u00f6rungen und bleibende kognitive Einbu\u00dfen nachweislich. Das ist keine Moral, sondern Neurobiologie. Wer fr\u00fch beginnt, sollte das wissen.'},
    {t:'THC/CBD-Ratio',b:'Hochdosiges THC ohne CBD erh\u00f6ht das Psychoserisiko. CBD wirkt neuroprotektiv und kann die Intensit\u00e4t des Rausches d\u00e4mpfen. Schwarzmarktprodukte haben meist einen tiefen oder kaum vorhandenen CBD-Gehalt \u2014 ein bekanntes, aber untersch\u00e4tztes Risiko. Wer die Wahl hat: CBD-haltige Sorten bevorzugen oder CBD-Bl\u00fcten beimischen.'},
    {t:'Konsumpausen (T-Break)',b:'Regelm\u00e4ssige Pausen unterbrechen die Toleranzentwicklung, schonen das ECS und geben dem Gehirn Zeit zur Erholung. Schon 2\u20134 Wochen Abstinenz bauen die Toleranz messbar ab \u2014 was auch bedeutet: danach wirkt weniger mehr. Wer wei\u00df, dass er pausieren kann, konsumiert langfristig bewusster.'},
    {t:'Fahren & Cannabis',b:'Cannabis beeintr\u00e4chtigt Reaktionszeit, Aufmerksamkeit und Entscheidungsf\u00e4higkeit \u2014 auch wenn man sich subjektiv fit f\u00fchlt. In der Schweiz gilt THC-Nulltoleranz im Strassenverkehr; bei regelm\u00e4ssigem Konsum ist der Grenzwert nahezu st\u00e4ndig \u00fcberschritten. Faustregel: mind. 72h nach dem letzten Konsum warten, bevor man f\u00e4hrt.'},
    {t:'Mischkonsum',b:'Alkohol und Cannabis verst\u00e4rken sich gegenseitig \u2014 nicht additiv, sondern potenzierend. Der Effekt ist schwer vorherzusagen und h\u00e4ufig Ausl\u00f6ser f\u00fcr unangenehme Erfahrungen. Opioide, Benzodiazepine und andere Sedativa erh\u00f6hen das Risiko zus\u00e4tzlich. Medikamente: CYP450-Wechselwirkungen m\u00f6glich \u2014 Arzt oder Apotheke fragen.'},
    {t:'Set & Setting',b:'Wer man ist, wie man sich f\u00fchlt und wo man ist \u2014 das beeinflusst die Erfahrung mindestens genauso wie die Dosis. Stress, Angst, schlechte Stimmung oder fremde Umgebung k\u00f6nnen einen Konsum kippen. Positive Erfahrungen entstehen nicht durch Zufall: vertraute Menschen, sichere Umgebung, kein Druck.'}
  ]},
  lunge:{cat:'Konsum & Lunge',icon:'\U0001f4a8',items:[
    {t:'Verbrennung vs. Verdampfen',b:'Beim Rauchen (Joint, Bong) entstehen dieselben Verbrennungsprodukte wie beim Tabak: Benzol, Kohlenmonoxid, Teer, PAK. Vaporizer erhitzen auf 160\u2013220\u00b0C \u2014 unterhalb der Verbrennungstemperatur. Das Ergebnis ist Aerosol statt Rauch, mit deutlich weniger Schadstoffen. Studien zeigen reduzierte Atemwegssymptome bei Vaporer-Nutzern im Vergleich zu Rauchern.'},
    {t:'Vaporizer-Temperaturen',b:'170\u2013185\u00b0C: schonend, viele Terpene, leichtere Wirkung \u2014 gut f\u00fcr Einstieg und Tageskonsum. 185\u2013200\u00b0C: vollere Wirkung, mehr THC. 200\u2013220\u00b0C: maximale Extraktion, etwas mehr Abbauprodukte. \u00dcber 230\u00b0C beginnt Verbrennung. Medizinisch anerkannte Ger\u00e4te: Volcano Medic, Mighty Medic.'},
    {t:'Tabak-Mischkonsum',b:'Der Tabakzusatz im Joint wird h\u00e4ufig untersch\u00e4tzt: Nikotin ist k\u00f6rperlich abh\u00e4ngig machend und erh\u00f6ht das Suchtpotenzial des Mischkonsums erheblich. Reine Joints mit Aktivkohlefilter reduzieren den Schadstoffeintrag. Wer auf Tabak verzichten will: getrocknete Kr\u00e4uter als F\u00fcllmaterial \u2014 oder auf Vaporizer umsteigen.'},
    {t:'Tiefes Einatmen \u2014 der Mythos',b:'Tiefes Einatmen und langes Luftanhalten bringt kein zus\u00e4tzliches THC. Die Absorption in der Lunge ist nach 2\u20133 Sekunden abgeschlossen. Was l\u00e4nger gehalten wird, ist nur Rauch: mehr Kohlenmonoxid, mehr Teer, h\u00f6heres Risiko f\u00fcr Ohnmacht und Lungenverletzungen. Normales Ein- und Ausatmen gen\u00fcgt vollst\u00e4ndig.'},
    {t:'Dabbing',b:'Konzentrierte Extrakte auf heisser Nail liefern extrem hohe THC-Dosen in einem Atemzug. \u00dcber 450\u00b0C entstehen zus\u00e4tzlich Benzol und Karzinogene aus Terpenen. F\u00fcr Menschen ohne hohe Toleranz: starkes Greening-Out-Risiko bis hin zu Bewusstlosigkeit. Wer Dabs konsumiert: Temperaturkontrolle (E-Nail), niedrige Temperaturen, kleine Mengen.'},
    {t:'Langzeitkonsum & Atemwege',b:'T\u00e4gliches Rauchen \u00fcber Jahre ist mit Bronchitis-Symptomen, Husten und erh\u00f6hter Atemwegsinfektanf\u00e4lligkeit verbunden. Wer langfristig konsumieren m\u00f6chte und die Lunge schonen will: Vaporizer ist die evidenzbasiert risikoreduzierte Alternative zu Rauch.'}
  ]},
  kontrolle:{cat:'Kontrolle behalten',icon:'\u2696\ufe0f',items:[
    {t:'Eigenen Konsum einsch\u00e4tzen',b:'Drei Fragen: Kann ich problemlos eine Woche pausieren? Konsumiere ich auch wenn ich eigentlich nicht wollte? Hat der Konsum negative Folgen die ich ignoriere? \u2014 Wer bei einer oder mehreren Fragen z\u00f6gert, lohnt ein ehrlicherer Blick. CUDIT-Selbsttest: kostenlos online, anonym, 5 Minuten.'},
    {t:'Was wirklich hilft',b:'Aus der Beratungspraxis (DIZ Z\u00fcrich, n=166): CBD beimischen oder solo konsumieren. Kleinere Mengen kaufen und damit auskommen. Konsum auf bestimmte Tage begrenzen. Das Umfeld \u00fcber die Absicht zur Reduktion informieren. Ersatzhandlungen finden die auch Freude bereiten. Eine l\u00e4ngere Pause einlegen \u2014 ohne \\"nie mehr\\" zu sagen.'},
    {t:'Konsumpause (T-Break)',b:'2\u20134 Wochen reichen, um die Toleranz messbar zu senken. In dieser Zeit: lebendigere Tr\u00e4ume (THC unterdr\u00fcckt REM-Schlaf), m\u00f6gliche Reizbarkeit und Schlafprobleme in der ersten Woche \u2014 das sind normale Entzugszeichen, kein Zeichen von Schw\u00e4che. Nach der Pause: mit deutlich kleinerer Dosis neu einsteigen.'},
    {t:'Warnzeichen ernst nehmen',b:'Konsum trotz negativer Folgen (Job, Beziehung, Gesundheit). Stimmungstiefs und Reizbarkeit ohne Konsum. Steigende Dosen f\u00fcr denselben Effekt. Gedanken drehen sich haupts\u00e4chlich um den n\u00e4chsten Konsum. \u2014 Keines davon bedeutet Versagen. Es bedeutet, dass Unterst\u00fctzung sinnvoll ist \u2014 und sie wirkt nachweislich.'},
    {t:'Hilfe holen',b:'Kognitive Verhaltenstherapie (CBT) ist bei CUD evidenzbasiert wirksam. Quit the Shit: quittheshit.net \u2014 kostenlos, anonym, ohne Anmeldung. Suchtberatung ist vertraulich \u2014 kein Strafverfolgungsrisiko. Es braucht keine Abh\u00e4ngigkeitsdiagnose f\u00fcr Beratung; wer unsicher ist, ist willkommen.'}
  ]},
  od:"""

if OLD_END in src:
    src = src.replace(OLD_END, NEW_BLOCK)
    changes += 1; print('\u2714 [3] SAFETY: 3 neue Kategorien eingef\u00fcgt')
elif 'bewusst:{cat:' in src:
    print('\u00b7 [3] SAFETY neue Kategorien (bereits vorhanden)')
else:
    print('\u2718 [3] SAFETY-Ende-Muster nicht gefunden')

# ── Speichern & Syntax-Check ─────────────────────────────────────────────
print(f'\n{changes}/3 \u00c4nderungen (+ ggf. [0] GPL).')
open('index.html', 'w', encoding='utf-8').write(src)

scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', src, re.DOTALL)
for i, s in enumerate(scripts):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(s); tmp = f.name
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode == 0:
        print(f'\u2714 Script-Block {i}: Syntax OK')
    else:
        m2 = re.search(r':(\d+)\n', r.stderr)
        ln = int(m2.group(1)) if m2 else '?'
        lines = s.split('\n')
        errl = repr(lines[int(ln)-1][:100]) if isinstance(ln, int) else ''
        print(f'\u2718 Script-Block {i}, Zeile {ln}: {errl}')
        sys.exit(1)

print('\n\u2705 Fertig \u2014 git add index.html && git commit -m "Pr\u00e4vention ausgebaut: Bewusst/Lunge/Kontrolle + Tinktur-Fix" && git push')
