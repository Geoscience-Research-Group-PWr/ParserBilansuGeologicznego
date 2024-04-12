import unittest

from models import XD,Database

class XDTestCase(unittest.TestCase):
    def test_s(self):
        a = 5
        b = 6
        s=XD()
        result = s.s(a,b)
        self.assertEqual(result,11)

    def test_database(self):
        a = 6
        b = 5
        db=Database()
        result=db.sum(a,b)
        self.assertEqual(result,11)

if __name__ == '__main__' :
    unittest.main()