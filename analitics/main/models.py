from django.db import models

class Pais(models.Model):
	nombre = models.CharField(max_length=255)
	def __str__(self):
		return "%s" %(self.nombre)
	class Meta:
		verbose_name = "Pais"
		verbose_name_plural = "Paises"

class Ciudad(models.Model):
	nombre = models.CharField(max_length=255)
	latitud = models.FloatField()
	longitud = models.FloatField()
	pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
	def __str__(self):
		return "%s" %(self.nombre)
	class Meta:
		verbose_name = "Ciudad"
		verbose_name_plural = "Ciudades"