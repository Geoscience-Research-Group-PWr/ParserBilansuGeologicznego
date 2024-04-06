from pypdf import PdfReader,PdfWriter
import re
import pdfplumber
import pandas as pd
import os
import pymongo
import shutil
import logging


logger=logging.getLogger(__name__)


class Parser:
    """
    PDF parsing module.
    """
    def __init__(self,file:str):
        self.file=file
        self.path=os.getcwd()
        self.year=self.file[7:11]
        self.client = pymongo.MongoClient('mongodb+srv://mikolajsiewruk222:parser420@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority')  # zmienic password i username na swoje
        self.db = self.client['parser']
        self.collection = self.db['Kopalnie']

    def make_directories(self):
        """
        Creates necessary directories for organizing parsing results.
        :return:
        """
        if self.year=="2010":
            try:
                os.mkdir(f"{self.path}\Parsed_{self.year}1")
                logger.info(f"Created directory{self.path}\Parsed_{self.year}")
            except FileExistsError:
                pass
        try:
            os.mkdir(f"{self.path}\Parsed_{self.year}")
            logger.info(f"Created directory{self.path}\Parsed_{self.year}")
        except FileExistsError:
            pass
        try:
            os.mkdir(f"{self.path}\Split_{self.year}1")
            logger.info(f"Created directory{self.path}\Split_{self.year}")
        except FileExistsError:
            pass
        try:
            os.mkdir(f"{self.path}\CSV_{self.year}")
            logger.info(f"Created directory{self.path}\CSV_{self.year}")
        except FileExistsError:
            pass
        try:
            os.mkdir(f"{self.path}\Trash")
            logger.info(f"Created directory{self.path}\Trash")
        except FileExistsError:
            pass
        logger.info("All dirs created")

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
        logger.info(f"Created {name}parsed.pdf in {self.path}\Parsed_{self.year}")

    def headers(self,filename: str) -> list:
        """
        Extracts mineral names from page header.
        :param filename:a PDF file with tables only - created with parse()
        :return:a list with all minerals names within the input PDF file
        """
        header = ''
        output = []
        z = set()
        reader = PdfReader(filename)
        for page in reader.pages:
            text = page.extract_text()
            for i in range(0, 100):
                if text[i] != '\n':
                    header = text[0:i]
                    header = ''.join(sym for sym in header if not (sym.isdigit() or sym == '.'))
                    header = re.sub(r'^\s+|\s+$', '', header)
                else:
                    break
            z.add(header)
        for items in z:
            output.append(items)
        return output

    def get_pages(self,filename:str, header:str)->list:
        """
        Given a mineral name returns first and last page that a given mineral appears at.
        :param filename:a PDF file with tables only - created with parse()
        :param header: minerals name
        :return: a 2 element list with first and last appearance of the mineral name
        """
        occurance = []
        output = []
        reader = PdfReader(filename)
        for j in range(0, len(reader.pages)):
            page = reader.pages[j]
            if header in page.extract_text():
                occurance.append(j)
        output.append(min(occurance))
        output.append(max(occurance))
        return output

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
                if header==' ':
                    pass
                limits = self.get_pages(filename, header)
                pages = reader.pages[limits[0]:limits[-1] + 1]
                if header == "W\x08G L E   K A M I E N N E":
                    header = "WĘGLE KAMIENNE"
                if self.year in ['2018','2019','2020','2021','2022']:
                    res=re.sub(r' (?=[A-Z])', '', header)
                    if res=="W\x08GLE   KAMIENNE":
                        res="WeGLE KAMIENNE"
                    if '/' in res:
                        res = res.replace('D /P', 'DO PROD.')
                    new_file = open(f'{res}_{year}.pdf', 'wb')
                    for page in pages:
                        writer.add_page(page)
                        writer.write(new_file)
                    writer.close()
                    new_file.close()
                    shutil.move(f'{res}_{year}.pdf', f"{self.path}\Split_{self.year}")
                    logger.info(f"Created {res}_{year}.pdf in {self.path}\Split_{self.year}")
                else:
                    if '/' in header:
                        header = header.replace('D/P', 'DO PROD.')
                    new_file = open(f'{header}_{year}.pdf', 'wb')
                    for page in pages:
                        writer.add_page(page)
                        writer.write(new_file)
                    writer.close()
                    new_file.close()
                    shutil.move(f'{header}_{year}.pdf',f"{self.path}\Split_{self.year}1")
                    logger.info(f"Created {header}_{year}.pdf in {self.path}\Split_{self.year}")

    def export_data(self):
        """
        Converts PDF files to CSV.
        :return:
        """
        for files in os.listdir(f"{self.path}\Split_{self.year}1"):
            self.extract_one(f"{self.path}\Split_{self.year}1\\{files}")

    def clean_csv(self):
        """
        Changes headers of CSV files to adequate for each mineral type
        :return:
        """
        for files in os.listdir(f"{self.path}\CSV_{self.year}"):
            filename=f"{self.path}\CSV_{self.year}\\{files}"
            self.clean_one_csv(filename)
            
    def search_csv_for_errors(self):
        """
        Corrects conversion errors in CSV files. (unwanted letters or chars in columns)
        :return:
        """
      
        for files in os.listdir(f"{self.path}\CSV_{self.year}"):
            filename=f"{self.path}\CSV_{self.year}\\{files}"
            self.search_one_csv_for_errors(filename)
    def add_to_db(self):
        """
        Adds content of CSV files to MongoDB database.
        :return:
        """
        for files in os.listdir(f"{self.path}\CSV_{self.year}"):
            logger.info(f"Current CSV {files}")
            filename = f"{self.path}\CSV_{self.year}\{files}"
            df = pd.read_csv(filename, encoding='UTF-8')
            type = files[:-9]
            year = files[-8:-4]
            for i in range(0, df.shape[0]):
                if "Ŝ" in str(df.at[i,"Nazwa"]):
                    df.at[i,"Nazwa"]=df.at[i,"Nazwa"].replace("Ŝ","ż")
                if "Ŝ" in df.at[i, "Powiat"]:
                    df.at[i, "Powiat"] = df.at[i, "Powiat"].replace("Ŝ", "ż")
                d = {
                    'Name': df.at[i, "Nazwa"],
                    'Year': year,
                    'Type': type,
                    'More': {
                        'Stan': df.at[i, "Stan"],
                        'Zasoby wydobywalne bilansowe': str(df.at[i, 'Zasoby wydobywalne bilansowe']),
                        'Zasoby przemyslowe': str(df.at[i, 'Zasoby przemyslowe']),
                        'Wydobycie': str(df.at[i, 'Wydobycie']),
                        'Powiat': df.at[i, 'Powiat']
                    }
                }
                if "BENTONITY  I  IŁY  BENTONITOWE" in files:
                    d["Type"]="BENTONITY I IŁY BENTONITOWE"
                if "PIASKI I śWIRY" in files:
                    d["Type"]="PIASKI I ŻWIRY"
                if "KWARC  śYŁOWY" in files:
                    d["Type"] = "KWARC ŻYŁOWY"
                if "KWARCYTY  OGNI0TRWAŁE" in files:
                    d["Type"] = "KWARCYTY OGNIOTRWAŁE"
                if "R U D Y   Z Ł O T A,  A R S E N U   I   C Y N Y" in files:
                    d["Type"] = "RUDY ZŁOTA, ARSENU I CYNY"
                if 'R U D Y  M O L I B D E N O W O - W O L F R A M  O W O - M I E D Z I O W E' in files:
                    d["Type"] = "RUDY MOLIBDENOWO-WOLFRAMOWO-MIEDZIOWE"
                if 'S U R O W C E   I L A S T E' in files:
                    d["Type"] = "SUROWCE ILASTE"
                if 'S U R O W C E  D L A  P R A C  I N ś Y N I E R S K I C H' in files:
                    d["Type"] = "SUROWCE DLA PRAC INŻYNIERSKICH"
                if "K A L C Y T" in files:
                    d["Type"] = "KALCYT"
                self.collection.insert_one(d)
                logger.info(f"Added to database {d['Name']}")
                logger.info(f"Completed {i}/{len(df)}  ({round(i/len(df),2)}%)")

    def parse_one(self,name:str):
        """
        Extract all tables belonging to mineral name
        :param name:
        :return: PDF with one mineral tables
        """
        for files in os.listdir(f"{self.path}\Parsed_{self.year}"):
            filename=f"{self.path}\Parsed_{self.year}\\{files}"
            reader = PdfReader(filename)
            year = filename[-14:-10]
            writer = PdfWriter()
            header = name
            limits = self.get_pages(filename, header)
            if header=="W\x08G L E   K A M I E N N E":
                header="WĘGLE KAMIENNE"
            pages = reader.pages[limits[0]:limits[-1] + 1]
            if self.year in ['2018', '2019', '2020', '2021', '2022']:
                res = re.sub(r' (?=[A-Z])', '', header)
                if res == "GLE  KAMIENNE":
                    res = "WeGLE KAMIENNE"
                if '/' in res:
                    res = res.replace('D /P', 'DO PROD.')
                new_file = open(f'{res}_{year}.pdf', 'wb')
                for page in pages:
                    writer.add_page(page)
                    writer.write(new_file)
                writer.close()
                new_file.close()
                shutil.move(f'{res}_{year}.pdf', f"{self.path}\Split_{self.year}")
                logger.info(f"Created {res}_{year}.pdf in {self.path}\Split_{self.year}")
            else:
                if '/' in header:
                    header = header.replace('D/P', 'DO PROD.')
                new_file = open(f'{header}_{year}.pdf', 'wb')
                for page in pages:
                    writer.add_page(page)
                    writer.write(new_file)
                writer.close()
                new_file.close()
                shutil.move(f'{header}_{year}.pdf', f"{self.path}\Split_{self.year}")
                logger.info(f"Created {header}_{year}.pdf in {self.path}\Split_{self.year}")
    def extract_one(self,filepath:str):
        """
        Extract CSV from one PDF file
        :param filepath:
        :return: CSV file
        """
        name = str(filepath)[:-4]
        with pdfplumber.open(filepath) as pdf:
            data = []
            for page_number in range(1, len(pdf.pages) + 1):
                table = pdf.pages[page_number - 1].extract_table()
                d = [row for row in table if any(row)]
                data.extend(d)
            df = pd.DataFrame(data)
        df.to_csv(f'{name}.csv', index=False)
        shutil.move(f'{name}.csv', f"{self.path}\CSV_{self.year}")
        logger.info(f"Created {name}.csv in {self.path}\CSV_{self.year}")

    def clean_one_csv(self,filepath:str):
        """
        Add headers and clean empty cells in one CSV file
        :param filepath:
        :return:
        """

        df = pd.read_csv(filepath, encoding='UTF-8')
        '''if "PIASKI I śWIRY" in filepath:
            filepath=filepath.replace("PIASKI I śWIRY","PIASKI I ŻWIRY")'''
        if len(df.columns)==6:
            df.to_csv(filepath, index=False)
            shutil.move(filepath,"D:\POBRANE")
        elif "HEL" in filepath or "H E L" in filepath:
            new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?","Wydobycie"]
            df.columns = new_column_names
            df["Zasoby przemyslowe"]='-'
            df["Powiat"]='-'
            df = df.dropna()
        elif ("WĘGLE KAMIENNE" in filepath or "WĘGLE  KAMIENNE" in filepath) and self.year in ['2018','2019','2020','2021','2022','2017','2016']:
            new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?", "?", "?",
                                "?",
                                "Zasoby przemyslowe",
                                "Wydobycie"]
            df.columns = new_column_names
            df["Powiat"]="-"
            df = df.dropna()
        elif len(df.columns)==7:
            new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "Zasoby przemyslowe",
                                "Wydobycie", "Powiat"]
            df.columns = new_column_names
        elif len(df.columns)==8:
            new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?","?", "Zasoby przemyslowe",
                                "Wydobycie",]
            df.columns = new_column_names
            df["Powiat"]="-"
            df.dropna()
        elif len(df.columns) == 9 :
            new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?", "Zasoby przemyslowe",
                                "Wydobycie",
                                "Powiat"]
            df.columns = new_column_names
        elif len(df.columns) == 10:
            new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?", "?",
                                "Zasoby przemyslowe",
                                "Wydobycie",
                                "Powiat"]
            df.columns = new_column_names
        elif len(df.columns)==11:
            new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?", "?", "?",
                                "Zasoby przemyslowe",
                                "Wydobycie",
                                "Powiat"]
            df.columns = new_column_names
        elif len(df.columns)==12:
            new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?", "?", "?", "?",
                                "Zasoby przemyslowe",
                                "Wydobycie",
                                "Powiat"]
            df.columns = new_column_names
        '''if 'H E L' in filepath:
            new_column_names = ['Lp.', 'Nazwa', 'Stan', 'Zas. wyd. bil. Razem', 'Zas. wyd. bil. A+B',
                                'Zas. wyd. bil. C', 'Wydobycie']
        elif 'M E T A N  P O K Ł A D Ó W  W ĘG L A' in filepath:
            new_column_names = ['Lp.', 'Nazwa', 'Stan', 'Zasoby wydobywalne bilansowe',
                                'Zasoby wydobywalne pozabilansowe', 'Zasoby przemyslowe', 'Emisja z wentylacja',
                                'Wydobycie']
        elif 'WĘGLE  KAMIENNE' in filepath:
            new_column_names = ['Lp.', 'Nazwa', 'Stan', 'Zasoby geologiczne bilansowe Razem',
                                'Zasoby geologiczne bilansowe A+B+C1', 'Zasoby wydobywalne bilansowe C2+D',
                                'Zasoby przemyslowe', 'Wydobycie']
        elif 'SOLANKI, WODY LECZNICZE I TERMALNE' in filepath:
            new_column_names = ['Lp.', 'Nazwa', 'Typ wody', 'Zasoby geologiczne bilansowe dyspozycyjne',
                                'Zasoby geologiczne bilansowe eksploatacyjne', 'Pobor', 'Powiat']
        elif "WODY PITNE I PRZEMYSŁOWE" in filepath:
            new_column_names = ['Lp', 'Znak', 'Data', 'Nazwa', 'Powierzchnia', 'Modul']
        else:
            new_column_names = ['Lp.', 'Nazwa', 'Stan', 'Zasoby wydobywalne bilansowe', 'Zasoby przemyslowe',
                                'Wydobycie', 'Powiat']
        new_column_names=["Lp.","Nazwa","Stan","Zasoby wydobywalne bilansowe","Zasoby przemysłowe","Wydobycie","Powiat"]
        new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe","?", "Zasoby przemysłowe", "Wydobycie",
                            "Powiat"] # 8
        new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe","?","?", "Zasoby przemysłowe", "Wydobycie",
                            "Powiat"] #9
        new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?","?", "Zasoby przemysłowe",
                            "Wydobycie",
                            "Powiat"]  # 10
        new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?", "?","?", "Zasoby przemysłowe",
                            "Wydobycie",
                            "Powiat"]  # 11
        new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?", "?", "?","?",
                            "Zasoby przemysłowe",
                            "Wydobycie",
                            "Powiat"]  # 12
        #wegle kam
        new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?", "?", "?",
                            "?",
                            "Zasoby przemysłowe",
                            "Wydobycie"]  # 11 dodac kolumne powiat i wypełnić "-"
        # hel
        new_column_names = ["Lp.", "Nazwa", "Stan", "Zasoby wydobywalne bilansowe", "?", "?",

                            "Zasoby przemysłowe",
                            "Wydobycie"]  # 11 dodac kolumne powiat i wypełnić "-" zas przem wypełnic -'''
        '''difference = abs(len(df.columns) - len(new_column_names))
        if difference > 0:
            new_column_names.extend('?')
        df.columns = new_column_names'''
        df = df.dropna()
        df.to_csv(filepath, index=False)
        logger.info(f"Added column headers in {filepath}")

    def search_one_csv_for_errors(self,filepath:str):
        """
        Clean unwanted characters in one CSV file
        :param filepath:
        :return:
        """
        df = pd.read_csv(filepath, encoding='UTF-8')
        for i in range(0, len(df)):
            if df.at[i, "Nazwa"][0] == "ś":
                df.at[i, "Nazwa"]="Ż"+df.at[i, "Nazwa"][1:]
            if not df.at[i, "Nazwa"][0].isupper():
                df.at[i, "Nazwa"] = df.at[i, "Nazwa"][1:]

            if not df.at[i, "Stan"][0].isupper():
                df.at[i, "Stan"] = df.at[i, "Stan"][1:]

            if str(df.at[i, "Zasoby wydobywalne bilansowe"]) == "tylko pzb.":
                pass
            elif str(df.at[i, "Zasoby wydobywalne bilansowe"])[0].islower() or \
                    str(df.at[i, "Zasoby wydobywalne bilansowe"])[0] == '.':
                df.at[i, "Zasoby wydobywalne bilansowe"] = df.at[i, "Zasoby wydobywalne bilansowe"][1:]

            if df.at[i, "Zasoby przemyslowe"] == "tylko pzb.":
                pass
            elif str(df.at[i, "Zasoby przemyslowe"])[0].islower() or str(df.at[i, "Zasoby przemyslowe"])[0] == '.':
                df.at[i, "Zasoby przemyslowe"] = df.at[i, "Zasoby przemyslowe"][1:]

            if str(df.at[i, "Wydobycie"])[0].islower() or str(df.at[i, "Wydobycie"])[0] == '.':
                df.at[i, "Wydobycie"] = df.at[i, "Wydobycie"][1:]
        '''if 'H E L' in filepath:
            for i in range(0, len(df)):
                if not df.at[i, "Nazwa"][0].isupper():
                    df.at[i, "Nazwa"] = df.at[i, "Nazwa"][1:]

                if not df.at[i, "Stan"][0].isupper():
                    df.at[i, "Stan"] = df.at[i, "Stan"][1:]

                if str(df.at[i, "Zas. wyd. bil. Razem"]) == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zas. wyd. bil. Razem"])[0].islower() or str(df.at[i, "Zas. wyd. bil. Razem"])[
                    0] == '.':
                    df.at[i, "Zas. wyd. bil. Razem"] = df.at[i, "Zas. wyd. bil. Razem"][1:]

                if df.at[i, "Zas. wyd. bil. A+B"] == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zas. wyd. bil. A+B"])[0].islower() or str(df.at[i, "Zas. wyd. bil. A+B"])[0] == '.':
                    df.at[i, "Zas. wyd. bil. A+B"] = df.at[i, "Zas. wyd. bil. A+B"][1:]

                if df.at[i, "Zas. wyd. bil. C"] == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zas. wyd. bil. C"])[0].islower() or str(df.at[i, "Zas. wyd. bil. C"])[0] == '.':
                    df.at[i, "Zas. wyd. bil. C"] = df.at[i, "Zas. wyd. bil. C"][1:]

                if df.at[i, "Wydobycie"][0].islower() or df.at[i, "Wydobycie"][0] == '.':
                    df.at[i, "Wydobycie"] = df.at[i, "Wydobycie"][1:]

        elif 'M E T A N  P O K Ł A D Ó W  W ĘG L A' in filepath:
            for i in range(0, len(df)):
                if not df.at[i, "Nazwa"][0].isupper():
                    df.at[i, "Nazwa"] = df.at[i, "Nazwa"][1:]

                if not df.at[i, "Stan"][0].isupper():
                    df.at[i, "Stan"] = df.at[i, "Stan"][1:]

                if str(df.at[i, "Zasoby wydobywalne bilansowe"]) == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zasoby wydobywalne bilansowe"])[0].islower() or \
                        str(df.at[i, "Zasoby wydobywalne bilansowe"])[0] == '.':
                    df.at[i, "Zasoby wydobywalne bilansowe"] = df.at[i, "Zasoby wydobywalne bilansowe"][1:]

                if df.at[i, "Zasoby wydobywalne pozabilansowe"] == "tylko pzb.":
                    pass
                elif df.at[i, "Zasoby wydobywalne pozabilansowe"][0].islower() or \
                        df.at[i, "Zasoby wydobywalne pozabilansowe"][0] == '.':
                    df.at[i, "Zasoby wydobywalne pozabilansowe"] = df.at[i, "Zasoby wydobywalne pozabilansowe"][1:]

                if df.at[i, "Zasoby przemyslowe"] == "tylko pzb.":
                    pass
                elif df.at[i, "Zasoby przemyslowe"][0].islower() or df.at[i, "Zasoby przemyslowe"][0] == '.':
                    df.at[i, "Zasoby przemyslowe"] = df.at[i, "Zasoby przemyslowe"][1:]

                if df.at[i, "Emisja z wentylacja"][0].islower() or df.at[i, "Emisja z wentylacja"][0] == '.':
                    df.at[i, "Emisja z wentylacja"] = df.at[i, "Emisja z wentylacja"][1:]

                if df.at[i, "Wydobycie"][0].islower() or df.at[i, "Wydobycie"][0] == '.':
                    df.at[i, "Wydobycie"] = df.at[i, "Wydobycie"][1:]


        elif 'WĘGLE  KAMIENNE' in filepath:
            for i in range(0, len(df)):
                if not df.at[i, "Nazwa"][0].isupper():
                    df.at[i, "Nazwa"] = df.at[i, "Nazwa"][1:]

                if not df.at[i, "Stan"][0].isupper():
                    df.at[i, "Stan"] = df.at[i, "Stan"][1:]

                if str(df.at[i, "Zasoby geologiczne bilansowe Razem"]) == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zasoby geologiczne bilansowe Razem"])[0].islower() or \
                        str(df.at[i, "Zasoby geologiczne bilansowe Razem"])[0] == '.':
                    df.at[i, "Zasoby geologiczne bilansowe Razem"] = df.at[i, "Zasoby geologiczne bilansowe Razem"][
                                                                     1:]

                if df.at[i, "Zasoby geologiczne bilansowe A+B+C1"] == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zasoby geologiczne bilansowe A+B+C1"])[0].islower() or \
                        str(df.at[i, "Zasoby geologiczne bilansowe A+B+C1"])[0] == '.':
                    df.at[i, "Zasoby geologiczne bilansowe A+B+C1"] = df.at[
                                                                          i, "Zasoby geologiczne bilansowe A+B+C1"][
                                                                      1:]

                if df.at[i, "Zasoby wydobywalne bilansowe C2+D"] == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zasoby wydobywalne bilansowe C2+D"])[0].islower() or \
                        str(df.at[i, "Zasoby wydobywalne bilansowe C2+D"])[0] == '.':
                    df.at[i, "Zasoby wydobywalne bilansowe C2+D"] = df.at[i, "Zasoby wydobywalne bilansowe C2+D"][
                                                                    1:]

                if str(df.at[i, "Zasoby przemyslowe"])[0].islower() or str(df.at[i, "Zasoby przemyslowe"])[0] == '.':
                    df.at[i, "Zasoby przemyslowe"] = df.at[i, "Zasoby przemyslowe"][1:]

                if df.at[i, "Wydobycie"][0].islower() or df.at[i, "Wydobycie"][0] == '.':
                    df.at[i, "Wydobycie"] = df.at[i, "Wydobycie"][1:]

        elif 'SOLANKI, WODY LECZNICZE I TERMALNE' in filepath:
            for i in range(0, len(df)):
                if not df.at[i, "Nazwa"][0].isupper():
                    df.at[i, "Nazwa"] = df.at[i, "Nazwa"][1:]

                if not df.at[i, "Typ wody"][0].isupper():
                    df.at[i, "Typ wody"] = df.at[i, "Typ wody"][1:]

                if str(df.at[i, "Zasoby geologiczne bilansowe dyspozycyjne"]) == "nie ekspl.":
                    pass
                elif str(df.at[i, "Zasoby geologiczne bilansowe dyspozycyjne"])[0].islower() or \
                        str(df.at[i, "Zasoby geologiczne bilansowe dyspozycyjne"])[0] == '.':
                    df.at[i, "Zasoby geologiczne bilansowe dyspozycyjne"] = df.at[
                                                                                i, "Zasoby geologiczne bilansowe dyspozycyjne"][
                                                                            1:]

                if str(df.at[i, "Zasoby geologiczne bilansowe eksploatacyjne"]) == "nie ekspl.":
                    pass
                elif str(df.at[i, "Zasoby geologiczne bilansowe eksploatacyjne"])[0].islower() or \
                        str(df.at[i, "Zasoby geologiczne bilansowe eksploatacyjne"])[0] == '.':
                    df.at[i, "Zasoby geologiczne bilansowe eksploatacyjne"] = df.at[
                                                                                  i, "Zasoby geologiczne bilansowe eksploatacyjne"][
                                                                              1:]

                if str(df.at[i, "Pobor"]) == "nie ekspl." or df.at[i, "Pobor"] == "b.d.":
                    pass
                elif str(df.at[i, "Pobor"])[0].islower() or str(df.at[i, "Pobor"])[0] == '.':
                    df.at[i, "Pobor"] = df.at[i, "Pobor"][1:]
        else:
            for i in range(0, len(df)):
                if not df.at[i, "Nazwa"][0].isupper():
                    df.at[i, "Nazwa"] = df.at[i, "Nazwa"][1:]

                if not df.at[i, "Stan"][0].isupper():
                    df.at[i, "Stan"] = df.at[i, "Stan"][1:]

                if str(df.at[i, "Zasoby wydobywalne bilansowe"]) == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zasoby wydobywalne bilansowe"])[0].islower() or \
                        str(df.at[i, "Zasoby wydobywalne bilansowe"])[0] == '.':
                    df.at[i, "Zasoby wydobywalne bilansowe"] = df.at[i, "Zasoby wydobywalne bilansowe"][1:]

                if df.at[i, "Zasoby przemyslowe"] == "tylko pzb.":
                    pass
                elif str(df.at[i, "Zasoby przemyslowe"])[0].islower() or str(df.at[i, "Zasoby przemyslowe"])[0] == '.':
                    df.at[i, "Zasoby przemyslowe"] = df.at[i, "Zasoby przemyslowe"][1:]

                if df.at[i, "Wydobycie"][0].islower() or df.at[i, "Wydobycie"][0] == '.':
                    df.at[i, "Wydobycie"] = df.at[i, "Wydobycie"][1:]'''
        df.to_csv(filepath, index=False)
        logger.info(f"Mistakes corrected in {filepath}")

    def add_one_file(self,filename:str):
        """
        Add one file to database.
        :param filename:
        :return:
        """
        logger.info(f"Current CSV {filename}")
        df = pd.read_csv(filename, encoding='UTF-8')
        type = filename[:-9]
        year = filename[-8:-4]
        for i in range(0, df.shape[0]):
            if "Ŝ" in str(df.at[i, "Nazwa"]):
                df.at[i, "Nazwa"] = df.at[i, "Nazwa"].replace("Ŝ", "ż")
            if "Ŝ" in str(df.at[i, "Powiat"]):
                df.at[i, "Powiat"] = df.at[i, "Powiat"].replace("Ŝ", "ż")
            d = {
                'Name': df.at[i, "Nazwa"],
                'Year': year,
                'Type': type,
                'More': {
                    'Stan': df.at[i, "Stan"],
                    'Zasoby wydobywalne bilansowe': str(df.at[i, 'Zasoby wydobywalne bilansowe']),
                    'Zasoby przemyslowe': str(df.at[i, 'Zasoby przemyslowe']),
                    'Wydobycie': str(df.at[i, 'Wydobycie']),
                    'Powiat': df.at[i, 'Powiat']
                }
            }
            '''if 'H E L' in filename:
                d = {
                    'Name': df.at[i, "Nazwa"],
                    'Year': year,
                    'Type': 'HEL',
                    'More': {
                        'Stan': df.at[i, "Stan"],
                        'Zas. wyd. bil. Razem': str(df.at[i, 'Zas. wyd. bil. Razem']),
                        'Zas. wyd. bil. A+B': str(df.at[i, 'Zas. wyd. bil. A+B']),
                        'Zas. wyd. bil. C': str(df.at[i, 'Zas. wyd. bil. C']),
                        'Wydobycie': str(df.at[i, 'Wydobycie'])
                    }
                }
            elif 'M E T A N  P O K Ł A D Ó W  W ĘG L A' in filename:
                d = {
                    'Name': df.at[i, "Nazwa"],
                    'Year': year,
                    'Type': 'METAN POKŁADÓW WĘGLA',
                    'More': {
                        'Stan': df.at[i, "Stan"],
                        'Zasoby wydobywalne bilansowe': str(df.at[i, 'Zasoby wydobywalne bilansowe']),
                        'Zasoby wydobywalne pozabilansowe': str(df.at[i, 'Zasoby wydobywalne pozabilansowe']),
                        'Zasoby przemyslowe': str(df.at[i, 'Zasoby przemyslowe']),
                        'Emisja z wentylacja': str(df.at[i, 'Emisja z wentylacja']),
                        'Wydobycie': str(df.at[i, 'Wydobycie'])
                    }
                }
            elif 'WĘGLE  KAMIENNE' in filename:
                d = {
                    'Name': df.at[i, "Nazwa"],
                    'Year': year,
                    'Type': 'WĘGLE KAMIENNE',
                    'More': {
                        'Stan': df.at[i, "Stan"],
                        'Zasoby geologiczne bilansowe Razem': str(df.at[i, 'Zasoby geologiczne bilansowe Razem']),
                        'Zasoby geologiczne bilansowe A+B+C1': str(df.at[i, 'Zasoby geologiczne bilansowe A+B+C1']),
                        'Zasoby wydobywalne bilansowe C2+D': str(df.at[i, 'Zasoby wydobywalne bilansowe C2+D']),
                        'Zasoby przemyslowe': str(df.at[i, 'Zasoby przemyslowe']),
                        'Wydobycie': str(df.at[i, 'Wydobycie'])
                    }
                }
            elif 'SOLANKI, WODY LECZNICZE I TERMALNE' in filename:
                if "Ŝ" in df.at[i, "Powiat"]:
                    df.at[i, "Powiat"] = df.at[i, "Powiat"].replace("Ŝ", "ż")
                d = {
                    'Name': df.at[i, "Nazwa"],
                    'Year': year,
                    'Type': type,
                    'More': {
                        'Typ wody': df.at[i, "Typ wody"],
                        'Zasoby geologiczne bilansowe dyspozycyjne': str(df.at[
                                                                             i, 'Zasoby geologiczne bilansowe dyspozycyjne']),
                        'Zasoby geologiczne bilansowe eksploatacyjne': str(df.at[
                                                                               i, 'Zasoby geologiczne bilansowe eksploatacyjne']),
                        'Pobor': str(df.at[i, 'Pobor']),
                        'Powiat': df.at[i, 'Powiat']
                    }
                }
            else:
                if "Ŝ" in df.at[i, "Powiat"]:
                    df.at[i, "Powiat"] = df.at[i, "Powiat"].replace("Ŝ", "ż")
                d = {
                    'Name': df.at[i, "Nazwa"],
                    'Year': year,
                    'Type': type,
                    'More': {
                        'Stan': df.at[i, "Stan"],
                        'Zasoby wydobywalne bilansowe': str(df.at[i, 'Zasoby wydobywalne bilansowe']),
                        'Zasoby przemyslowe': str(df.at[i, 'Zasoby przemyslowe']),
                        'Wydobycie': str(df.at[i, 'Wydobycie']),
                        'Powiat': df.at[i, 'Powiat']
                    }
                }'''
            if "BENTONITY  I  IŁY  BENTONITOWE" in filename:
                d["Type"] = "BENTONITY I IŁY BENTONITOWE"
            if "PIASKI I śWIRY" in filename:
                d["Type"] = "PIASKI I ŻWIRY"
            if "KWARC  śYŁOWY" in filename:
                d["Type"] = "KWARC ŻYŁOWY"
            if "KWARCYTY  OGNI0TRWAŁE" in filename:
                d["Type"] = "KWARCYTY OGNIOTRWAŁE"
            if "R U D Y   Z Ł O T A,  A R S E N U   I   C Y N Y" in filename:
                d["Type"] = "RUDY ZŁOTA, ARSENU I CYNY"
            if 'R U D Y  M O L I B D E N O W O - W O L F R A M  O W O - M I E D Z I O W E' in filename:
                d["Type"] = "RUDY MOLIBDENOWO-WOLFRAMOWO-MIEDZIOWE"
            if 'S U R O W C E   I L A S T E' in filename:
                d["Type"] = "SUROWCE ILASTE"
            if 'S U R O W C E  D L A  P R A C  I N ś Y N I E R S K I C H' in filename:
                d["Type"] = "SUROWCE DLA PRAC INŻYNIERSKICH"
            if "K A L C Y T" in filename:
                d["Type"] = "KALCYT"
            self.collection.insert_one(d)
            logger.info(f"Added to database {d['Name']}")
            logger.info(f"Completed {i}/{len(df)}  ({(round(i / len(df), 2))*100}%)")

'''
Przykład użycia:
p=Parser("Bilans_2011.pdf")
p.make_directories()
p.parse()
p.parse_parsed()
p.export_data()
p.clean_csv()

p.search_csv_for_errors()
p.add_to_db()'''
