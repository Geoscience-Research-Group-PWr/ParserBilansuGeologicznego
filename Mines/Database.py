import pymongo
import datetime

class Database:
    """
    MongoDB operations module.
    """
    def __init__(self):
        self.connection=pymongo.MongoClient('mongodb+srv://mikolajsiewruk222:parser420@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority&appName=parser')
        self.db=self.connection['parser']
        self.collection=self.db['Kopalnie']

    def search_by_name(self,name:str,start=0,end=datetime.date.today().year,county=""):
        """
        Querying by mine name.
        :param t: name of a mine
        :param start:
        :param end:
        :param county:
        :return: list of objects from the database searched by name in range given by start and end years.
        """
        result=[]
        if county: # dodać warunek że pole powiat istnieje
            query = {"$and": [{"Name": name}, {"Year": {"$gte": str(start)}}, {"Year": {"$lte": str(end)}},{"More.Powiat":county}]}
        query={"$and":[{"Name":name},{"Year":{"$gte":str(start)}},{"Year":{"$lte":str(end)}}]}
        output=self.collection.find(query)
        for results in output:
            result.append(results)
        return result

    def search_by_type(self,t:str,start=0,end=datetime.date.today().year)->list:
        """
        Querying by mineral type.
        :param t: name of a type
        :param start:
        :param end:
        :return: list of objects from the database searched by type in range given by start and end years.
        """
        result = []
        query = {"$and": [{"Type": t}, {"Year": {"$gte": str(start)}}, {"Year": {"$lte": str(end)}}]}
        output = self.collection.find(query)
        for results in output:
            result.append(results)
        return result

    def search_by_county(self,county:str,start=0,end=datetime.date.today().year)-> list:
        """
        Querying by a given county
        :param county:
        :param start:
        :param end:
        :return: list of objects where county field contains given county
        """
        result=[]
        query={"More.Powiat":str(county)}
        output = self.collection.find(query)
        for results in output:
            result.append(results)
        return result
    def get_data(self,results:list,headers:list)->tuple:
        """
        Retrieving row data from searching
        :param results: list of results from searching
        :param headers: list of column headers
        :return: tuple(list,list)
        """
        data=[]
        h=[]
        w=[]
        s=[]
        m=[]
        zas_wyd_bil=0 # suma zasobów wydobywalnych bilansowych
        zas_przem=0
        wyd=0
        zas_ab=0
        zas_c=0
        hel=False
        coal=False
        water=False
        met=False

        # dla typów - dodanie wykresów wydobycia w czasie, policzenie średniej wydobycia na rok
        # dla nazw dodanie sumy wydobycia w czasie, wykres wydobycia (opcjonalnie)
        # doprecyzowanie wyszukiwania po nazwach (dodać powiat)
        # wyszukiwanie po powiecie, wykresy i sumy itd
        # w js napisać coś do eksportu danych
        # external js w folderze static

        for i in range(len(results[0])):
            temp=results[0]
            if temp[i]["Type"]=="H E L":
                hh=['Name', 'Year', 'Type', 'Stan', 'Zas. wyd. bil. Razem', 'Zas. wyd. bil. A+B', 'Zas. wyd. bil. C', 'Wydobycie']
                h.append((temp[i]["Name"], temp[i]["Year"], temp[i]["Type"], temp[i]["More"]['Stan'],
                             temp[i]["More"]['Zas. wyd. bil. Razem'], temp[i]["More"]['Zas. wyd. bil. A+B'], temp[i]["More"]['Zas. wyd. bil. C'],
                             temp[i]["More"]['Wydobycie']))
                '''zas_wyd_bil_col = str(temp[i]["More"][headers[1]])
                zas_ab_col = str(temp[i]["More"][headers[2]])
                zas_c_col= str(temp[i]["More"][headers[3]])
                wyd_col = temp[i]["More"][headers[4]]
                zas_wyd_bil_col = zas_wyd_bil_col.replace(" ", "")
                zas_ab_col = zas_ab_col.replace(" ", "")
                wyd_col = wyd_col.replace(" ", "")
                if str(zas_wyd_bil_col[0]).isnumeric():
                    zas_wyd_bil += float(zas_wyd_bil_col)
                if str(zas_ab_col[0]).isnumeric():
                    zas_ab += float(zas_ab_col)
                if str(zas_c_col[0]).isnumeric():
                    zas_c+=float(zas_c_col)
                if wyd_col[0].isnumeric():
                    wyd += float(wyd_col)'''
                hel=True
            elif temp[i]["Type"]=="M E T A N  P O K Ł A D Ó W  W ĘG L A":
                hm=['Name', 'Year', 'Type', 'Stan', 'Zasoby wydobywalne bilansowe', 'Zasoby wydobywalne pozabilansowe', 'Zasoby przemyslowe', 'Emisja z wentylacja', 'Wydobycie']
                m.append((temp[i]["Name"], temp[i]["Year"], temp[i]["Type"], temp[i]["More"]['Stan'],
                          temp[i]["More"]['Zasoby wydobywalne bilansowe'], temp[i]["More"]['Zasoby wydobywalne pozabilansowe'], temp[i]["More"]['Zasoby przemyslowe'],
                          temp[i]["More"]['Emisja z wentylacja'], temp[i]["More"]['Wydobycie']))
                '''zas_wyd_bil_col = str(temp[i]["More"][headers[1]])
                zas_ab_col = str(temp[i]["More"][headers[2]])
                zas_c_col = str(temp[i]["More"][headers[3]])
                zas_przem_col = str(temp[i]["More"][headers[4]])
                wyd_col = temp[i]["More"][headers[5]]
                zas_wyd_bil_col = zas_wyd_bil_col.replace(" ", "")
                zas_ab_col = zas_ab_col.replace(" ", "")
                zas_c_col = zas_c_col.replace(" ", "")
                zas_przem_col = zas_przem_col.replace(" ", "")
                wyd_col = wyd_col.replace(" ", "")
                if str(zas_wyd_bil_col[0]).isnumeric():
                    zas_wyd_bil += float(zas_wyd_bil_col)
                if str(zas_ab_col[0]).isnumeric():
                    zas_ab += float(zas_ab_col)
                if str(zas_c_col[0]).isnumeric():
                    zas_c += float(zas_c_col)
                if zas_przem_col[0].isnumeric():
                    zas_przem += float(zas_przem_col)
                if wyd_col[0].isnumeric():
                    wyd += float(wyd_col)'''
                met = True
            elif temp[i]["Type"]=="WĘGLE  KAMIENNE":
                hw=['Name', 'Year', 'Type', 'Stan', 'Zasoby geologiczne bilansowe Razem', 'Zasoby geologiczne bilansowe A+B+C1', 'Zasoby wydobywalne bilansowe C2+D', 'Zasoby przemyslowe', 'Wydobycie']
                w.append((temp[i]["Name"], temp[i]["Year"], temp[i]["Type"], temp[i]["More"]['Stan'],
                             temp[i]["More"]['Zasoby geologiczne bilansowe Razem'], temp[i]["More"]['Zasoby geologiczne bilansowe A+B+C1'], temp[i]["More"]['Zasoby wydobywalne bilansowe C2+D'],
                             temp[i]["More"]['Zasoby przemyslowe'],temp[i]["More"]['Wydobycie']))
                '''zas_wyd_bil_col = str(temp[i]["More"]['Zasoby geologiczne bilansowe Razem'])
                zas_ab_col = str(temp[i]["More"]['Zasoby geologiczne bilansowe A+B+C1'])
                zas_c_col = str(temp[i]["More"]['Zasoby wydobywalne bilansowe C2+D'])
                zas_przem_col = str(temp[i]["More"]['Zasoby przemyslowe'])
                wyd_col = str(temp[i]["More"]['Wydobycie'])
                zas_wyd_bil_col = zas_wyd_bil_col.replace(" ", "")
                zas_ab_col = zas_ab_col.replace(" ", "")
                zas_c_col=zas_c_col.replace(" ", "")
                zas_przem_col = zas_przem_col.replace(" ", "")
                wyd_col = wyd_col.replace(" ", "")
                if str(zas_wyd_bil_col[0]).isnumeric():
                    zas_wyd_bil += float(zas_wyd_bil_col)
                if str(zas_ab_col[0]).isnumeric():
                    zas_ab += float(zas_ab_col)
                if str(zas_c_col[0]).isnumeric():
                    zas_c += float(zas_c_col)
                if zas_przem_col[0].isnumeric():
                    zas_przem += float(zas_przem_col)
                if wyd_col[0].isnumeric():
                    wyd += float(wyd_col)'''
                coal=True

            elif temp[i]["Type"]=="SOLANKI, WODY LECZNICZE I TERMALNE":
                h_sol=['Name', 'Year', 'Type', 'Typ wody', 'Zasoby geologiczne bilansowe dyspozycyjne', 'Zasoby geologiczne bilansowe eksploatacyjne', 'Pobor', 'Powiat']
                s.append((temp[i]["Name"], temp[i]["Year"], temp[i]["Type"], temp[i]["More"][headers[0]],
                             temp[i]["More"][headers[1]], temp[i]["More"][headers[2]], temp[i]["More"][headers[3]],
                             temp[i]["More"][headers[4]]))


            else:
                h_all=['Name', 'Year', 'Type', 'Stan', 'Zasoby wydobywalne bilansowe', 'Zasoby przemyslowe', 'Wydobycie', 'Powiat']
                data.append((temp[i]["Name"],temp[i]["Year"],temp[i]["Type"],temp[i]["More"]['Stan'],temp[i]["More"]['Zasoby wydobywalne bilansowe'],temp[i]["More"]['Zasoby przemyslowe'],temp[i]["More"]['Wydobycie'],temp[i]["More"]['Powiat']))
                '''zas_wyd_bil_col=str(temp[i]["More"]['Zasoby wydobywalne bilansowe'])
                zas_przem_col=str(temp[i]["More"]['Zasoby przemyslowe'])
                wyd_col=str(temp[i]["More"]['Wydobycie'])
                zas_wyd_bil_col=zas_wyd_bil_col.replace(" ","")
                zas_przem_col=zas_przem_col.replace(" ","")
                wyd_col = wyd_col.replace(" ", "")
                if zas_wyd_bil_col[0].isnumeric():
                    zas_wyd_bil+=float(zas_wyd_bil_col)
                if zas_przem_col[0].isnumeric():
                    zas_przem+=float(zas_przem_col)
                if wyd_col[0].isnumeric():
                    wyd+=float(wyd_col)'''
        ret = [data, h, w, s, m]
        heads=[]
        for i in range(10):
            if [] in ret:
                ret.remove([])
        if data in ret:
            heads.append(h_all)
        if h in ret:
            heads.append(hh)
        if w in ret:
            heads.append(hw)
        if s in ret:
            heads.append(h_sol)
        if m in ret:
            heads.append(hm)

        return ret,heads
