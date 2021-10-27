import json

from django.contrib.auth.models import Group
from influenzagram.models import *

with open('config.json', 'r') as fd:
	jsondata = json.load(fd)

for group in jsondata['Groups']:
	Group.objects.get_or_create(**group)

for target in jsondata['Targets']:
	tag = target['first_name'] + ' ' + target['last_name']
	Tag.objects.get_or_create(tag=tag)
	Target.objects.get_or_create(**target)

for provider in jsondata['DataProviders']:
	DataProvider.objects.get_or_create(**provider)
