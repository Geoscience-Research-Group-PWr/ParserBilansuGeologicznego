import pymongo
import datetime

class Database:
    def __init__(self):
        self.connection=pymongo.MongoClient('mongodb+srv://mikolajsiewruk222:Mikis2003@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority&appName=parser')
        self.db=self.connection['parser']
        self.collection=self.db['Kopalnie']

    def search(self,name,start=0,end=datetime.date.today().year):
        result=[]
        query={"$and":[{"name":name},{"year":{"$gt":f'{start}'}},{"year":{"$lt":f'{end}'}}]}
        output=self.collection.find(query)
        for results in output:
            result.append(results)
        return result
    def get_data(self,results,headers):
        data=[]
        zas_wyd_bil=0 # suma zasobów wydobywalnych bilansowych
        zas_przem=0
        wyd=0
        for i in range(len(results[0])):
            temp=results[0]
            data.append((temp[i]["name"],temp[i]["year"],temp[i]["type"],temp[i]["more"][headers[0]],temp[i]["more"][headers[1]],temp[i]["more"][headers[2]],temp[i]["more"][headers[3]],temp[i]["more"][headers[4]]))
            zas_wyd_bil_col=temp[i]["more"][headers[1]]
            zas_przem_col=temp[i]["more"][headers[2]]
            wyd_col=temp[i]["more"][headers[3]]
            zas_wyd_bil_col=zas_wyd_bil_col.replace(" ","")
            zas_przem_col=zas_przem_col.replace(" ","")
            wyd_col = wyd_col.replace(" ", "")
            if zas_wyd_bil_col.isnumeric():
                zas_wyd_bil+=float(zas_wyd_bil_col)
            if zas_przem_col.isnumeric():
                zas_przem+=float(zas_przem_col)
            if wyd_col.isnumeric():
                wyd+=float(wyd_col)
        return data,zas_wyd_bil,zas_przem,wyd

