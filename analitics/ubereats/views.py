from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework import status
from ubereats.models import *
from ubereats.serializers import *
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def ciudad_solicitada_list(request, format=None):
	#######################################
	##	Retorna todas las ciudades
	if request.method == 'GET':
		ciudades = CiudadRequested.objects.all()
		serializer = CiudadRequestedSerializer(ciudades, many=True)
		return Response(serializer.data)
	#######################################
	##	Crea una nueva ciudad solicitada
	elif request.method == 'POST':
		serializer = CiudadRequestedSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def ciudad_solicitada_detail(request, pk, format=None):

	try:
		ciudad = CiudadRequested.objects.get(pk=pk)
	except CiudadRequested.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	#######################################
	##	Obtiene informacion a partir del id
	if request.method == 'GET':
		serializer = CiudadRequestedSerializer(ciudad)
		return Response(serializer.data)

	#######################################
	##	Edita informacion a partir del id
	elif request.method == 'PUT':
		serializer = CiudadRequestedSerializer(ciudad, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	#######################################
	##	Elimina informacion a partir del id
	elif request.method == 'DELETE':
		ciudad.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	#######################################
	##	Suma 1 like a la ciudad solicitada
	elif request.method == 'POST':
		ciudad.like = ciudad.like + 1
		ciudad.save()
		serializer = CiudadRequestedSerializer(ciudad)
		return Response(serializer.data)