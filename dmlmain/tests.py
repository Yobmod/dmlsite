from django.test import TestCase
#unittest / unittest2
#doctest

class MainViewsTestCase(TestCase):
	def test_homepage(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 200)
