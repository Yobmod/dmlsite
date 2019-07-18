# from django.contrib.auth import get_user_model
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpRequest,
)  # , FileResponse, Http404,
from django.shortcuts import render
from django.views.generic import View, TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.contrib.staticfiles.templatetags.staticfiles import static

# from random import randint
import arrow
from chartjs.views.lines import BaseLineChartView
from django.contrib.auth.models import User

from typing import List, Any, Dict
# from django.db.models.query import QuerySet
# from django.template import Context
# from django.db.models import Model


# User = get_user_model()


class HomeView(View):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, "research.html")


def poster_view(request: HttpRequest) -> HttpResponse:
    # try:
    # 	return FileResponse(open('/static/poster.pdf', 'rb'), content_type='application/pdf')
    # except FileNotFoundError:
    # 	raise Http404()
    # file_path = staticfiles_storage.url('Poster.txt')
    # file_path = staticfiles_storage.url(os.path.join(BASE_DIR, 'static_root/Poster.pdf'))
    # file_path = static('dmlresearch/static/Poster.pdf')
    with open("Poster.pdf", "rb") as pdf:
        response = HttpResponse(pdf.read(), content_type="application/pdf")
        response["Content-Disposition"] = "inline;filename=poster.pdf"
        return response


def get_data(request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
    data = {"sales": 100, "customers": 10}
    return JsonResponse(data)  # http response


class ChartData(APIView):
    authentication_classes: List = []
    permission_classes: List = []

    def get(self, request: HttpRequest, format: None = None) -> Response:
        qs_count = User.objects.all().count()
        labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
        default_items = [qs_count, 23, 2, 3, 12, 2]
        data = {"labels": labels, "default": default_items}
        return Response(data)


class LineChartJSONView(BaseLineChartView):
    def get_labels(self) -> List[str]:
        """Return 7 labels."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_data(self) -> List[List[int]]:
        """Return 3 datasets to plot."""
        datasets = [
            [0, 4, 9, 11, 44, 95, 350],
            [41, 92, 18, 3, 73, 87, 92],
            [87, 21, 94, 3, 90, 13, 65],
        ]
        return datasets


class LineChartView(TemplateView):
    template_name = "dmlresearch/linechart.html"


class AnalyticsIndexView(TemplateView):
    template_name = "dmlresearch/visitorchart.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
        context["monthly_registrations"] = self.thirty_day_registrations()
        # monthly_registrations = self.thirty_day_registrations()
        # context = {'monthly_registrations':monthly_registrations,}
        return context

    def thirty_day_registrations(self) -> List[int]:
        final_data = []

        date = arrow.now()
        for day in range(1, 30):
            date = date.replace(days=-1)
            count = User.objects.filter(
                date_joined__gte=date.floor("day").datetime,
                date_joined__lte=date.ceil("day").datetime,
            ).count()
            final_data.append(count)

        return final_data

    """class mychart(Temlplateview):
            template = 'mychart.html'
            context = {'xlabels': xlabels, 'ydata': ydata}

            def get_data:
                xlabels = [1,2,3,4,5]
                return xlabels


            def get_data:
                ydata = [3,6,4,2,5]
                return ydata
                """
