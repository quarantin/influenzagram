from django.contrib import admin
from .models import Minister


class MinisterAdmin(admin.ModelAdmin):
	list_display = ('__str__',)

admin.site.register(Minister, MinisterAdmin)
