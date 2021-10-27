from django.contrib import admin
from .models import *

class TargetAdmin(admin.ModelAdmin):
    pass

class DataProviderAdmin(admin.ModelAdmin):
	pass

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
