with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. parseDose-Helper einfügen + getDoseAmpel umstellen
old1 = """window.getDoseAmpel = function(dose) {
  dose = parseFloat(dose) || 0;"""
new1 = """function parseDose(v) {
  if(v===undefined || v===null) return 0;
  var n = parseFloat(String(v).replace(/[^0-9.,-]/g,'').replace(',','.'));
  return isNaN(n) ? 0 : n;
}

window.getDoseAmpel = function(dose) {
  dose = parseDose(dose);"""

if old1 not in content:
    print("WARNUNG 1: getDoseAmpel-Anfang nicht gefunden.")
else:
    content = content.replace(old1, new1)
    changes += 1
    print("1/4: parseDose-Helper eingefügt, getDoseAmpel umgestellt.")

# 2. Chart-Filter
old2 = "var doseData=sorted.filter(function(c){return parseFloat(c.dose)>0;});"
new2 = "var doseData=sorted.filter(function(c){return parseDose(c.dose)>0;});"
if old2 not in content:
    print("WARNUNG 2: doseData-Filter nicht gefunden.")
else:
    content = content.replace(old2, new2)
    changes += 1
    print("2/4: Chart-Filter umgestellt.")

# 3. Chart-Daten
old3 = "datasets:[{label:'mg/Portion',data:doseData.map(function(c){return parseFloat(c.dose)||0;}),"
new3 = "datasets:[{label:'mg/Portion',data:doseData.map(function(c){return parseDose(c.dose);}),"
if old3 not in content:
    print("WARNUNG 3: Chart-Datasets nicht gefunden.")
else:
    content = content.replace(old3, new3)
    changes += 1
    print("3/4: Chart-Daten umgestellt.")

# 4. Dashboard-Sichtbarkeit
old4 = "var hasDose=charges.some(function(c){return parseFloat(c.dose)>0;});"
new4 = "var hasDose=charges.some(function(c){return parseDose(c.dose)>0;});"
if old4 not in content:
    print("WARNUNG 4: hasDose-Check nicht gefunden.")
else:
    content = content.replace(old4, new4)
    changes += 1
    print("4/4: Dashboard-Sichtbarkeitsprüfung umgestellt.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n{changes}/4 Änderungen angewendet. Datei gespeichert.")
if changes < 4:
    print("ACHTUNG: nicht alle Stellen gefunden — manuell prüfen!")
  