import unittest

from trac.test import EnvironmentStub
from tracgate.util import *

class UtilTestCase(unittest.TestCase):
    def setUp(self):
        self.env = EnvironmentStub()
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

    def test_find_sid_by_email(self):
        self.assertEquals(
            'rcorsaro',
            find_sid_by_email(self.env, 'rcorsaro@optaros.com')
        )
        self.assertEquals(
            'rcorsaro',
            find_sid_by_email(
                self.env, 
                '"Robert Corsaro" <rcorsaro@optaros.com>'
            )
        )
        self.assertEquals(
            'rcorsaro',
            find_sid_by_email(
                self.env, 
                'Robert Corsaro <rcorsaro@optaros.com>'
            )
        )
        self.assertEquals(
            'jblow@optaros.com',
            find_sid_by_email(
                self.env, 
                'Joe Blow <jblow@optaros.com>'
            )
        )
        self.assertEquals(
            'csutton',
            find_sid_by_email(
                self.env, 
                'Joe Blow <csutton@hotmail.com>'
            )
        )



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UtilTestCase, 'test'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
        
