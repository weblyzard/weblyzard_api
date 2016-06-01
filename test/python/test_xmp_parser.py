

class TestParser(unittest.TestCase):

    def test_scientific_notation_bug(self):
        '''
        make sure that a decoding bug for strings in scientific notation yielding infinity doesn't occur
        '''
        import hashlib

        m = hashlib.md5()
        m.update(
            "\"That triumph for more military spending was an anomaly in the budget blueprint, which would cut spending $5.5 trillion over the next decade.")
        md5sum = m.hexdigest()
        expected = '3120900866903065837e521458088467'
        self.assertEqual(md5sum, expected)
        self.assertEqual(XMLParser.decode_value(md5sum), expected)


if __name__ == '__main__':
    unittest.main()