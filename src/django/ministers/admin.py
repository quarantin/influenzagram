from django.contrib import admin
from .models import Minister


class MinisterAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'political_regime', 'head_of_state', 'nomination_start', 'nomination_end', 'function')
	search_fields = ('first_name', 'last_name', 'function')

admin.site.register(Minister, MinisterAdmin)
