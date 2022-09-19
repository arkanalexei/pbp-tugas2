from django.test import TestCase
from django.test import Client

# Create your tests here.
class UnitTest(TestCase):

    def test_mywatchlist_is_exist(self):
        response  = Client().get('/mywatchlist/')
        self.assertEqual(response.status_code, 200)
    
    def test_mywatchlist_html_is_exist(self):
        response  = Client().get('/mywatchlist/html/')
        self.assertEqual(response.status_code, 200)
    
    def test_mywatchlist_json_is_exist(self):
        response  = Client().get('/mywatchlist/json/')
        self.assertEqual(response.status_code, 200)
    
    def test_mywatchlist_xml_is_exist(self):
        response  = Client().get('/mywatchlist/xml/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/mywatchlist/')
        self.assertTemplateUsed(response, 'mywatchlist.html')