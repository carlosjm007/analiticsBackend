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