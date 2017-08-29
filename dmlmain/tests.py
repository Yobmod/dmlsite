from django.test import TestCase
#import unittest
#doctest
#nose

class MainViewsTestCase(TestCase):
	def test_homepage(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 200)

from django.urls import reverse
from .urls import urlpatterns

class UrlsTest(TestCase):

	def test_responses(self):
		for pattern in urlpatterns:
			if hasattr(pattern, "name") and pattern.name:
				response = self.client.get(reverse(pattern.name))
				print(str(pattern) + str(response.status_code))
			else:
				print(str(pattern) + "skipped")
			allowed_codes = [200, 302,]
			""" 200: httpresponse, 302:httpredirect """
			self.assertTrue(response.status_code in allowed_codes)



# from django.conf import settings
# from django.test.testcases import TestCase
# import re
# from urllib.parse import urlsplit, urljoin
#
# class GenericTestCase( TestCase ):
# 	fixtures = []
#
# 	def test_links( self ):
# 		self.p1 = re.compile( r'href="([^"]*)"' )
# 		self.p2 = re.compile( r"href='([^']*)'" )
# 		self.visited_urls = set()
# 		self.visit( '/', 0 )
#
# 	def visit( self, url, depth ):
# 		print( '-' * depth + url ),
# 		self.visited_urls.add( url )
# 		response = self.client.get( url, follow=True )
# 		if response.redirect_chain:
# 			url = urlsplit( response.redirect_chain[-1][0] ).path
# 			print( ' => ' + url )
# 			if url in self.visited_urls:
# 				return
# 			self.visited_urls.add( url )
# 		else:
# 			print( '' )
#
# 		self.assertEquals( response.status_code, 200 )
#
# 		refs = self.get_refs( response.content )
# 		for relative_url in refs:
# 			absolute_url = urljoin( url, relative_url )
# 			if not self.skip_url( absolute_url, relative_url ):
# 				self.visit( absolute_url, depth + 1 )
#
# 	def skip_url( self, absolute_url, relative_url ):
# 		return absolute_url in self.visited_urls \
# 			or  ':' in absolute_url \
# 			or absolute_url.startswith( settings.STATIC_URL ) \
# 			or relative_url.startswith( '#' )
#
# 	def get_refs( self, text ):
# 		urls = set()
# 		urls.update( self.p1.findall( text.decode('UTF-8') ) )
# 		urls.update( self.p2.findall( text.decode('UTF-8') ) )
# 		return urls
