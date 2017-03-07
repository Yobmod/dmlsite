from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response


User = get_user_model()

class HomeView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'dmlresearch/charts.html', {"customers": 10})

def get_data(request, *args, **kwargs):
	data = {
		"sales": 100,
		"customers": 10,
	}
	return JsonResponse(data) # http response


class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		qs_count = User.objects.all().count()
		labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
		default_items = [qs_count, 23, 2, 3, 12, 2]
		data = {
				"labels": labels,
				"default": default_items,
		}
		return Response(data)

from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView



class LineChartJSONView(BaseLineChartView):
	def get_labels(self):
		"""Return 7 labels."""
		return ["January", "February", "March", "April", "May", "June", "July"]

	def get_data(self):
		"""Return 3 datasets to plot."""
		return [
				[0, 4, 9, 11, 44, 95, 350],
				[41, 92, 18, 3, 73, 87, 92],
				[87, 21, 94, 3, 90, 13, 65]
				]

class LineChartView(TemplateView):
	template_name='dmlresearch/linechart.html'



from django.views.generic import TemplateView
from django.contrib.auth.models import User
import arrow


class AnalyticsIndexView(TemplateView):
	template_name = 'dmlresearch/visitorchart.html'

	def get_context_data(self, **kwargs):
		context = super(AnalyticsIndexView, self).get_context_data(**kwargs)
		context['monthly_registrations'] = self.thirty_day_registrations()
		#monthly_registrations = self.thirty_day_registrations()
		#context = {'monthly_registrations':monthly_registrations,}
		return context

	def thirty_day_registrations(self):
		final_data = []

		date = arrow.now()
		for day in xrange(1, 30):
			date = date.replace(days=-1)
			count = User.objects.filter(
				date_joined__gte=date.floor('day').datetime,
				date_joined__lte=date.ceil('day').datetime).count()
			final_data.append(count)

		return final_data

	'''class mychart(Temlplateview):
			template = 'mychart.html'
			context = {'xlabels': xlabels, 'ydata': ydata}

			def get_data:
				xlabels = [1,2,3,4,5]
				return xlabels


			def get_data:
				ydata = [3,6,4,2,5]
				return ydata
				'''
