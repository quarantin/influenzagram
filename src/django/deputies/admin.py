from django.contrib import admin

from .models import *

class OrganAdmin(admin.ModelAdmin):
	pass

class DeputyAdmin(admin.ModelAdmin):
	pass

class DeputyAddress(admin.ModelAdmin):
	pass

class MandateAdmin(admin.ModelAdmin):
	pass

class MandateOrganAdmin(admin.ModelAdmin):
	pass

class MandateCollaborator(admin.ModelAdmin):
	pass

admin.site.register(Organ, OrganAdmin)
admin.site.register(Deputy, DeputyAdmin)
admin.site.register(DeputyAddress, DeputyAddressAdmin)
admin.site.register(Mandate, MandateAdmin)
admin.site.register(MandateOrgan, MandateOrganAdmin)
admin.site.register(MandateCollaborater, MandateCollaboraterAdmin)
