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
        self.client = pymongo.MongoClient('mongodb+srv://<USERNAME>:<PASSWORD>@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority')  # zmienic password i username na swoje
        self.db = self.client['parser']
        self.collection = self.db['Kopalnie']

    def make_directories(self):
        """
        Creates necessary directories for organizing parsing results.
        :return:
        """
        os.mkdir(f"{self.path}\Parsed_{self.year}")
        os.mkdir(f"{self.path}\Split_{self.year}")
        os.mkdir(f"{self.path}\CSV_{self.year}")

    def parse(self):
        """
        From source .pdf file extracts a PDF with tables only. Moves the file to a dir created with make_directories()
        :return:
        """
        reader = PdfReader(self.file)
        writer = PdfWriter()
        name = str(self.file)[:-4]
        for page in reader.pages:
            if 'Lp.' in page.extract_text() and ('zag.' in page.extract_text() or "Powiat" in page.extract_text()):  # dodac warunek na powiat np zeby odsiac niechciane tabele
                writer.add_page(page)
                with open(f'{name}parsed.pdf', 'wb') as file:
                    writer.write(file)
        shutil.move(f'{name}parsed.pdf',f"{self.path}\Parsed_{self.year}")

    def headers(self,filename: str) -> list:
        """
        Extracts mineral names from page header.
        :param filename:a PDF file with tables only - created with parse()
        :return:a list with all minerals names within the input PDF file
        """
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
            zi.append(items)
        return zi

    def get_pages(self,filename:str, header:str)->list:
        """
        Given a mineral name returns first and last page that a given mineral appears at.
        :param filename:a PDF file with tables only - created with parse()
        :param header: minerals name
        :return: a 2 element list with first and last appearance of the mineral name
        """
        occurance = []
        c = []
        reader = PdfReader(filename)
        for j in range(0, len(reader.pages)):
            page = reader.pages[j]
            if header in page.extract_text():
                occurance.append(j)
        c.append(min(occurance))
        c.append(max(occurance))
        return c

    def parse_parsed(self):
        """
        Splits a PDF file with tables only.
        :return: Dir of PDF files with tables belonging to the same mineral name
        """
        for files in os.listdir(f"{self.path}\Parsed_{self.year}"):
            filename=f"{self.path}\Parsed_{self.year}\\{files}"
            reader = PdfReader(filename)
            year = filename[-14:-10]
            z = self.headers(filename)
            for i in range(0, len(z)):
                writer = PdfWriter()
                header = z[i]
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

    def export_data(self):
        """
        Converts PDF files to CSV.
        :return:
        """
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
        """
        Changes headers of CSV files to adequate for each mineral type
        :return:
        """
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

    def add_to_db(self):
        """
        Adds content of CSV files to MongoDB database.
        :return:
        """
        for files in os.listdir(f"{self.path}\CSV_{self.year}"):
            filename = f"{self.path}\CSV_{self.year}\{files}"
            df = pd.read_csv(filename, encoding='UTF-8')
            type = files[:-9]
            year = files[-8:-4]
            for i in range(0, df.shape[0]):
                if 'H E L' in files:
                    d = {
                        'Name': df.at[i, "Nazwa"],
                        'Year': year,
                        'Type': type,
                        'More': {
                            'Stan': df.at[i, "Stan"],
                            'Zas. wyd. bil. Razem': df.at[i, 'Zas. wyd. bil. Razem'],
                            'Zas. wyd. bil. A+B': df.at[i, 'Zas. wyd. bil. A+B'],
                            'Zas. wyd. bil. C': df.at[i, 'Zas. wyd. bil. C'],
                            'Wydobycie': df.at[i, 'Wydobycie']
                        }
                    }
                elif 'M E T A N  P O K Ł A D Ó W  W ĘG L A' in files:
                    d = {
                        'Name': df.at[i, "Nazwa"],
                        'Year': year,
                        'Type': type,
                        'More': {
                            'Stan': df.at[i, "Stan"],
                            'Zasoby wydobywalne bilansowe': df.at[i, 'Zasoby wydobywalne bilansowe'],
                            'Zasoby wydobywalne pozabilansowe': df.at[i, 'Zasoby wydobywalne pozabilansowe'],
                            'Zasoby przemyslowe': df.at[i, 'Zasoby przemyslowe'],
                            'Emisja z wentylacja': df.at[i, 'Emisja z wentylacja'],
                            'Wydobycie': df.at[i, 'Wydobycie']
                        }
                    }
                elif 'WĘGLE  KAMIENNE' in files:
                    d = {
                        'Name': df.at[i, "Nazwa"],
                        'Year': year,
                        'Type': type,
                        'More': {
                            'Stan': df.at[i, "Stan"],
                            'Zasoby geologiczne bilansowe Razem': df.at[i, 'Zasoby geologiczne bilansowe Razem'],
                            'Zasoby geologiczne bilansowe A+B+C1': df.at[i, 'Zasoby geologiczne bilansowe A+B+C1'],
                            'Zasoby wydobywalne bilansowe C2+D': df.at[i, 'Zasoby wydobywalne bilansowe C2+D'],
                            'Zasoby przemyslowe': df.at[i, 'Zasoby przemyslowe'],
                            'Wydobycie': df.at[i, 'Wydobycie']
                        }
                    }
                elif 'SOLANKI, WODY LECZNICZE I TERMALNE' in files:
                    d = {
                        'Name': df.at[i, "Nazwa"],
                        'Year': year,
                        'Type': type,
                        'More': {
                            'Typ wody': df.at[i, "Typ wody"],
                            'Zasoby geologiczne bilansowe dyspozycyjne': df.at[
                                i, 'Zasoby geologiczne bilansowe dyspozycyjne'],
                            'Zasoby geologiczne bilansowe eksploatacyjne': df.at[
                                i, 'Zasoby geologiczne bilansowe eksploatacyjne'],
                            'Pobor': df.at[i, 'Pobor'],
                            'Powiat': df.at[i, 'Powiat']
                        }
                    }
                else:
                    d = {
                        'Name': df.at[i, "Nazwa"],
                        'Year': year,
                        'Type': type,
                        'More': {
                            'Stan': df.at[i, "Stan"],
                            'Zasoby wydobywalne bilansowe': str(df.at[i, 'Zasoby wydobywalne bilansowe']),
                            'Zasoby przemyslowe': df.at[i, 'Zasoby przemyslowe'],
                            'Wydobycie': df.at[i, 'Wydobycie'],
                            'Powiat': df.at[i, 'Powiat']
                        }
                    }
                self.collection.insert_one(d)

'''
Przykład użycia:
p=Parser("Bilans_2011.pdf")
p.make_directories()
p.parse()
p.parse_parsed()
p.export_data()
p.clean_csv()
p.add_to_db()
'''