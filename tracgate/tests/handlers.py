import unittest

from trac.test import EnvironmentStub
from tracgate.handlers import *

class HandlersTestCase(unittest.TestCase):
    def setUp(self):
        self.env = EnvironmentStub()
        self.out = TracGateTicketEmailHandler(self.env)
        emailmap = {
            'rcorsaro': 'rcorsaro@optaros.com',
            'doki_pen': 'doki_pen@doki-pen.org',
            'csutton': 'csutton@hotmail.com',
            'rreimer': 'rreimer@yahoo.com'
        }
        db = self.env.get_db_cnx()
        cursor = db.cursor()
        for k, v in emailmap.iteritems():
            cursor.execute("""
        INSERT INTO session_attribute (sid, name, value) 
             VALUES (%s, 'email', %s)
            """, (k, v))

    def test_find_fields(self):
        l = list(self.out._find_fields("""
        @a b
        @c ddd ddd ddd
        lsjdf
        sldkjf
        @again do it
        """))
        self.assertEquals(3, len(l))

    def test_strip_fields(self):
        o = self.out._strip_fields("""
        @a b
        @c ddd ddd ddd
        lsjdf
        sldkjf
        @again do it
        """)
        print o
        self.assertEquals(3, len(o.split("\n")))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(HandlersTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
        
