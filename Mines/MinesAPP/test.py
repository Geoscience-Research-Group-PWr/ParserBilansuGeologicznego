import unittest
import pymongo
from bson import ObjectId

from models import Database

class DBTestCase(unittest.TestCase):

    def test_name_search(self):
        db=Database()
        maxyear = 0
        minyear = 10000
        r1 = db.search_by_name("Górka Lubartowska",'2010','2015')
        r2 = db.search_by_name("Czeszów")
        r3 = db.search_by_name("")
        for items in r1:
            if int(items['Year']) >= maxyear:
                maxyear = int(items['Year'])
            if int(items['Year']) <= minyear:
                minyear = int(items['Year'])
        self.assertEqual(r1,[{'_id': ObjectId('660f1249e59ff5d144a6d9e7'), 'Name': 'Górka Lubartowska', 'Year': '2010', 'Type': 'BURSZTYNY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '1 088', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f124ae4d2a2dbf7034464'), 'Name': 'Górka Lubartowska', 'Year': '2012', 'Type': 'BURSZTYNY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '1 088', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f124adf74c1126280df31'), 'Name': 'Górka Lubartowska', 'Year': '2015', 'Type': 'BURSZTYNY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '1 088', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f124abee1883e29a57d3e'), 'Name': 'Górka Lubartowska', 'Year': '2013', 'Type': 'BURSZTYNY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '1 088', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f124a3626cf532f25b389'), 'Name': 'Górka Lubartowska', 'Year': '2011', 'Type': 'BURSZTYNY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '1 088', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f124aa801a9cfc3eb2fe9'), 'Name': 'Górka Lubartowska', 'Year': '2014', 'Type': 'BURSZTYNY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '1 088', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f130ddf74c1126280e476'), 'Name': 'Górka Lubartowska', 'Year': '2015', 'Type': 'PIASKI FORMIERSKIE', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '10 363.00', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f1312bee1883e29a58282'), 'Name': 'Górka Lubartowska', 'Year': '2013', 'Type': 'PIASKI FORMIERSKIE', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '10 363', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f1313e4d2a2dbf703499b'), 'Name': 'Górka Lubartowska', 'Year': '2012', 'Type': 'PIASKI FORMIERSKIE', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '10 363', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f132ca801a9cfc3eb35cc'), 'Name': 'Górka Lubartowska', 'Year': '2014', 'Type': 'PIASKI FORMIERSKIE', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '10 363', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f13b7e59ff5d144a6e3af'), 'Name': 'Górka Lubartowska', 'Year': '2010', 'Type': 'PIASKI I ŻWIRY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '102 412', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f13d3df74c1126280e9cf'), 'Name': 'Górka Lubartowska', 'Year': '2015', 'Type': 'PIASKI I ŻWIRY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '102 412', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f13d9bee1883e29a587c3'), 'Name': 'Górka Lubartowska', 'Year': '2013', 'Type': 'PIASKI I ŻWIRY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '102 412', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f13db3626cf532f25bdaa'), 'Name': 'Górka Lubartowska', 'Year': '2011', 'Type': 'PIASKI I ŻWIRY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '102 412', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f13dce4d2a2dbf7034ec3'), 'Name': 'Górka Lubartowska', 'Year': '2012', 'Type': 'PIASKI I ŻWIRY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '102 412', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}, {'_id': ObjectId('660f13f8a801a9cfc3eb3b20'), 'Name': 'Górka Lubartowska', 'Year': '2014', 'Type': 'PIASKI I ŻWIRY', 'More': {'Stan': 'P', 'Zasoby wydobywalne bilansowe': '102 412', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubartowski'}}])
        self.assertEqual(type(r1),list)
        self.assertEqual(type(r1[0]),dict)
        self.assertLessEqual(maxyear,2015)
        self.assertGreaterEqual(minyear,2010)
        self.assertNotEqual(r2,[])
        self.assertEqual(r3,[])

    def test_type_search(self):
        db = Database()
        maxyear = 0
        minyear = 10000
        r1 = db.search_by_type("ŻWIRKI FILTRACYJNE",'2021','2021')
        r2 = db.search_by_type("ŻWIRKI FILTRACYJNE")
        r3 = db.search_by_type("")
        for items in r1:
            if int(items['Year']) >= maxyear:
                maxyear = int(items['Year'])
            if int(items['Year']) <= minyear:
                minyear = int(items['Year'])
        self.assertEqual(r1,[{'_id': ObjectId('660f1f13d6f8c7ba90e730bf'), 'Name': 'Nowy Dwór Wejherowski', 'Year': '2021', 'Type': 'ŻWIRKI FILTRACYJNE', 'More': {'Stan': 'R', 'Zasoby wydobywalne bilansowe': '101', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'wejherowski'}}, {'_id': ObjectId('660f1f13d6f8c7ba90e730c0'), 'Name': 'Panoszów', 'Year': '2021', 'Type': 'ŻWIRKI FILTRACYJNE', 'More': {'Stan': 'R', 'Zasoby wydobywalne bilansowe': '172', 'Zasoby przemyslowe': '-', 'Wydobycie': '-', 'Powiat': 'lubliniecki'}}])
        self.assertEqual(type(r1), list)
        self.assertEqual(type(r1[0]), dict)
        self.assertLessEqual(maxyear, 2021)
        self.assertGreaterEqual(minyear, 2021)
        self.assertNotEqual(r2, [])
        self.assertEqual(r3, [])
if __name__ == '__main__' :
    unittest.main()