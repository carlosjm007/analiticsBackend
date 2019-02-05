from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ubereats.models import *

class PaisRequestedSerializer(serializers.ModelSerializer):
	class Meta:
		model = PaisRequested
		fields = ('id', 'nombre')

class CiudadRequestedSerializer(serializers.ModelSerializer):
	class Meta:
		model = CiudadRequested
		fields = ('id', 'nombre','pais', 'like')

class CiudadSerializer(serializers.ModelSerializer):
	nombre = serializers.StringRelatedField()
	class Meta:
		model = CiudadRequested
		fields = ('id', 'nombre')

class PaisSerializer(serializers.ModelSerializer):
	nombre = serializers.StringRelatedField()
	ciudad = serializers.SerializerMethodField('TraeCiudades')
	def TraeCiudades(self, objeto):
		ciudades = CiudadRequested.objects.filter(pais=objeto)
		serializer = CiudadSerializer(instance=ciudades, many=True)
		return serializer.data

	class Meta:
		model = Pais
		fields = ('id', 'nombre', 'ciudad')