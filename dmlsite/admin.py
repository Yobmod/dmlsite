from django.contrib import admin
from django.contrib.sites.models import Site


admin.site.unregister(Site)


class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'name')


admin.site.register(Site, SiteAdmin)
