# -*- coding: utf-8 -*-

import os
import json
import requests
import pyexcel_ods
from datetime import datetime

from django.core.management.base import BaseCommand
from ministers.models import *

class Command(BaseCommand):

	regimes = {v: k for k, v in Minister.REGIME_CHOICES}

	def download_data(self):
		if not os.path.exists(self.filepath):
			print('Downloading ' + self.url)
			response = requests.get(self.url)
			fd = open(self.filepath, 'wb')
			fd.write(response.content)
			fd.close()

	"""
['V', 'VOYNET', 'Dominique', 'Vème République', 'Jacques CHIRAC 17/05/1995 - 16/05/2007', 'Lionel JOSPIN (2ème gouvernement)', '27/03/2000 - 06/05/2002', "Ministre de l'Aménagement du Territoire et de l'Environnement", datetime.datetime(2000, 3, 27, 0, 0), datetime.datetime(2001, 7, 10, 0, 0)]
['W', 'WAUQUIEZ', 'Laurent', 'Vème République', 'Nicolas SARKOZY 16/05/2007 - 15/05/2012', 'François FILLON (2ème gouvernement)', '18/06/2007 - 18/03/2008', 'SE, Porte-parole du Gouvernement', datetime.datetime(2007, 6, 18, 0, 0), datetime.datetime(2008, 3, 18, 0, 0)]
['W', 'WAUQUIEZ', 'Laurent', 'Vème République', 'Nicolas SARKOZY 16/05/2007 - 15/05/2012', 'François FILLON (Remaniements 2ème gouvernement)', '18/03/2008 - 13/11/2010', 'SE (Emploi)', datetime.datetime(2008, 3, 18, 0, 0), datetime.datetime(2010, 11, 13, 0, 0)]
['W', 'WAUQUIEZ', 'Laurent', 'Vème République', 'Nicolas SARKOZY 16/05/2007 - 15/05/2012', 'François FILLON (3ème gouvernement, remaniements aux 27/02/2011, 29/05/2011, 29/06/2011, 26/09/2011, 28/09/2011)', '14/11/2010 - 10/05/2012', 'Ministre auprès de la ministre d’Etat, ministre des affaires étrangères et européennes, chargé des affaires européennes', datetime.datetime(2010, 11, 14, 0, 0), datetime.datetime(2011, 6, 29, 0, 0)]
['W', 'WAUQUIEZ', 'Laurent', 'Vème République', 'Nicolas SARKOZY 16/05/2007 - 15/05/2012', 'François FILLON (3ème gouvernement, remaniements aux 27/02/2011, 29/05/2011, 29/06/2011, 26/09/2011, 28/09/2011)', '14/11/2010 - 10/05/2012', "Ministre de l'Enseignement supérieur et de la Recherche", datetime.datetime(2011, 6, 29, 0, 0), datetime.datetime(2012, 5, 10, 0, 0)]
['W', 'WILTZER', 'Pierre-André', 'Vème République', 'Jacques CHIRAC 17/05/1995 - 16/05/2007', 'Jean-Pierre RAFFARIN (2ème gouvernement)', '17/06/2002 - 30/03/2004', 'MD chargé de la Coopération et de la Francophonie', datetime.datetime(2002, 6, 17, 0, 0), datetime.datetime(2004, 3, 30, 0, 0)]
['W', 'WOERTH', 'Eric', 'Vème République', 'Jacques CHIRAC 17/05/1995 - 16/05/2007', 'Jean-Pierre RAFFARIN (3ème gouvernement)', '31/03/2004 - 28/11/2004', "SE (Réforme de l'Etat)", datetime.datetime(2004, 3, 31, 0, 0), datetime.datetime(2004, 11, 28, 0, 0)]"""

	def parse_ministers(self):
		data = pyexcel_ods.get_data(self.filepath)
		for sheet, rows in data.items():
			for row in rows[2:]:

				if not row:
					continue

				d = {}
				if len(row) == 9:
					_, d['last_name'], d['first_name'], regime, head_of_state, head_of_government, period, d['function'], d['nomination_start'] = row
					d['nomination_end'] = None
				elif len(row) == 10:
					_, d['last_name'], d['first_name'], regime, head_of_state, head_of_government, period, d['function'], d['nomination_start'], d['nomination_end'] = row
					d['comments'] = ''
				elif len(row) == 11:
					_, d['last_name'], d['first_name'], regime, head_of_state, head_of_government, period, d['function'], d['nomination_start'], d['nomination_end'], d['comments'] = row
				else:
					raise Exception('ERROR: %s' % row)

				d['political_regime'] = self.regimes[regime]

				lines = head_of_state.split('\n')
				tokens = lines[0].split(' ')
				d['head_of_state'] = ' '.join(tokens[0:-3])
				d['head_of_state_start'] = datetime.strptime(tokens[-3], '%d/%m/%Y')
				if tokens[-1].startswith('…'):
					d['head_of_state_end'] = None
				else:
					d['head_of_state_end'] = datetime.strptime(tokens[-1], '%d/%m/%Y')

				if len(lines) > 1:
					tokens = lines[1].split(' ')
					d['temp_head_of_state'] = ' '.join(tokens[0:-3])
					d['temp_head_of_state_start'] = datetime.strptime(tokens[-3], '%d/%m/%Y')
					d['temp_head_of_state_end'] = datetime.strptime(tokens[-1], '%d/%m/%Y')

				tokens = head_of_government.split('(')
				d['head_of_government'] = tokens[0].strip()

				if d['function'].startswith('MD'):
					d['function'] = d['function'].replace('MD', 'Ministre délégué')
				elif d['function'].startswith('SE'):
					d['function'] = d['function'].replace('SE', 'Secrétaire d\'état')
				elif d['function'].startswith('Sous-SE'):
					d['function'] = d['function'].replace('Sous-SE', 'Sous-secrétaire d\'état')

				tokens = period.strip().split(' ')
				if len(tokens) == 2:
					d['period_start'] = tokens[0].strip('- ') or None
					d['period_end'] = tokens[1] or None
				else:
					d['period_start'] = tokens[0] or None
					d['period_end'] = tokens[2] or None

				if d['period_start'] and d['period_start'].startswith('…'):
					d['period_start'] = None

				if d['period_end'] and d['period_end'].startswith('…'):
					d['period_end'] = None

				if d['period_start']:
					d['period_start'] = datetime.strptime(d['period_start'], '%d/%m/%Y')

				if d['period_end']:
					d['period_end'] = datetime.strptime(d['period_end'], '%d/%m/%Y')

				Minister.objects.get_or_create(**d)
				print('.', end='')

	def handle(self, *args, **kwargs):
		self.url = 'https://www.data.gouv.fr/storage/f/2014-06-18T11-14-55/liste-alphabetique-ministres-de-la-liberation-a-la-veme-republique.ods'
		self.folder = 'data'
		self.filepath = os.path.join(self.folder, os.path.basename(self.url))
		self.jsonfolder = os.path.join(self.folder, 'json')

		self.download_data()
		self.parse_ministers()
