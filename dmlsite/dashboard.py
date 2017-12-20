from controlcenter import Dashboard, widgets
from dmlblog.models import Post


class ModelItemList(widgets.ItemList):
    model = Post
    list_display = ('pk', 'field')


class MyDashboard(Dashboard):
    widgets = (
        ModelItemList,
    )
