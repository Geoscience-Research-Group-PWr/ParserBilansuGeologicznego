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
        s=0 # suma wydobycia
        for i in range(len(results[0])):
            temp=results[0]
            data.append((temp[i]["name"],temp[i]["year"],temp[i]["type"],temp[i]["more"][headers[0]],temp[i]["more"][headers[1]],temp[i]["more"][headers[2]],temp[i]["more"][headers[3]],temp[i]["more"][headers[4]]))
            a=temp[i]["more"][headers[1]]
            a=a.replace(" ","")
            if a.isnumeric():
                s+=float(a)
            else:
                s+=0
        return data,s

