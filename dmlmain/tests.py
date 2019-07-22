from django.test import TestCase
from django.urls import reverse
from .urls import urlpatterns

# unittest / unittest2
# doctest
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.utils.translation import activate


class MainViewsTestCase(TestCase):
    def test_homepage(self) -> None:
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)


class UrlsTest(TestCase):
    def test_responses(self) -> None:
        allowed_codes = [200, 302]
        """ 200: httpresponse, 302:httpredirect """
        for pattern in urlpatterns:
            if hasattr(pattern, "name") and pattern.name:
                response = self.client.get(reverse(pattern.name))
                print(pattern.name, response.status_code)
                self.assertTrue(response.status_code in allowed_codes)
            else:
                print(str(pattern) + "skipped")

    def test_page_not_found_response(self) -> None:
        """404: PageNotFound"""
        resp = self.client.get("/this_page_should_not_exist/")
        self.assertEqual(resp.status_code, 404)


