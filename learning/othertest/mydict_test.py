import unittest
from mydict import Dict

class TestDict(unittest.TestCase):
    '''test of Dict'''
    def setUp(self):
        print('setup...')
    def tearDown(self):
        print('tear_down...')
    def test_init(self):
        d=Dict(a=1,b='value')
        self.assertEqual(d.a,1)
        self.assertEqual(d.b,'value')
        self.assertTrue(d,dict)

    def test_key(self):
        d=Dict()
        d['key'] = 'value'
        self.assertEqual(d.key,'value')
        self.assertEqual(d['key'],'value')

    def test_attr(self):
        d=Dict()
        d['key'] = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'],'value')
    def test_keyerror(self):
        d=Dict()
        with self.assertRaises(KeyError):
            value=d['empty']
    def test_keyerrot(self):
        d=Dict()
        with self.assertRaises(AttributeError):
            value=d.empty


if __name__=='__main__':
     unittest.main()
