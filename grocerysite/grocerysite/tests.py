from django.test import RequestFactory, TestCase
from grocerysite.views import index, search, search_result

from grocerysite.load_data import load_model
import os


class SearchResultsTestCase(TestCase):
    """
    for testing search results to see if they return correct 200 response
    also tests to see if search for "banana" returns page with "Banana" 
    """
    def setUp(self):
        # call custom function to load test database
        load_model('Product', 'grocerysite/data/products_data.csv', silent=True)
        self.factory = RequestFactory()

    def test_search(self):
        """
        test if search results object exists for "Banana"
        """
        request = self.factory.get('search_result', data={'q':'fruit'})
        response = search_result(request)
        
        # perform checks

        # check that successful response was generated
        self.assertEqual(response.status_code, 200)

        # check that final html document is non-empty
        self.assertTrue(response.content.find(b'fruit') != -1)


class StaticTestCase(TestCase):
    """
    For testing pages with content that doesn't change
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_index(self):
        request = self.factory.get('index')
        response = index(request)

        # check that successful response was generated
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        request = self.factory.get('search')
        response = search(request)

        # check that successful response was generated
        self.assertEqual(response.status_code, 200)

