#!/usr/bin/env python3
# Patch K: --warn/--warn-bg global aufgehellt (Kontrast ~4.9:1 -> ~6:1).
# Betrifft ALLE roten Warn-Elemente einheitlich: .adv-badge, Fehlerbox
# ("Ungueltige Eingabe"), .lex-tag.adv (z.B. "Edibles-Risiko"),
# dose-veryhigh Tag ("Sehr stark"), Sicherheitshinweise.
#
# Idempotent: prueft vor der Aenderung, ob der alte String noch vorhanden ist.

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0
total = 1

old1 = ":root{--bg:#111;--bg2:#1a1a1a;--bg3:#222;--border:#2a2a2a;--border2:#3a3a3a;--text:#e8e8e8;--text2:#aaa;--text3:#666;--accent:#52b788;--accent-bg:#0d2018;--warn:#e05252;--warn-bg:#1f0e0e;--amber:#d4a017;--amber-bg:#1f1500;--radius:8px;--radius-lg:12px;--fs:14px;--fs-sm:12px;--fs-xs:11px;--fs-lg:15px;--fs-xl:17px}"
new1 = ":root{--bg:#111;--bg2:#1a1a1a;--bg3:#222;--border:#2a2a2a;--border2:#3a3a3a;--text:#e8e8e8;--text2:#aaa;--text3:#666;--accent:#52b788;--accent-bg:#0d2018;--warn:#ff6b6b;--warn-bg:#2a1414;--amber:#d4a017;--amber-bg:#1f1500;--radius:8px;--radius-lg:12px;--fs:14px;--fs-sm:12px;--fs-xs:11px;--fs-lg:15px;--fs-xl:17px}"

if old1 not in content:
    print("WARNUNG 1: :root-Variablenzeile nicht (exakt) gefunden — evtl. seit letztem Patch verändert.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print(f"1/{total}: --warn: #e05252 -> #ff6b6b, --warn-bg: #1f0e0e -> #2a1414 (Kontrast ~4.9:1 -> ~6:1).")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/{total} Änderungen angewendet.")
if changes < total:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
