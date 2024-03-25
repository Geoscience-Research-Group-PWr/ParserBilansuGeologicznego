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

s=Database()
res=s.search("Jedlinka",2010,2024)

print(res)
