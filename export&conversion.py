import pdfplumber
import pandas as pd
import os
def exportdata(filename):
    name = str(filename)[:-4]
    with pdfplumber.open(filename) as pdf:
        data=[]
        for page_number in range(1, len(pdf.pages) + 1):
            table = pdf.pages[page_number - 1].extract_table()
            d= [row for row in table if any(row)]
            data.extend(d)
        df = pd.DataFrame(data)
    df.to_csv(f'{name}.csv',index=False,header=None)

def normalcsv(filepath):
    df = pd.read_csv(filepath, encoding='UTF-8')
    if 'H E L' in filepath:
        new_column_names=['Lp.','Nazwa','Stan','Zas. wyd. bil. Razem','Zas. wyd. bil. A+B','Zas. wyd. bil. C','Wydobycie']
    elif 'M E T A N  P O K Ł A D Ó W  W ĘG L A' in filepath:
        new_column_names=['Lp.','Nazwa','Stan','Zasoby wydobywalne bilansowe''Zasoby wydobywalne pozabilansowe','Zasoby przemyslowe','Emisja z wentylacja','Wydobycie']
    elif 'WĘGLE  KAMIENNE' in filepath:
        new_column_names=['Lp.','Nazwa','Stan','Zasoby geologiczne bilansowe Razem','Zasoby geologiczne bilansowe A+B+C1','Zasoby wydobywalne bilansowe C2+D','Zasoby przemyslowe','Wydobycie']
    elif 'SOLANKI, WODY LECZNICZE I TERMALNE' in filepath:
        new_column_names=['Lp.','Nazwa','Typ wody','Zasoby geologiczne bilansowe dyspozycyjne','Zasoby geologiczne bilansowe eksploatacyjne','Pobor','Powiat']
    elif "WODY PITNE I PRZEMYSŁOWE" in filepath:
        new_column_names=['Lp','Znak','Data','Nazwa','Powierzchnia','Modul']
    else:
        new_column_names=['Lp.','Nazwa','Stan','Zasoby wydobywalne bilansowe','Zasoby przemyslowe','Wydobycie','Powiat']
    difference=abs(len(df.columns)-len(new_column_names))
    if difference>0:
        new_column_names.extend('?')
    df.columns=new_column_names
    df=df.dropna()
    df.to_csv(filepath,index=False)


directory=os.listdir('C:\\Users\\DELL\\PycharmProjects\\parserpdf\\y2010')
filespdf=[file for file in directory if file.endswith('.pdf')]
for ffs in filespdf:
    fpath=f'C:\\Users\\DELL\\PycharmProjects\\parserpdf\\y2010\\{ffs}'
    exportdata(fpath)

filescsv=[file for file in directory if file.endswith('.csv')]
for filecsv in filescsv:
    fpath = f'C:\\Users\\DELL\\PycharmProjects\\parserpdf\\y2010\\{filecsv}'
    normalcsv(fpath)