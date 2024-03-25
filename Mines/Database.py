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
        temp=results[0]
        data=[(temp[0]["name"],temp[0]["year"],temp[0]["type"],temp[0]["more"][headers[0]],temp[0]["more"][headers[1]],temp[0]["more"][headers[2]],temp[0]["more"][headers[3]],temp[0]["more"][headers[4]])]
        return data

