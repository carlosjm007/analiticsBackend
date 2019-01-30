from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework import status
from ubereats.models import *
from ubereats.serializers import *
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def ciudad_solicitada_list(request, format=None):
	"""
	List all code snippets, or create a new snippet.
	"""
	if request.method == 'GET':
		ciudades = CiudadRequested.objects.all()
		serializer = CiudadRequestedSerializer(ciudades, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = CiudadRequestedSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ciudad_solicitada_detail(request, pk, format=None):
	"""
	Retrieve, update or delete a code snippet.
	"""
	try:
		ciudad = CiudadRequested.objects.get(pk=pk)
	except CiudadRequested.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = CiudadRequestedSerializer(ciudad)
		return Response(serializer.data)

	elif request.method == 'PUT':
		serializer = CiudadRequestedSerializer(ciudad, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		ciudad.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
'''
from ubereats.serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
'''