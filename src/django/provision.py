from django.contrib.auth.models import Group
for group in [ 'Contributor', 'Viewer' ]:
	obj, created = Group.objects.get_or_create(name=group)

from influenzagram.models import Target
obj, created = Target.objects.get_or_create(first_name='Éric', last_name='Zemmour', country='France', birth_date='1958-08-31')

from influenzagram.models import DataProvider
obj, created = DataProvider.objects.get_or_create(name='YouTube', url='https://www.youtube.com/', source_type='videos')

from influenzagram.models import Tag
obj, created = Tag.objects.get_or_create(tag='Bad Faith')
