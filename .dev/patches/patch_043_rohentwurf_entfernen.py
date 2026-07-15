#!/usr/bin/env python3
# Patch 043: Entfernt alle "[ROHENTWURF - bitte pruefen]"-Marker (beide
# Schreibweisen: normal und unicode-escaped) samt nachfolgendem Leerzeichen,
# damit der reine Inhaltstext ohne Draft-Kennzeichnung stehen bleibt.
#
# ACHTUNG (bewusst zur Kenntnis genommen): Diese Marker kennzeichneten Inhalte,
# die noch nicht persoenlich fachlich gegengeprueft wurden. Mit diesem Patch
# gelten sie als freigegeben.
#
# Idempotent: zaehlt Treffer vor und nach der Ersetzung.

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

before = len(re.findall(r'\[ROHENTWURF[^\]]*\]\s?', content))
content = re.sub(r'\[ROHENTWURF[^\]]*\]\s?', '', content)
after = len(re.findall(r'\[ROHENTWURF[^\]]*\]', content))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Gefundene Marker: {before}")
print(f"Entfernt: {before - after}")
print(f"Verbleibend: {after}")
if after == 0 and before > 0:
    print("\n✓ Alle ROHENTWURF-Marker entfernt.")
elif before == 0:
    print("\nKeine Marker gefunden — evtl. bereits entfernt.")
else:
    print("\nACHTUNG: nicht alle Marker entfernt — manuell prüfen!")
