import server
import unittest


class FlaskServerTestCase(unittest.TestCase):
    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        self.assertTrue("Anonymization Tool" in resp.data)
        resp = self.app.post('/import.html')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.data)
        self.assertTrue("Not Allowed" in resp.data)

    def test_categorization2python(self):
        resp = self.app.get('/_categorization2python')
        self.assertNotEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        resp = self.app.get('/_categorization2python', data={
            'attrCategorization': ""
        })
        self.assertNotEqual(resp.status_code, 200)
        self.assertTrue(resp.data)

    def test_getkanonresult(self):
        resp = self.app.get('/getkanonresult')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        resp = self.app.get('/getkanonresult', data={
            'attributes': ""
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        resp = self.app.post('/getkanonresult', data={
            'attributes': ""
        })
        self.assertNotEqual(resp.status_code, 200)
        self.assertTrue(resp.data)

    def test_python2array(self):
        resp = self.app.get('/_python2array')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        resp = self.app.get('/_python2array', data={
            'attributes': ""
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        resp = self.app.post('/getkanonresult')
        self.assertNotEqual(resp.status_code, 200)
        self.assertTrue(resp.data)

    def test_import(self):
        resp = self.app.get('/import.html')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        self.assertTrue("import" in resp.data)
        resp = self.app.post('/import.html')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.data)
        self.assertTrue("Not Allowed" in resp.data)
        resp = self.app.get('/import')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.data)
        self.assertTrue("Not Found" in resp.data)

    def test_anonymize(self):
        resp = self.app.get('/anonymize.html')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        self.assertTrue("anonymize" in resp.data)
        resp = self.app.post('/anonymize.html')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.data)
        self.assertTrue("Not Allowed" in resp.data)
        resp = self.app.get('/anonymize')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.data)
        self.assertTrue("Not Found" in resp.data)

    def test_results(self):
        resp = self.app.get('/results.html')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        self.assertTrue("Preview" in resp.data)
        resp = self.app.post('/results.html')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.data)
        self.assertTrue("Not Allowed" in resp.data)
        resp = self.app.get('/results')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.data)
        self.assertTrue("Not Found" in resp.data)

    def test_export(self):
        resp = self.app.get('/export.html')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        self.assertTrue("Export" in resp.data)
        resp = self.app.post('/export.html')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.data)
        self.assertTrue("Not Allowed" in resp.data)
        resp = self.app.get('/export')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.data)
        self.assertTrue("Not Found" in resp.data)

    def test_download(self):
        resp = self.app.get('/download')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        resp = self.app.post('/download')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.data)
        self.assertTrue("Not Allowed" in resp.data)

    def test_postcsv(self):
        resp = self.app.get('/postcsv')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.data)
        self.assertTrue("Not Allowed" in resp.data)
        resp = self.app.post('/postcsv')
        self.assertNotEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        resp = self.app.post('/postcsv', data={
            'file': ""
        })
        self.assertNotEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        resp = self.app.post('/postcsv', data={
            'file': "/dataset/origin.csv"
        })
        self.assertNotEqual(resp.status_code, 200)
        self.assertTrue(resp.data)

    def test_user_query(self):
        resp = self.app.get('/userQuery')
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(resp.data)
        self.assertTrue("Not Allowed" in resp.data)
        resp = self.app.post('/userQuery')
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.data)
        resp = self.app.post('/userQuery', data={
            'query': ""
        })
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data)
        self.assertTrue('null' in resp.data)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
