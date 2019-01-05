from background_task import background
from ubereats.models import *
from main.models import *
import sys, requests, json, datetime
from pytrends.request import TrendReq
from django.conf import settings
from django.utils import timezone

@background()
def obtener_datos():
	city = Ciudad.objects.all().first()
	client = requests.session()
	pagina_ciudad, client = PaginaCiudad.objects.get_csrftoken(client, city)
	the_url, client = Urls.objects.get_data(client, pagina_ciudad)
	the_store = Tienda.objects.get_tienda(the_url, pagina_ciudad)
	Productos.objects.get_productos(the_store)
	print('obtener_datos')

@background()
def obtener_trends():
	palabras = []
	restaurant = Tienda.objects.all().order_by('-last_trend').first()
	#restaurant = Tienda.objects.get(id=1254)
	print("%s - obtener_trends"%restaurant.nombre)
	menu = Productos.objects.filter(tienda = restaurant)
	if restaurant.nombre_google == '':
		palabras.append(restaurant.nombre)
	else:
		palabras.append(restaurant.nombre_google)
	for m in menu:
		palabras.append(m.nombre)
	pytrends = TrendReq(hl='en-US', tz=360)
	pytrends.build_payload(palabras, cat=71, timeframe='now 7-d', geo='NZ-AUK', gprop='')
	data = pytrends.interest_over_time()
	ProductoBusqueda.objects.get_productos_busqueda(menu, data)
	TiendaBusqueda.objects.get_tiendas_busqueda(restaurant, data)
	restaurant.last_trend = datetime.datetime.now(tz=timezone.utc)
	restaurant.save()

@background()
def get_complement_information():
	latitud = 0.0
	longitud = 0.0
	calificacion = 0.0
	nombre_google = ""
	direccion_google = ""
	restaurant = Tienda.objects.all().order_by('-last_google').first()
	if restaurant == None:
		return None
	print("%s - get_complement_information"%restaurant.nombre)
	tienda_nombre = restaurant.nombre
	tienda_nombre = tienda_nombre.replace(" ","+")
	tienda_nombre = tienda_nombre.replace("&","and")
	url = '%slocation=%s,%s&radius=5000&type=restaurant&keyword=%s&key=%s'%(settings.GOOGLE_API_RESTAURANT, restaurant.ciudad.latitud, restaurant.ciudad.longitud, tienda_nombre, settings.GOOGLE_KEY)
	a = requests.get(url)
	for ind, t in enumerate(a.json()["results"]):
		if ind == 0:
			latitud = t['geometry']['location']["lat"]
			longitud = t['geometry']['location']["lng"]
			calificacion = t['rating']
			nombre_google = t['name']
			direccion_google = t['vicinity']
	restaurant.latitud = latitud
	restaurant.longitud = longitud
	restaurant.calificacion = calificacion
	restaurant.nombre_google = nombre_google
	restaurant.direccion_google = direccion_google
	restaurant.last_google = datetime.datetime.now(tz=timezone.utc)
	restaurant.save()

@background()
def ponderaciones():
	city = PaginaCiudad.objects.all().order_by('-actualizado').first()
	delta = datetime.datetime.now(tz=timezone.utc) - city.actualizado
	if (delta.seconds < 100):
		print(delta.seconds)
		return None
	restaurant = Tienda.objects.filter(ciudad=city, disponible=True).order_by('last_trend')
	if restaurant == None:
		return None
	datos = {}
	datos["name"] = city.nombre
	datos["position"] = {
		"lat":city.latitud,
		"lng":city.longitud
	}
	datos["square"] ={
		"lat1":city.lat1,
		"lng1":city.lng1,
		"lat2":city.lat2,
		"lng2":city.lng2
	}
	datos["restaurants"] = []
	datos["maximo_lista"] = 0
	datos["maximo_busqueda"] = 0
	date = datetime.datetime.now() + datetime.timedelta(hours=int(city.timezone))
	menu = ProductoBusqueda.objects.filter(hour__hour=str(date.hour), day__day=str(date.weekday()), producto__tienda__in=restaurant)
	store = TiendaBusqueda.objects.filter(hour__hour=str(date.hour), day__day=str(date.weekday()), tienda__in=restaurant)
	for s in store:
		u = {}
		u["position"] = {
			"lat":city.latitud,
			"lng":city.longitud
		}
		u["lista"] = s.tienda.ubicacion_lista
		if u["lista"] > datos["maximo_lista"]:
			datos["maximo_lista"] = u["lista"]
		u["busqueda"] = s.busquedas
		for m in menu.filter(producto__tienda=s.tienda):
			u["busqueda"] = u["busqueda"] + m.busquedas
		if u["busqueda"] > datos["maximo_busqueda"]:
			datos["maximo_busqueda"] = u["busqueda"]
		datos["restaurants"].append(u)

	with open('%s/static/ubereats/jsons/%s.json'%(settings.BASE_DIR,city.id), 'w') as f:
		json.dump(datos, f)
	city.save()
	print(city.nombre)