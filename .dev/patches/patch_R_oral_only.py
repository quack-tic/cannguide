#!/usr/bin/env python3
# Patch R: "Start Low, Go Slow" -- Inhalations-Dosisangabe entfernt, analog zur
# manuellen Anpassung der Praevention-Box. Fokus jetzt konsequent auf oralen Konsum.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = """    {t:'Start Low, Go Slow',b:'<b style="color:var(--accent)">Dos:</b><br>Erste Erfahrung: max. 1.5–2.5 mg THC inhalativ, 2.5–5 mg Edibles. Mind. 2 Stunden warten (Edibles) resp. 15 Min (Inhalation).<br><br><b style="color:var(--warn)">Don\\'ts:</b><br>Niemals nachkonsumieren weil nichts passiert.<br>Kein Mischkonsum mit Alkohol. Nicht Auto fahren. Nie bei Minderjährigen.'},"""

new1 = """    {t:'Start Low, Go Slow',b:'<b style="color:var(--accent)">Dos:</b><br>Erste Erfahrung: max. 2.5–5 mg THC (oral). Mindestens 2 Stunden warten, bevor nachdosiert wird.<br><br><b style="color:var(--warn)">Don\\'ts:</b><br>Niemals nachkonsumieren weil nichts passiert.<br>Kein Mischkonsum mit Alkohol. Nicht Auto fahren. Nie bei Minderjährigen.'},"""

if old1 not in content:
    print("WARNUNG 1: 'Start Low, Go Slow'-Eintrag nicht (exakt) gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: Inhalations-Dosisangabe entfernt, Eintrag fokussiert auf oralen Konsum.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht gefunden — manuell prüfen!")
