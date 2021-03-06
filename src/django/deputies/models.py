from django.db import models

# DATA WE NEED
# - countries
# - french cities
# - french departments
# - french postal codes
# - INSEE job categories
# - INSEE job families

CITY_MAX_LENGTH = 32
UID_MAX_LENGTH = 10

class Organ(models.Model):
	TYPE_GROUPE_POLITIQUE                   = 'GroupePolitique_type'
	TYPE_ORGANE_EXTERNE                     = 'OrganeExterne_Type'
	TYPE_ORGANE_EXTRA_PARLEMENTAIRE         = 'OrganeExtraParlementaire_type'
	TYPE_ORGANE_PARLEMENTAIRE               = 'OrganeParlementaire_Type'
	TYPE_ORGANE_PARLEMENTAIRE_INTERNATIONAL = 'OrganeParlementaireInternational'

	ORGAN_TYPE_CHOICES = (
		(TYPE_GROUPE_POLITIQUE,                   'Groupe Politique'),
		(TYPE_ORGANE_EXTERNE,                     'Organe Externe'),
		(TYPE_ORGANE_EXTRA_PARLEMENTAIRE,         'Organe Extra Parlementaire'),
		(TYPE_ORGANE_PARLEMENTAIRE,               'Orgaine Parlementaire'),
		(TYPE_ORGANE_PARLEMENTAIRE_INTERNATIONAL, 'Organe Parlementaire International'),
	)

	CODE_TYPE_API          = 'API'
	CODE_TYPE_ASSEMBLEE    = 'ASSEMBLEE'
	CODE_TYPE_CJR          = 'CJR'
	CODE_TYPE_CMP          = 'CMP'
	CODE_TYPE_CNPE         = 'CNPE'
	CODE_TYPE_CNPS         = 'CNPS'
	CODE_TYPE_COMNL        = 'COMNL'
	CODE_TYPE_COMPER       = 'COMPER'
	CODE_TYPE_COMSENAT     = 'COMSENAT'
	CODE_TYPE_COMSPSENAT   = 'COMSPSENAT'
	CODE_TYPE_CONFPT       = 'CONFPT'
	CODE_TYPE_CONSTITU     = 'CONSTITU'
	CODE_TYPE_DELEG        = 'DELEG'
	CODE_TYPE_DELEGBUREAU  = 'DELEGBUREAU'
	CODE_TYPE_DELEGSENAT   = 'DELEGSENAT'
	CODE_TYPE_GA           = 'GA'
	CODE_TYPE_GE           = 'GE'
	CODE_TYPE_GEVI         = 'GEVI'
	CODE_TYPE_GOUVERNEMENT = 'GOUVERNEMENT'
	CODE_TYPE_GP           = 'GP'
	CODE_TYPE_GROUPESENAT  = 'GROUPESENAT'
	CODE_TYPE_HCJ          = 'HCJ'
	CODE_TYPE_MINISTERE    = 'MINISTERE'
	CODE_TYPE_MISINFO      = 'MISINFO'
	CODE_TYPE_MISINFOCOM   = 'MISINFOCOM'
	CODE_TYPE_MISINFOPRE   = 'MISINFOPRE'
	CODE_TYPE_OFFPAR       = 'OFFPAR'
	CODE_TYPE_ORGAINT      = 'ORGAINT'
	CODE_TYPE_ORGEXTPARL   = 'ORGEXTPARL'
	CODE_TYPE_PARPOL       = 'PARPOL'
	CODE_TYPE_PRESREP      = 'PRESREP'
	CODE_TYPE_SENAT        = 'SENAT'

	ORGAN_TYPE_CODE_CHOICES = (
		(CODE_TYPE_API,          'Assembl??e parlementaire internationale'),
		(CODE_TYPE_ASSEMBLEE,    'Assembl??e nationale'),
		(CODE_TYPE_CJR,          'Cour de justice de la R??publique'),
		(CODE_TYPE_CMP,          'Commissions mixtes paritaires'),
		(CODE_TYPE_CNPE,         'Commissions d???enqu??tes'),
		(CODE_TYPE_CNPS,         'Commissions sp??ciales'),
		(CODE_TYPE_COMNL,        'Autres commissions permanentes'),
		(CODE_TYPE_COMPER,       'Commissions permanentes l??gislatives'),
		(CODE_TYPE_COMSENAT,     'Commissions s??natoriales'),
		(CODE_TYPE_COMSPSENAT,   'Commissions sp??ciales s??natoriales'),
		(CODE_TYPE_CONFPT,       'Conf??rence des pr??sidents'),
		(CODE_TYPE_CONSTITU,     'Conseil constitutionnel'),
		(CODE_TYPE_DELEG,        'D??l??gation parlementaire'),
		(CODE_TYPE_DELEGBUREAU,  'D??l??gation du Bureau de l???Assembl??e Nationale'),
		(CODE_TYPE_DELEGSENAT,   'D??l??gation s??natoriale'),
		(CODE_TYPE_GA,           'Groupe d???amiti??'),
		(CODE_TYPE_GE,           'Groupe d?????tudes'),
		(CODE_TYPE_GEVI,         'Groupe d?????tudes ?? vocation internationale'),
		(CODE_TYPE_GOUVERNEMENT, 'Gouvernement'),
		(CODE_TYPE_GP,           'Groupe politique'),
		(CODE_TYPE_GROUPESENAT,  'Groupe s??natorial'),
		(CODE_TYPE_HCJ,          'Haute cour de justice'),
		(CODE_TYPE_MINISTERE,    'Minist??re'),
		(CODE_TYPE_MISINFO,      'Missions d???informations'),
		(CODE_TYPE_MISINFOCOM,   'Missions d???information communes'),
		(CODE_TYPE_MISINFOPRE,   'Missions d???information de la conf??rence des Pr??sidents'),
		(CODE_TYPE_OFFPAR,       'Office parlementaire ou d??l??gation mixte'),
		(CODE_TYPE_ORGAINT,      'Organisme international'),
		(CODE_TYPE_ORGEXTPARL,   'Organisme extra parlementaire'),
		(CODE_TYPE_PARPOL,       'Parti politique'),
		(CODE_TYPE_PRESREP,      'Pr??sidence de la R??publique'),
		(CODE_TYPE_SENAT,        'S??nat'),
	)

	uid = models.CharField(max_length=UID_MAX_LENGTH, verbose_name='UID')
	type = models.CharField(max_length=40, choices=ORGAN_TYPE_CHOICES)
	type_code = models.CharField(max_length=16, choices=ORGAN_TYPE_CODE_CHOICES)
	label = models.CharField(max_length=2048)
	label_edition = models.CharField(max_length=2048, null=True)
	label_short = models.CharField(max_length=128)
	label_abbrev = models.CharField(max_length=32)
	date_start = models.DateField(null=True)
	date_agreement = models.DateField(null=True)
	date_end = models.DateField(null=True)
	parent_organ = models.ForeignKey('deputies.Organ', on_delete=models.CASCADE, null=True)
	chamber = models.CharField(max_length=32, null=True) # Always null
	regime = models.CharField(max_length=200, null=True)
	legislature = models.IntegerField(null=True)
	secretary_1 = models.CharField(max_length=64, null=True)
	secretary_2 = models.CharField(max_length=64, null=True)

	def __str__(self):
		return self.label

class Deputy(models.Model):
	uid = models.CharField(max_length=UID_MAX_LENGTH, verbose_name='UID')
	civility = models.CharField(max_length=8)
	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	alpha = models.CharField(max_length=32)
	trigram = models.CharField(max_length=8)
	birth_date = models.DateField()
	birth_city = models.CharField(max_length=CITY_MAX_LENGTH)
	birth_department = models.CharField(max_length=32)
	birth_country = models.CharField(max_length=32)
	death_date = models.DateField(null=True)
	job = models.CharField(max_length=128)
	job_category = models.CharField(max_length=200)
	job_family = models.CharField(max_length=64)
	hatvp_url = models.URLField(max_length=2048, verbose_name='HATVP URL')

	def __str__(self):
		return '%s %s %s' % (self.civility, self.first_name, self.last_name)

	class Meta:
		verbose_name_plural = 'Deputies'

class DeputyAddress(models.Model):

	TYPE_OFFICAL_ADDRESS         = 0
	TYPE_PARIS_ADDRESS           = 1
	TYPE_CIRCONSCRIPTION_ADDRESS = 2
	TYPE_TELEPHONE               = 11
	TYPE_TELECOPY                = 12
	TYPE_MAIL                    = 15
	TYPE_WEBSITE                 = 22
	TYPE_SENATOR_URL             = 23
	TYPE_TWITTER                 = 24
	TYPE_FACEBOOK                = 25
	TYPE_INSTAGRAM               = 29
	TYPE_LINKEDIN                = 30

	TYPE_CHOICES = (
		(TYPE_OFFICAL_ADDRESS,         'Adresse officielle'),
		(TYPE_PARIS_ADDRESS,           'Adresse publi??e pour Paris ou sa r??gion'),
		(TYPE_CIRCONSCRIPTION_ADDRESS, 'Adresse publi??e de circonscription'),
		(TYPE_TELEPHONE,               'T??l??phone'),
		(TYPE_TELECOPY,                'T??l??copie'),
		(TYPE_MAIL,                    'M??l'),
		(TYPE_WEBSITE,                 'Site internet'),
		(TYPE_SENATOR_URL,             'URL s??nateur'),
		(TYPE_TWITTER,                 'Twitter'),
		(TYPE_FACEBOOK,                'Facebook'),
		(TYPE_INSTAGRAM,               'Instagram'),
		(TYPE_LINKEDIN,                'Linkedin'),
	)

	deputy = models.ForeignKey(Deputy, on_delete=models.CASCADE)
	type = models.IntegerField(choices=TYPE_CHOICES)
	weight = models.IntegerField(null=True)
	address_uid = models.CharField(max_length=8, null=True, verbose_name='Address UID')
	entitle = models.CharField(max_length=64, null=True)
	street_number = models.CharField(max_length=16, null=True)
	street_name = models.CharField(max_length=64, null=True)
	street_addition = models.CharField(max_length=64, null=True)
	postal_code = models.CharField(max_length=5, null=True)
	city = models.CharField(max_length=CITY_MAX_LENGTH, null=True)
	phone_number = models.CharField(max_length=32)
	email_address = models.CharField(max_length=320)
	web_site = models.CharField(max_length=2048)

	#def __str__(self):
	#	if self.
	class Meta:
		verbose_name_plural = 'Deputy addresses'

class Mandate(models.Model):

	TYPE_MANDATE_MISSION        = 'MandatMission_Type'
	TYPE_MANDATE_PARLEMENTAIRE  = 'MandatParlementaire_type'
	TYPE_MANDATE_SIMPLE         = 'MandatSimple_Type'
	TYPE_MANDATE_WITH_SUPPLEANT = 'MandatAvecSuppleant_Type'

	MANDATE_CHOICES = (
		(TYPE_MANDATE_MISSION,        'Mission'),
		(TYPE_MANDATE_PARLEMENTAIRE,  'Parlementaire'),
		(TYPE_MANDATE_SIMPLE,         'Simple'),
		(TYPE_MANDATE_WITH_SUPPLEANT, 'Avec Suppl??ant'),
	)

	deputy = models.ForeignKey(Deputy, on_delete=models.CASCADE)
	uid = models.CharField(max_length=UID_MAX_LENGTH, verbose_name='UID')
	mandate_type = models.CharField(max_length=24, choices=MANDATE_CHOICES)
	legislature = models.IntegerField(null=True)
	organ = models.ForeignKey(Organ, on_delete=models.CASCADE, null=True)
	date_start = models.DateField(null=True)
	date_end = models.DateField(null=True)
	date_published = models.DateField(null=True)
	precedence = models.IntegerField(null=True)
	main_nomination = models.BooleanField()
	quality_code = models.CharField(max_length=128, null=True)
	quality_label = models.CharField(max_length=128)
	quality_label_sex = models.CharField(max_length=128, null=True)
	suppleant_uid = models.CharField(max_length=UID_MAX_LENGTH, verbose_name='Suppleant UID')
	suppleant_date_start = models.DateField(null=True)
	suppleant_date_end = models.DateField(null=True)
	chamber = models.CharField(max_length=32, null=True) # Always null
	election_region = models.CharField(max_length=32, null=True)
	election_region_type = models.CharField(max_length=64, null=True)
	election_department = models.CharField(max_length=32, null=True)
	election_department_number = models.CharField(max_length=8, null=True)
	election_circonscription = models.IntegerField(null=True)
	mandate_cause = models.CharField(max_length=200, null=True)
	circonscription_uid = models.CharField(max_length=UID_MAX_LENGTH, null=True, verbose_name='Circonscription UID')
	mandate_date_start = models.DateField(null=True)
	mandate_end_cause = models.CharField(max_length=200, null=True)
	mandate_first_election = models.BooleanField(null=True)
	mandate_hemicycle_seat = models.IntegerField(null=True)
	mandate_replace_uid = models.CharField(max_length=UID_MAX_LENGTH, null=True, verbose_name='Mandate replace UID')

	def __str__(self):
		return 'Mandat ' + self.get_mandate_type_display()

class MandateOrgan(models.Model):
	organ = models.ForeignKey(Organ, on_delete=models.CASCADE, null=True)
	organ_uid = models.CharField(max_length=UID_MAX_LENGTH, verbose_name='Organ UID')
	mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE)

class MandateCollaborater(models.Model):
	deputy = models.ForeignKey(Deputy, on_delete=models.CASCADE)
	mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE)
	civility = models.CharField(max_length=8)
	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	date_start = models.DateField(null=True)
	date_end = models.DateField(null=True)

	def __str__(self):
		return '%s %s %s' % (self.civility, self.first_name, self.last_name)
