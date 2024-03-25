import pymongo
import pandas as pd
import os

client=pymongo.MongoClient('mongodb+srv://<USERNAME>:<PASSWORD>@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority')# zmienic password i username na swoje
db=client['parser']
col=db['Kopalnie']
direc=os.listdir('D:\PyCharm\PyCharm 2023.2.4\parserpdf\year2012\csv')
filescsv=[file for file in direc if file.endswith('.csv')]
for files in filescsv:
    df=pd.read_csv(f'D:\PyCharm\PyCharm 2023.2.4\parserpdf\year2012\csv\{files}',encoding='UTF-8')
    type=files[:-9]
    year=files[-8:-4]
    for i in range(0,df.shape[0]):
        if 'H E L' in files:
            d={
                'Name':df.at[i,"Nazwa"],
                'Year':year,
                'Type':type,
                'More':{
                    'Stan':df.at[i,"Stan"],
                    'Zas. wyd. bil. Razem':df.at[i,'Zas. wyd. bil. Razem'],
                    'Zas. wyd. bil. A+B':df.at[i,'Zas. wyd. bil. A+B'],
                    'Zas. wyd. bil. C':df.at[i,'Zas. wyd. bil. C'],
                    'wydobycie':df.at[i,'Wydobycie']
                }
            }
        elif 'M E T A N  P O K Ł A D Ó W  W ĘG L A' in files:
            d = {
                'name': df.at[i, "Nazwa"],
                'year': year,
                'type': type,
                'more': {
                    'stan': df.at[i, "Stan"],
                    'Zasoby wydobywalne bilansowe': df.at[i, 'Zasoby wydobywalne bilansowe'],
                    'Zasoby wydobywalne pozabilansowe': df.at[i, 'Zasoby wydobywalne pozabilansowe'],
                    'Zasoby przemyslowe': df.at[i, 'Zasoby przemyslowe'],
                    'Emisja z wentylacja':df.at[i,'Emisja z wentylacja'],
                    'wydobycie': df.at[i, 'Wydobycie']
                }
            }
        elif 'WĘGLE  KAMIENNE' in files:
            d = {
                'name': df.at[i, "Nazwa"],
                'year': year,
                'type': type,
                'more': {
                    'stan': df.at[i, "Stan"],
                    'Zasoby geologiczne bilansowe Razem': df.at[i, 'Zasoby geologiczne bilansowe Razem'],
                    'Zasoby geologiczne bilansowe A+B+C1': df.at[i, 'Zasoby geologiczne bilansowe A+B+C1'],
                    'Zasoby wydobywalne bilansowe C2+D': df.at[i, 'Zasoby wydobywalne bilansowe C2+D'],
                    'Zasoby przemyslowe': df.at[i, 'Zasoby przemyslowe'],
                    'wydobycie': df.at[i, 'Wydobycie']
                }
            }
        elif 'SOLANKI, WODY LECZNICZE I TERMALNE' in files:
            d = {
                'name': df.at[i, "Nazwa"],
                'year': year,
                'type': type,
                'more': {
                    'Typ wody': df.at[i, "Typ wody"],
                    'Zasoby geologiczne bilansowe dyspozycyjne': df.at[i, 'Zasoby geologiczne bilansowe dyspozycyjne'],
                    'Zasoby geologiczne bilansowe eksploatacyjne': df.at[i, 'Zasoby geologiczne bilansowe eksploatacyjne'],
                    'Pobor': df.at[i, 'Pobor'],
                    'Powiat': df.at[i, 'Powiat']
                }
            }
        else:
            d = {
                'name': df.at[i, "Nazwa"],
                'year': year,
                'type': type,
                'more': {
                    'stan': df.at[i, "Stan"],
                    'Zasoby wydobywalne bilansowe': str(df.at[i, 'Zasoby wydobywalne bilansowe']),
                    'Zasoby przemyslowe': df.at[i, 'Zasoby przemyslowe'],
                    'Wydobycie': df.at[i, 'Wydobycie'],
                    'Powiat': df.at[i, 'Powiat']
                }
            }
        col.insert_one(d)