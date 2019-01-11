from main.serializers import *
from main.models import *
from rest_framework import viewsets


class PaisViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = Pais.objects.all().order_by('nombre')
	serializer_class = PaisSerializer


class CiudadViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Ciudad.objects.all().order_by('nombre')
	serializer_class = CiudadSerializer