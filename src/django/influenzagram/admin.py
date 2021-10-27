from django.contrib import admin
from .models import *

class TargetAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'country', 'birth_date')

class DataProviderAdmin(admin.ModelAdmin):
	list_display = ('name', 'source_type', 'url')

class DataProviderSecretAdmin(admin.ModelAdmin):
	pass

class DataSourceAdmin(admin.ModelAdmin):
	pass

class OnlinePresenceAdmin(admin.ModelAdmin):
	pass

class PictureAdmin(admin.ModelAdmin):
	pass

class ProfilePictureAdmin(admin.ModelAdmin):
	pass

class TagAdmin(admin.ModelAdmin):
	pass

class TagAssocAdmin(admin.ModelAdmin):
	pass
 
class VerificationAdmin(admin.ModelAdmin):
	pass

class VideoAdmin(admin.ModelAdmin):
	pass

admin.site.register(Target, TargetAdmin)
admin.site.register(DataProvider, DataProviderAdmin)
admin.site.register(DataProviderSecret, DataProviderSecretAdmin)
admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(OnlinePresence, OnlinePresenceAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(ProfilePicture, ProfilePictureAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TagAssoc, TagAssocAdmin)
