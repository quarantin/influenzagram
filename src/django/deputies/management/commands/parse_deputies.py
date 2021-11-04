import os
import json
import requests
import zipfile

from django.core.management.base import BaseCommand
from deputies.models import *


class Command(BaseCommand):

	def debug(self, string):
		self.fd.write(string + '\n')

	def download_data(self):
		if not os.path.exists(self.filepath):
			print('Downloading ' + self.url)
			response = requests.get(self.url)
			fd = open(self.filepath, 'wb')
			fd.write(response.content)
			fd.close()

	def extract_data(self):
		if not os.path.exists(self.jsonfolder):
			print('Extracting ' + self.filepath)
			with zipfile.ZipFile(self.filepath) as fd:
				fd.extractall(self.folder)

	def parse_organ(self, jsonfile, parents):

		print('Parsing organ ' + os.path.basename(jsonfile))
		with open(jsonfile, 'r') as fd:
			data = json.loads(fd.read())

		organ = data['organe']

		info = {
			'uid':            organ['uid'],
			'type':           organ['@xsi:type'],
			'type_code':      organ['codeType'],
			'label':          organ['libelle'],
			'label_edition':  organ['libelleEdition'],
			'label_short':    organ['libelleAbrege'],
			'label_abbrev':   organ['libelleAbrev'],
			'date_start':     organ['viMoDe']['dateDebut'],
			'date_agreement': organ['viMoDe']['dateAgrement'],
			'date_end':       organ['viMoDe']['dateFin'],
			'chamber':        organ.get('chambre'),
			'regime':         organ.get('regime'),
			'legislature':    organ.get('legislature'),
			'secretary_1':    organ.get('secretariat', {}).get('secretaire01'),
			'secretary_2':    organ.get('secretariat', {}).get('secretaire02'),
		}

		organ, created = Organ.objects.get_or_create(**info)

		if organ.parent_organ:
			parents[organ.pk] = organ['parent_organ']

	def parse_parent_organs(self, parents):
		for organ_pk, parent_uid in parents.items():
			organ = Organ.objects.get(pk=organ_pk)
			organ.parent_organ = Organ.objects.get(uid=parent_uid)
			organ.save()

	def convert(self, data):
		return data and data.strip(', ') or data

	def parse_address(self, deputy, addr):

		info = {
			'deputy':      deputy,
			'type':        addr['type'],
			'weight':      addr['poids'],
			'address_uid': addr['adresseDeRattachement'],
		}

		if addr['@xsi:type'] == 'AdresseMail_Type':
			info['email_address']   = addr['valElec']

		elif addr['@xsi:type'] == 'AdressePostale_Type':
			info['entitle']         = self.convert(addr['intitule'])
			info['street_number']   = addr['numeroRue']
			info['street_name']     = self.convert(addr['nomRue'])
			info['street_addition'] = self.convert(addr['complementAdresse'])
			info['postal_code']     = addr['codePostal']
			info['city']            = addr['ville']

		elif addr['@xsi:type'] == 'AdresseSiteWeb_Type':
			info['web_site']        = addr['valElec']

		elif addr['@xsi:type'] == 'AdresseTelephonique_Type':
			info['phone_number']    = addr['valElec']

		address, created = DeputyAddress.objects.get_or_create(**info)

	def parse_mandate(self, deputy, mandate):

		info = {
			'deputy':                     deputy,
			'uid':                        mandate['uid'],
			'mandate_type':               mandate['@xsi:type'],
			'legislature':                mandate['legislature'],
			'date_start':                 mandate['dateDebut'],
			'date_published':             mandate['datePublication'],
			'date_end':                   mandate['dateFin'],
			'precedence':                 mandate['preseance'],
			'main_nomination':            mandate['nominPrincipale'],
			'quality_code':               mandate['infosQualite']['codeQualite'],
			'quality_label':              mandate['infosQualite']['libQualite'],
			'quality_label_sex':          mandate['infosQualite']['libQualiteSex'],
			'chamber':                    mandate.get('chambre'),
			'election_region':            mandate.get('election', {}).get('lieu', {}).get('region'),
			'election_region_type':       mandate.get('election', {}).get('lieu', {}).get('regionType'),
			'election_department':        mandate.get('election', {}).get('lieu', {}).get('departement'),
			'election_department_number': mandate.get('election', {}).get('lieu', {}).get('numDepartement'),
			'election_circonscription':   mandate.get('election', {}).get('lieu', {}).get('numCirco'),
			'mandate_cause':              mandate.get('election', {}).get('causeMandat'),
			'circonscription_uid':        mandate.get('election', {}).get('refCirconscription'),
			'mandate_date_start':         mandate.get('mandature', {}).get('datePriseFonction'),
			'mandate_end_cause':          mandate.get('mandature', {}).get('causeFin'),
			'mandate_first_election':     mandate.get('mandature', {}).get('premiereElection'),
			'mandate_hemicycle_seat':     mandate.get('mandature', {}).get('placeHemicycle'),
			'mandate_replace_uid':        mandate.get('mandature', {}).get('mandatRemplaceRef'),
		}

		if 'suppleants' in mandate and mandate['suppleants']:
			info['suppleant_date_start'] = mandate['suppleants']['suppleant']['dateDebut']
			info['suppleant_date_end']   = mandate['suppleants']['suppleant']['dateFin']
			info['suppleant_uid']        = mandate['suppleants']['suppleant']['suppleantRef']

		try:
			mandate_obj, created = Mandate.objects.get_or_create(**info)
		except Exception as err:
			self.debug(str(err))
			self.debug(json.dumps(info, indent=4))
			return # TODO remove this line

		self.parse_mandate_organs(mandate_obj, mandate['organes']['organeRef'])

		if 'collaborateurs' in mandate and mandate['collaborateurs'] and type(mandate['collaborateurs']) == dict:
			if type(mandate['collaborateurs']['collaborateur']) == list:
				for collaborater in mandate['collaborateurs']['collaborateur']:
					self.parse_mandate_collaborater(deputy, mandate_obj, collaborater)
			else:
				self.parse_mandate_collaborater(deputy, mandate_obj, mandate['collaborateurs']['collaborateur'])

	def parse_mandate_organ(self, mandate, organ_uid):

		try:
			organ = Organ.objects.get(uid=organ_uid)

		except Organ.DoesNotExist:
			self.debug('WARN: Missing organ: ' + organ_uid)
			organ = None

		MandateOrgan.objects.get_or_create(mandate=mandate, organ=organ, organ_uid=organ_uid)

	def parse_mandate_organs(self, mandate, organs):
		if type(organs) == list:
			for organ_uid in organs:
				self.parse_mandate_organ(mandate, organ_uid)
		else:
			self.parse_mandate_organ(mandate, organs)

	def parse_mandate_collaborater(self, deputy, mandate, collaborater):

		info = {
			'deputy':     deputy,
			'mandate':    mandate,
			'civility':   collaborater['qualite'],
			'first_name': collaborater['prenom'],
			'last_name':  collaborater['nom'],
			'date_start': collaborater['dateDebut'],
			'date_end':   collaborater['dateFin'],
		}

		MandateCollaborater.objects.get_or_create(**info)

	def parse_actor(self, jsonfile):

		print('Parsing actor ' + os.path.basename(jsonfile))
		with open(jsonfile, 'r') as fd:
			data = json.loads(fd.read())

		actor = data['acteur']

		info = {
			'uid':              actor['uid']['#text'],
			'civility':         actor['etatCivil']['ident']['civ'],
			'first_name':       actor['etatCivil']['ident']['prenom'],
			'last_name':        actor['etatCivil']['ident']['nom'],
			'alpha':            actor['etatCivil']['ident']['alpha'],
			'trigram':          actor['etatCivil']['ident']['trigramme'],
			'birth_date':       actor['etatCivil']['infoNaissance']['dateNais'],
			'birth_city':       actor['etatCivil']['infoNaissance']['villeNais'],
			'birth_department': actor['etatCivil']['infoNaissance']['depNais'],
			'birth_country':    actor['etatCivil']['infoNaissance']['paysNais'],
			'death_date':       actor['etatCivil']['dateDeces'],
			'job':              actor['profession']['libelleCourant'],
			'job_category':     actor['profession']['socProcINSEE']['catSocPro'],
			'job_family':       actor['profession']['socProcINSEE']['famSocPro'],
			'hatvp_url':        actor['uri_hatvp'],
		}

		fields = [
			'trigram',
			'birth_city',
			'birth_department',
			'birth_country',
			'death_date',
			'hatvp_url',
			'job',
			'job_category',
			'job_family',
		]

		for field in fields:
			if type(info[field]) != str:
				del(info[field])

		deputy, created = Deputy.objects.get_or_create(**info)

		if type(actor['adresses']['adresse']) == list:
			for address in actor['adresses']['adresse']:
				self.parse_address(deputy, address)
		else:
			self.parse_address(deputy, actor['adresses']['adresse'])

		if type(actor['mandats']['mandat']) == list:
			for mandate in actor['mandats']['mandat']:
				self.parse_mandate(deputy, mandate)
		else:
			self.parse_mandate(deputy, actor['mandats']['mandat'])

	def parse_organs(self, folder):
		parents = {}
		for jsonfile in os.listdir(folder):
			path = os.path.join(folder, jsonfile)
			if os.path.isfile(path):
				self.parse_organ(path, parents)
		return parents

	def parse_actors(self, folder):
		for jsonfile in os.listdir(folder):
			path = os.path.join(folder, jsonfile)
			if os.path.isfile(path):
				self.parse_actor(path)

	def handle(self, *args, **kwargs):

		self.fd = open('output.log', 'w')
		self.url = 'https://data.assemblee-nationale.fr/static/openData/repository/15/amo/deputes_senateurs_ministres_legislature/AMO20_dep_sen_min_tous_mandats_et_organes_XV.json.zip'
		self.folder = '/tmp'
		self.filepath = os.path.join(self.folder, os.path.basename(self.url))
		self.jsonfolder = os.path.join(self.folder, 'json')

		self.download_data()
		self.extract_data()

		self.parse_parent_organs(self.parse_organs(os.path.join(self.jsonfolder, 'organe')))
		self.parse_actors(os.path.join(self.jsonfolder, 'acteur'))
