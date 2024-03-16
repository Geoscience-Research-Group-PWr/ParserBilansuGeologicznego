from pypdf import PdfReader,PdfWriter
import re
import pdfplumber
import pandas as pd
import os
import pymongo
import shutil


class Parser:
    def __init__(self,file):
        self.file=file
        self.path=os.getcwd()
        self.year=self.file[7:11]

    def make_directories(self):
        os.mkdir(f"{self.path}\Parsed_{self.year}")
        os.mkdir(f"{self.path}\Split_{self.year}")
        os.mkdir(f"{self.path}\CSV_{self.year}")
    def parse(self):
        reader = PdfReader(self.file)
        writer = PdfWriter()
        name = str(self.file)[:-4]
        for page in reader.pages:
            if 'Lp.' in page.extract_text() and ('zag.' in page.extract_text() or "Powiat" in page.extract_text()):  # dodac warunek na powiat np zeby odsiac niechciane tabele
                writer.add_page(page)
                with open(f'{name}parsed.pdf', 'wb') as file:
                    writer.write(file)
        shutil.move(f'{name}parsed.pdf',f"{self.path}\Parsed_{self.year}")

    def headers(self,filename):
        header = ''
        zi = []
        z = set()
        reader = PdfReader(filename)
        for page in reader.pages:
            t = page.extract_text()
            for i in range(0, 100):
                if t[i] != '\n':
                    header = t[0:i]
                    header = ''.join(sym for sym in header if not (sym.isdigit() or sym == '.'))
                    header = re.sub(r'^\s+|\s+$', '', header)
                else:
                    break
            z.add(header)
        for items in z:
            print(items)
            zi.append(items)
        return zi

    def get_pages(self,filename, header):
        occurance = []
        c = []
        reader = PdfReader(filename)
        for j in range(0, len(reader.pages)):
            page = reader.pages[j]
            if header in page.extract_text():
                occurance.append(j)
        c.append(min(occurance))
        c.append(max(occurance))
        print(c)
        return c

    def parse_parsed(self):
        for files in os.listdir(f"{self.path}\Parsed_{self.year}"):
            filename=f"{self.path}\Parsed_{self.year}\\{files}"
            reader = PdfReader(filename)
            year = filename[-14:-10]
            z = self.headers(filename)
            for i in range(0, len(z)):
                writer = PdfWriter()
                header = z[i]
                print(header)
                limits = self.get_pages(filename, header)
                pages = reader.pages[limits[0]:limits[-1] + 1]
                if '/' in header:
                    header = header.replace('D/P', 'DO PROD.')
                new_file = open(f'{header}_{year}.pdf', 'wb')
                for page in pages:
                    writer.add_page(page)
                    writer.write(new_file)
                writer.close()
                new_file.close()
                shutil.move(f'{header}_{year}.pdf',f"{self.path}\Split_{self.year}")

    def exportdata(self):
        for files in os.listdir(f"{self.path}\Split_{self.year}"):
            filename=f"{self.path}\Split_{self.year}\{files}"
            name = str(filename)[:-4]
            with pdfplumber.open(filename) as pdf:
                data = []
                for page_number in range(1, len(pdf.pages) + 1):
                    table = pdf.pages[page_number - 1].extract_table()
                    d = [row for row in table if any(row)]
                    data.extend(d)
                df = pd.DataFrame(data)
            df.to_csv(f'{name}.csv', index=False)
            shutil.move(f'{name}.csv',f"{self.path}\CSV_{self.year}")

    def clean_csv(self):
        for files in os.listdir(f"{self.path}\CSV_{self.year}"):
            filename=f"{self.path}\CSV_{self.year}\{files}"
            df = pd.read_csv(filename, encoding='UTF-8')
            if 'H E L' in filename:
                new_column_names = ['Lp.', 'Nazwa', 'Stan', 'Zas. wyd. bil. Razem', 'Zas. wyd. bil. A+B',
                                    'Zas. wyd. bil. C', 'Wydobycie']
            elif 'M E T A N  P O K Ł A D Ó W  W ĘG L A' in filename:
                new_column_names = ['Lp.', 'Nazwa', 'Stan', 'Zasoby wydobywalne bilansowe',
                                    'Zasoby wydobywalne pozabilansowe', 'Zasoby przemyslowe', 'Emisja z wentylacja',
                                    'Wydobycie']
            elif 'WĘGLE  KAMIENNE' in filename:
                new_column_names = ['Lp.', 'Nazwa', 'Stan', 'Zasoby geologiczne bilansowe Razem',
                                    'Zasoby geologiczne bilansowe A+B+C1', 'Zasoby wydobywalne bilansowe C2+D',
                                    'Zasoby przemyslowe', 'Wydobycie']
            elif 'SOLANKI, WODY LECZNICZE I TERMALNE' in filename:
                new_column_names = ['Lp.', 'Nazwa', 'Typ wody', 'Zasoby geologiczne bilansowe dyspozycyjne',
                                    'Zasoby geologiczne bilansowe eksploatacyjne', 'Pobor', 'Powiat']
            elif "WODY PITNE I PRZEMYSŁOWE" in filename:
                new_column_names = ['Lp', 'Znak', 'Data', 'Nazwa', 'Powierzchnia', 'Modul']
            else:
                new_column_names = ['Lp.', 'Nazwa', 'Stan', 'Zasoby wydobywalne bilansowe', 'Zasoby przemyslowe',
                                    'Wydobycie', 'Powiat']
            difference = abs(len(df.columns) - len(new_column_names))
            if difference > 0:
                new_column_names.extend('?')
            df.columns = new_column_names
            df = df.dropna()
            df.to_csv(filename, index=False)
p=Parser("Bilans_2011.pdf")
p.parse()
