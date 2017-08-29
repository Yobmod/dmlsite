from django.conf import settings
from django.test.testcases import TestCase
import re
from urllib.parse import urlsplit, urljoin

class GenericTestCase( TestCase ):
	fixtures = []

	def test_links( self ):
		self.p1 = re.compile( r'href="([^"]*)"' )
		self.p2 = re.compile( r"href='([^']*)'" )
		self.visited_urls = set()
		self.visit( '/', 0 )

	def visit( self, url, depth ):
		print( '-' * depth + url ),
		self.visited_urls.add( url )
		response = self.client.get( url, follow=True )
		if response.redirect_chain:
			url = urlsplit( response.redirect_chain[-1][0] ).path
			print( ' => ' + url )
			if url in self.visited_urls:
				return
			self.visited_urls.add( url )
		else:
			print( '' )

		self.assertEquals( response.status_code, 200 )

		refs = self.get_refs( response.content )
		for relative_url in refs:
			absolute_url = urljoin( url, relative_url )
			if not self.skip_url( absolute_url, relative_url ):
				self.visit( absolute_url, depth + 1 )

	def skip_url( self, absolute_url, relative_url ):
		return absolute_url in self.visited_urls \
			or  ':' in absolute_url \
			or absolute_url.startswith( settings.STATIC_URL ) \
			or relative_url.startswith( '#' )

	def get_refs( self, text ):
		urls = set()
		urls.update( self.p1.findall( text.decode('UTF-8') ) )
		urls.update( self.p2.findall( text.decode('UTF-8') ) )
		return urls
