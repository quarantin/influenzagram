from django.contrib import admin

from .models import *

class OrganAdmin(admin.ModelAdmin):
	list_display = ('uid', 'label')

class DeputyAdmin(admin.ModelAdmin):
	list_display = ('uid', 'first_name', 'last_name')

class DeputyAddressAdmin(admin.ModelAdmin):
	list_display = ('pk', 'deputy', 'type_label')

class MandateAdmin(admin.ModelAdmin):
	list_display = ('pk', 'deputy', 'mandate_type', 'date_start', 'date_end')

class MandateOrganAdmin(admin.ModelAdmin):
	pass

class MandateCollaboraterAdmin(admin.ModelAdmin):
	pass

admin.site.register(Organ, OrganAdmin)
admin.site.register(Deputy, DeputyAdmin)
admin.site.register(DeputyAddress, DeputyAddressAdmin)
admin.site.register(Mandate, MandateAdmin)
admin.site.register(MandateOrgan, MandateOrganAdmin)
admin.site.register(MandateCollaborater, MandateCollaboraterAdmin)
