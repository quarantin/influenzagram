from django.db import models

class Minister(models.Model):
	TYPE_REGIME_PREMIERE          = 1
	TYPE_REGIME_SECONDE           = 2
	TYPE_REGIME_PROVISOIRE        = 3
	TYPE_REGIME_IVIEME_REPUBLIQUE = 4
	TYPE_REGIME_VIEME_REPUBLIQUE  = 5

	REGIME_CHOICES = (
		(TYPE_REGIME_PREMIERE,          'Gouvernement de la première Assemblée constituante'),
		(TYPE_REGIME_SECONDE,           'Gouvernement de la deuxième Assemblée constituante'),
		(TYPE_REGIME_PROVISOIRE,        'Gouvernement provisoire de la République'),
		(TYPE_REGIME_IVIEME_REPUBLIQUE, 'IVème République'),
		(TYPE_REGIME_VIEME_REPUBLIQUE,  'Vème République'),
	)

	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	political_regime = models.IntegerField(choices=REGIME_CHOICES)
	head_of_state = models.CharField(max_length=64)
	head_of_state_start = models.DateField()
	head_of_state_end = models.DateField(null=True)
	temp_head_of_state = models.CharField(max_length=64, null=True)
	temp_head_of_state_start = models.DateField(null=True)
	temp_head_of_state_end = models.DateField(null=True)
	head_of_government = models.CharField(max_length=64)
	period_start = models.DateField(null=True)
	period_end = models.DateField(null=True)
	function = models.CharField(max_length=512)
	nomination_start = models.DateField(null=True)
	nomination_end = models.DateField(null=True)
	comments = models.CharField(max_length=256, null=True)

	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)
