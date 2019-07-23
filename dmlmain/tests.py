from django.test import TestCase
from django.urls import reverse
from .urls import urlpatterns
from .tasks import create_html_report
# unittest / unittest2
# doctest
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.utils.translation import activate


class MainViewsTestCase(TestCase):
    """for texting specific dmlmain views from their url"""
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


class TaskTest(TestCase):
    def test_create_html_report(self) -> None:
        report = create_html_report()
        assert isinstance(report, str) and len(report) > 0

