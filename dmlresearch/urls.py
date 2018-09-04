from django.conf.urls import url
from django.urls import path


from .views import (HomeView,
                    get_data,
                    ChartData,
                    LineChartView,
                    LineChartJSONView,
                    AnalyticsIndexView,)
from . import views

app_name = 'dmlresearch'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    path('poster', views.poster_view, name='poster'),


    #  url(r'^restchart/$', HomeView.as_view(), name='home'),
    url(r'^api/data/$', get_data, name='api-data'),
    url(r'^api/chart/data/$', ChartData.as_view()),

    url(r'^linechart/$', LineChartView.as_view(), name='linechart'),
    url(r'^linechart/data/$', LineChartJSONView.as_view(), name='line_chart_json'),

    url(r'^visitorchart/$', AnalyticsIndexView.as_view()),
    # url(r'^visitorchart/data/$', VisitorChartJSONView.as_view(), name='visitor_chart_json'),
]
