from django.db import models
from main.models import Ciudad, Pais
from decimal import Decimal
import requests, json
from ubereats.manager import *
from django.conf import settings
# Create your models here.

class HourDay(models.Model):
	hour = models.CharField(max_length=2)
	def __str__(self):
		return "%s" %(self.hour)
	class Meta:
		verbose_name = "Hora"
		verbose_name_plural = "Horas"

class DayWeek(models.Model):
	day = models.CharField(max_length=2) # De 0 a 6
	nombre = models.CharField(max_length=50) # De lunes a domingo
	def __str__(self):
		return "%s - %s" %(self.day, self.nombre)
	class Meta:
		verbose_name = "Dia"
		verbose_name_plural = "Dias"

class PaginaCiudad(Ciudad):
	url = models.URLField()
	csrftoken = models.CharField(max_length=100, default='')
	objects = PaginaCiudadManager()
	timezone = models.CharField(max_length=3, default='0')	#Horas de desfase con respecto a google trends
	lat1 = models.FloatField(default=0.0)
	lng1 = models.FloatField(default=0.0)
	lat2 = models.FloatField(default=0.0)
	lng2 = models.FloatField(default=0.0)
	actualizado = models.DateTimeField(auto_now=True)
	def __str__(self):
		return "%s" %(self.nombre)
	def save(self, *args, **kwargs):
		super(PaginaCiudad, self).save(*args, **kwargs)
		from main.serializers import PaisSerializer
		paises = Pais.objects.all()
		serializer = PaisSerializer(instance=paises, many=True)
		with open('%s/static/ubereats/jsons/paises.json'%(settings.BASE_DIR), 'w') as f:
			json.dump(serializer.data, f)
			
	class Meta:
		verbose_name = "Pagina por ciudad"
		verbose_name_plural = "Paginas por ciudad"

class Urls(models.Model):
	pagina_ciudad = models.ForeignKey(PaginaCiudad, on_delete=models.CASCADE)
	url = models.URLField()
	primera = models.BooleanField(default=False)
	offset = models.CharField(max_length=15, null=True, blank=True)
	pageSize = models.CharField(max_length=15, null=True, blank=True)
	request_payload = models.CharField(max_length=1000)
	data = models.TextField(null=True, blank=True)
	mapeado = models.BooleanField(default=True)	#Campo qu permite saber si la informacion capturada en data ya fue almacenada estructuralmente en las otras tablas
	objects = UrlManager()
	def __str__(self):
		return "%s" %(self.pagina_ciudad.nombre)
	class Meta:
		verbose_name = "URL"
		verbose_name_plural = "URLs"

class Tienda(models.Model):
	nombre = models.CharField(max_length=255)
	uuid = models.CharField(max_length=50)
	latitud = models.FloatField(default=0.0)
	longitud = models.FloatField(default=0.0)
	ciudad = models.ForeignKey(PaginaCiudad, on_delete=models.CASCADE)
	calificacion = models.DecimalField(default=Decimal('0.0'), max_digits=3, decimal_places=1)
	disponible = models.BooleanField(default=True)
	tipo_comida = models.TextField(null=True, blank=True)
	ubicacion_lista = models.IntegerField(null=True, blank=True)
	nombre_google = models.CharField(max_length=255, null=True, blank=True)
	direccion_google = models.CharField(max_length=255, null=True, blank=True)
	objects = TiendaManager()
	last_trend = models.DateTimeField(null=True, blank=True)	#Ultima informacion proporcionada por google trends
	last_google = models.DateTimeField(null=True, blank=True)	#Ultima informacion proporcionada por la api de google de restaurantes
	actualizado = models.DateTimeField(auto_now=True)
	def __str__(self):
		return "%s - %s" %(self.nombre, self.ciudad.nombre)
	def save(self, *args, **kwargs):
		pk = self.pk
		super(Tienda, self).save(*args, **kwargs)
		if pk == None:
			for hora in HourDay.objects.all():
				for dia in DayWeek.objects.all():
					TiendaBusqueda.objects.create(
							hour = hora,
							day = dia,
							tienda = self,
							busquedas = 0
						)
	class Meta:
		verbose_name = "Tienda"
		verbose_name_plural = "Tiendas"

class Productos(models.Model):
	nombre = models.CharField(max_length=255)
	tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
	eliminado = models.BooleanField(default=False)
	objects = ProductosManager()
	def __str__(self):
		return "%s - %s" %(self.nombre, self.tienda.nombre)
	def save(self, *args, **kwargs):
		pk = self.pk
		super(Productos, self).save(*args, **kwargs)
		if pk == None:
			for hora in HourDay.objects.all():
				for dia in DayWeek.objects.all():
					ProductoBusqueda.objects.create(
							hour = hora,
							day = dia,
							producto = self,
							busquedas = 0
						)
	class Meta:
		verbose_name = "Producto"
		verbose_name_plural = "Productos"

#####################################################
##	Tablas que se deben actualizar cada semana
class ProductoBusqueda(models.Model):
	hour = models.ForeignKey(HourDay, on_delete=models.CASCADE)
	day = models.ForeignKey(DayWeek, on_delete=models.CASCADE)
	producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
	busquedas = models.IntegerField()
	objects = ProductoBusquedaManager()
	def __str__(self):
		return "%s" %(self.producto.nombre)
	class Meta:
		verbose_name = "Busqueda por producto"
		verbose_name_plural = "Busquedas por producto"

class TiendaBusqueda(models.Model):
	hour = models.ForeignKey(HourDay, on_delete=models.CASCADE)
	day = models.ForeignKey(DayWeek, on_delete=models.CASCADE)
	tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
	busquedas = models.IntegerField()
	objects = TiendaBusquedaManager()
	def __str__(self):
		return "%s" %(self.tienda.nombre)
	class Meta:
		verbose_name = "Busqueda por tienda"
		verbose_name_plural = "Busquedas por tienda"

class PaisRequested(models.Model):
	nombre = models.CharField(max_length=255)
	def __str__(self):
		return "%s" %(self.nombre)
	def save(self, *args, **kwargs):
		super(PaisRequested, self).save(*args, **kwargs)
		from ubereats.serializers import PaisRequestedSerializer
		all_country = self.__class__.objects.all()
		datos = PaisRequestedSerializer(all_country, many=True).data
		with open('%s/static/ubereats/jsons/requested_countries.json'%(settings.BASE_DIR), 'w') as f:
			json.dump(datos, f)
	class Meta:
		verbose_name = "Pais solicitado"
		verbose_name_plural = "Paises solicitados"

class CiudadRequested(models.Model):
	nombre = models.CharField(max_length=255)
	pais = models.ForeignKey(PaisRequested, on_delete=models.CASCADE)
	like = models.IntegerField(default=0)
	def __str__(self):
		return "%s" %(self.nombre)
	class Meta:
		verbose_name = "Ciudad solicitada"
		verbose_name_plural = "Ciudades solicitados"