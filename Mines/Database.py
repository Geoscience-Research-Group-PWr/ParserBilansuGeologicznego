import pymongo
import datetime

class Database:
    def __init__(self):
        self.connection=pymongo.MongoClient('mongodb+srv://mikolajsiewruk222:parser420@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority&appName=parser')
        self.db=self.connection['parser']
        self.collection=self.db['Kopalnie']

    def search_by_name(self,name,start=0,end=datetime.date.today().year):
        result=[]
        query={"$and":[{"Name":name},{"Year":{"$gte":str(start)}},{"Year":{"$lte":str(end)}}]}
        output=self.collection.find(query)
        for results in output:
            result.append(results)
        return result

    def search_by_type(self,t,start=0,end=datetime.date.today().year):
        result = []
        query = {"$and": [{"ype": t}, {"Year": {"$gt": str(start)}}, {"Year": {"$lt": str(end)}}]}
        output = self.collection.find(query)
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
            data.append((temp[i]["Name"],temp[i]["Year"],temp[i]["Type"],temp[i]["More"][headers[0]],temp[i]["More"][headers[1]],temp[i]["More"][headers[2]],temp[i]["More"][headers[3]],temp[i]["More"][headers[4]]))
            zas_wyd_bil_col=temp[i]["More"][headers[1]]
            zas_przem_col=temp[i]["More"][headers[2]]
            wyd_col=temp[i]["More"][headers[3]]
            zas_wyd_bil_col=zas_wyd_bil_col.replace(" ","")
            zas_przem_col=zas_przem_col.replace(" ","")
            wyd_col = wyd_col.replace(" ", "")
            if zas_wyd_bil_col[0].isnumeric():
                zas_wyd_bil+=float(zas_wyd_bil_col)
            if zas_przem_col[0].isnumeric():
                zas_przem+=float(zas_przem_col)
            if wyd_col[0].isnumeric():
                wyd+=float(wyd_col)
        return data,zas_wyd_bil,zas_przem,wyd