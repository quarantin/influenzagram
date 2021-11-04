from django.contrib import admin

from .models import *

class OrganAdmin(admin.ModelAdmin):
	list_display = ('uid', 'label')

class DeputyAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'job_family', 'birth_date', 'death_date')

class DeputyAddressAdmin(admin.ModelAdmin):
	list_display = ('pk', 'deputy', 'type')

class MandateAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'deputy', 'date_start', 'date_end')

class MandateOrganAdmin(admin.ModelAdmin):
	list_display = ('mandate', 'organ_uid', 'organ')
	readonly_fields = ('organ_uid', 'organ', 'mandate')

class MandateCollaboraterAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'deputy', 'mandate', 'date_start', 'date_end')
	readonly_fields = ('deputy', 'mandate')

admin.site.register(Organ, OrganAdmin)
admin.site.register(Deputy, DeputyAdmin)
admin.site.register(DeputyAddress, DeputyAddressAdmin)
admin.site.register(Mandate, MandateAdmin)
admin.site.register(MandateOrgan, MandateOrganAdmin)
admin.site.register(MandateCollaborater, MandateCollaboraterAdmin)
