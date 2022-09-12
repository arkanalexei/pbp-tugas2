from django.test import TestCase
from django.test import Client

# Create your tests here.
class UnitTest(TestCase):

    def test_katalog_is_exist(self):
        response  = Client().get('/katalog/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/katalog/')
        self.assertTemplateUsed(response, 'katalog.html')