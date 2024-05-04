import pymongo
import datetime


class Database:
    """
    MongoDB operations module.
    """

    def __init__(self):
        self.connection = pymongo.MongoClient(
            'mongodb+srv://mikolajsiewruk222:parser420@parser.1gvwkzh.mongodb.net/?retryWrites=true&w=majority&appName=parser')
        self.db = self.connection['parser']
        self.collection = self.db['Kopalnie']

    def search_by_name(self, name: str, start=0, end=datetime.date.today().year, county="") -> list:
        """
        Querying by mine name.
        :param name: name of a mine
        :param start:
        :param end:
        :param county:
        :return: list of objects from the database searched by name in range given by start and end years.
        """
        result = []
        if county:
            query = {"$and": [{"Name": name}, {"More.Powiat": county}, {"Year": {"$gte": str(start)}},
                              {"Year": {"$lte": str(end)}}]}
        else:
            query = {"$and": [{"Name": name}, {"Year": {"$gte": str(start)}}, {"Year": {"$lte": str(end)}}]}
        output = self.collection.find(query)
        for results in output:
            result.append(results)
        return result

    def search_by_type(self, t: str, start=0, end=datetime.date.today().year) -> list:
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

    def search_by_county(self, county: str, start=0, end=datetime.date.today().year) -> list:
        """
        Querying by a given county
        :param county:
        :param start:
        :param end:
        :return: list of objects where county field contains given county
        """
        result = []
        query = {"$and": [{"More.Powiat": county}, {"Year": {"$gte": str(start)}}, {"Year": {"$lte": str(end)}}]}
        output = self.collection.find(query)
        for results in output:
            result.append(results)
        return result

    def get_data(self, results: list, headers: list) -> tuple:
        """
        Retrieving row data from searching
        :param results: list of results from searching
        :param headers: list of column headers
        :return: tuple(list,list)
        """
        data = []

        for i in range(len(results[0])):
            temp = results[0]
            h_all = ['Name', 'Year', 'Type', 'Stan', 'Zasoby wydobywalne bilansowe', 'Zasoby przemyslowe', 'Wydobycie',
                     'Powiat']
            data.append((temp[i]["Name"], temp[i]["Year"], temp[i]["Type"], temp[i]["More"]['Stan'],
                         temp[i]["More"]['Zasoby wydobywalne bilansowe'], temp[i]["More"]['Zasoby przemyslowe'],
                         temp[i]["More"]['Wydobycie'], temp[i]["More"]['Powiat']))
        ret = [data]
        heads = []
        for i in range(10):
            if [] in ret:
                ret.remove([])
        if data in ret:
            heads.append(h_all)

        return ret, heads

    def statistics(self, results: list, start: str, end: str) -> tuple:
        """
        Get chart data from query results.
        :param results:
        :param start:
        :param end:
        :return: (years,sums)
        """
        temp = results[0]
        sums = []
        years = [i for i in range(int(start), int(end) + 1)]
        y = int(start)
        j = 0
        while j < len(years):
            s_temp = 0
            for i in range(len(temp)):
                if int(temp[i]["Year"]) == y:
                    wyd_column = str(temp[i]["More"]["Wydobycie"])
                    wyd_column = wyd_column.replace(" ", "")
                    if wyd_column[0].isnumeric():
                        try:
                            s_temp += float(wyd_column)
                        except ValueError:
                            pass
                    else:
                        s_temp += 0
            sums.append(round(s_temp, 4))
            y += 1
            j += 1
        d = {"Years": years, "Sums": sums}
        mean=round(sum(sums)/len(years),2)
        return years, sums, mean


