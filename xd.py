a=[{ 'name': 'Jedlinka', 'year': '2012', 'type': 'BARYT I FLUORYT', 'more': {'stan': 'Z', 'Zasoby wydobywalne bilansowe': '37', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'wałbrzyski'}}, { 'name': 'Jedlinka', 'year': '2012', 'type': 'BARYT I FLUORYT', 'more': {'stan': 'Z', 'Zasoby wydobywalne bilansowe': '37', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'wałbrzyski'}}]

headers2=list(a[0]["more"].keys())
print(headers2)
for items in a:
    print(items["more"][headers2[0]])



data=[(d["name"],d["year"],d["type"],d["more"][headers2[0]],d["more"][headers2[1]],d["more"][headers2[2]],d["more"][headers2[3]],d["more"][headers2[4]]) for d in a]
print(data)

for i in range(len(a)):
    row = (a[i]["name"], a[i]["more"][headers2[0]])
    print(row)