from django.contrib import admin


admin.site.unregister(Site)

class SiteAdmin(admin.ModelAdmin):
	list_display = ('id', 'domain', 'name')

admin.site.register(Site, SiteAdmin)
