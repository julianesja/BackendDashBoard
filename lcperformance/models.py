from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

# modelo de od statage
class od_stage(models.Model):
	name = models.CharField(max_length=250)

class product(models.Model):
	name = models.CharField(max_length=250)
	type_expa = models.CharField(max_length=50)
	code_expa = models.IntegerField()

class comite(models.Model):
	name = models.CharField(max_length=250)
	code_od_stage = models.ForeignKey(od_stage)
	code_expa = models.IntegerField(blank=True, null=True)
	code_podio = models.IntegerField(blank=True, null=True)

class focus_product(models.Model):
	code_comite =models.ForeignKey(comite)
	code_product=models.ForeignKey(product)
	year=models.IntegerField()
	period=models.IntegerField()

class custumer_stage(models.Model):
	name=models.CharField(max_length=250)
	code_expa=models.CharField(max_length=50)

class weekly(models.Model):
	init_date=models.DateField(auto_now=False, auto_now_add=False)
	final_date=models.DateField(auto_now=False, auto_now_add=False)
	name=models.CharField(max_length=25)

class target_product(models.Model):
	code_custumer_stage=models.ForeignKey(custumer_stage)
	code_product=models.ForeignKey(product)
	code_comite=models.ForeignKey(comite)
	target=models.IntegerField()
	code_weekly=models.ForeignKey(weekly)

class cumplido(models.Model):
	code_comite=models.ForeignKey(comite)
	date=models.DateField(auto_now=False, auto_now_add=False)
	code_product=models.ForeignKey(product)
	quantity=models.IntegerField()
	code_custumer_stage=models.ForeignKey(custumer_stage)

class aplicacion(models.Model):
    code_secret = models.CharField(max_length=250)
    podio_id = models.IntegerField()
    unique_name = models.CharField(max_length=20)

class user_register(models.Model):
    user_podio = models.CharField(max_length=250)
    password_podio = models.CharField(max_length=250)
    id_cliente_podio = models.CharField(max_length=250)
    codigo_secreto_podio = models.CharField(max_length=250)
    user_expa = models.CharField(max_length=250)
    password_expa = models.CharField(max_length=250)
