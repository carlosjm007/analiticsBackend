from django.contrib.auth.models import User, Group
from rest_framework import serializers
from main.models import *

class CiudadSerializer(serializers.ModelSerializer):
	nombre = serializers.StringRelatedField()
	class Meta:
		model = Ciudad
		fields = ('id', 'nombre')

class PaisSerializer(serializers.ModelSerializer):
	nombre = serializers.StringRelatedField()
	ciudad = serializers.SerializerMethodField('TraeCiudades')
	def TraeCiudades(self, objeto):
		ciudades = Ciudad.objects.filter(pais=objeto)
		serializer = CiudadSerializer(instance=ciudades, many=True)
		return serializer.data

	class Meta:
		model = Ciudad
		fields = ('id', 'nombre', 'ciudad')