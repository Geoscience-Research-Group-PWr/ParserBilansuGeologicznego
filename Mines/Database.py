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

    def search_by_name(self,name:str,start=0,end=datetime.date.today().year):
        """
        Querying by mine name.
        :param t: name of a mine
        :param start:
        :param end:
        :return: list of objects from the database searched by name in range given by start and end years.
        """
        result=[]
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
    def get_data(self,results:list,headers:list)->tuple:
        """
        Retrieving row data from searching
        :param results: list of results from searching
        :param headers: list of column headers
        :return: tuple(list,float,float,float)
        """
        data=[]
        zas_wyd_bil=0 # suma zasobów wydobywalnych bilansowych
        zas_przem=0
        wyd=0
        zas_ab=0
        zas_c=0
        hel=False
        coal=False
        water=False
        # naprawić dla wyjątków
        # naprawić dla kopalni o różnych kopalinach zwłaszcza nieregularnych, najlepiej dla każdej kopaliny osobną tabelę bo to nie ma sensu inaczej
        # fml
        print(len(results[0]))
        for i in range(len(results[0])):
            temp=results[0]
            if temp[i]["Type"]=="H E L":
                data.append((temp[i]["Name"], temp[i]["Year"], temp[i]["Type"], temp[i]["More"][headers[0]],
                             temp[i]["More"][headers[1]], temp[i]["More"][headers[2]], temp[i]["More"][headers[3]],
                             temp[i]["More"][headers[4]]))
                zas_wyd_bil_col = str(temp[i]["More"][headers[1]])
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
                    wyd += float(wyd_col)
                hel=True

            elif temp[i]["Type"]=="WĘGLE  KAMIENNE" or temp[i]["Type"]=="METAN POKŁADÓW WĘGLA":
                print(headers)
                data.append((temp[i]["Name"], temp[i]["Year"], temp[i]["Type"], temp[i]["More"][headers[0]],
                             temp[i]["More"][headers[1]], temp[i]["More"][headers[2]], temp[i]["More"][headers[3]],
                             temp[i]["More"][headers[4]],temp[i]["More"][headers[5]]))
                zas_wyd_bil_col = str(temp[i]["More"][headers[1]])
                zas_ab_col = str(temp[i]["More"][headers[2]])
                zas_c_col = str(temp[i]["More"][headers[3]])
                zas_przem_col = str(temp[i]["More"][headers[4]])
                wyd_col = temp[i]["More"][headers[5]]
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
                    wyd += float(wyd_col)
                coal=True

            elif temp[i]["Type"]=="SOLANKI, WODY LECZNICZE I TERMALNE":
                data.append((temp[i]["Name"], temp[i]["Year"], temp[i]["Type"], temp[i]["More"][headers[0]],
                             temp[i]["More"][headers[1]], temp[i]["More"][headers[2]], temp[i]["More"][headers[3]],
                             temp[i]["More"][headers[4]]))
                zas_wyd_bil_col = str(temp[i]["More"][headers[1]])
                zas_ab_col = str(temp[i]["More"][headers[2]])
                zas_c_col = str(temp[i]["More"][headers[3]])
                wyd_col = str(temp[i]["More"][headers[4]])
                zas_wyd_bil_col = zas_wyd_bil_col.replace(" ", "")
                zas_ab_col = zas_ab_col.replace(" ", "")
                zas_c_col = zas_c_col.replace(" ", "")
                wyd_col = wyd_col.replace(" ", "")
                if str(zas_wyd_bil_col[0]).isnumeric():
                    zas_wyd_bil += float(zas_wyd_bil_col)
                if str(zas_ab_col[0]).isnumeric():
                    zas_ab += float(zas_ab_col)
                if str(zas_c_col[0]).isnumeric():
                    zas_c += float(zas_c_col)
                if wyd_col[0].isnumeric():
                    wyd += float(wyd_col)
                water=True

            else:
                data.append((temp[i]["Name"],temp[i]["Year"],temp[i]["Type"],temp[i]["More"][headers[0]],temp[i]["More"][headers[1]],temp[i]["More"][headers[2]],temp[i]["More"][headers[3]],temp[i]["More"][headers[4]]))
                zas_wyd_bil_col=str(temp[i]["More"][headers[1]])
                zas_przem_col=str(temp[i]["More"][headers[2]])
                wyd_col=str(temp[i]["More"][headers[3]])
                zas_wyd_bil_col=zas_wyd_bil_col.replace(" ","")
                zas_przem_col=zas_przem_col.replace(" ","")
                wyd_col = wyd_col.replace(" ", "")
                if zas_wyd_bil_col[0].isnumeric():
                    zas_wyd_bil+=float(zas_wyd_bil_col)
                if zas_przem_col[0].isnumeric():
                    zas_przem+=float(zas_przem_col)
                if wyd_col[0].isnumeric():
                    wyd+=float(wyd_col)
        if hel:
            return data,zas_wyd_bil,zas_ab,zas_c,wyd
        elif coal:
            return data,zas_wyd_bil,zas_ab,zas_c,zas_przem,wyd
        elif water:
            print("water")
            return data,zas_wyd_bil,zas_ab,zas_c,wyd
        else:
            return data,zas_wyd_bil,zas_przem,wyd