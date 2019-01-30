from django.db import models
import json, requests, time
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

class PaginaCiudadManager(models.Manager):
	def get_csrftoken(self, client, ciudad):
		url_pagina = self.get(id=ciudad.id)
		bandera = True
		page = client.get(url_pagina.url)
		pagina = str(page.content)
		ubicacion_csrf = pagina.find("window.csrfToken")
		url_pagina.csrftoken = ""
		while(bandera):
			url_pagina.csrftoken = url_pagina.csrftoken + pagina[ubicacion_csrf]
			ubicacion_csrf = ubicacion_csrf + 1
			if pagina[ubicacion_csrf] == ";":
				bandera = False
		url_pagina.csrftoken = url_pagina.csrftoken.replace("window.csrfToken","").replace(" = ","").replace("\\'","")
		url_pagina.save()
		return url_pagina, client

	def get_firts_city_updated(self):
		delta_15_minutes = datetime.now(tz=timezone.utc) - timedelta(minutes=15)
		#delta_15_minutes = datetime.now(tz=timezone.utc) - timedelta(minutes=1)
		ciudades = self.exclude(actualizado__gte=delta_15_minutes)
		if len(ciudades) > 0:
			return ciudades.first()
		else:
			return False

class UrlManager(models.Manager):
	def get_data(self, client, pagina_ciudad):
		headers={
			"Referer":pagina_ciudad.url,
			"x-csrf-token":pagina_ciudad.csrftoken,
			"content-type": "application/json",
			"x-requested-with": "XMLHttpRequest"}
		for url in self.filter(pagina_ciudad = pagina_ciudad):
			r = client.post(url.url, headers=headers, json=json.loads(url.request_payload))
			if url.primera:
				url.data = json.dumps(r.json()["marketplace"]["feed"]["feedItems"])
			else:
				url.data = json.dumps(r.json()["feed"]["feedItems"])
			url.mapeado = False
			url.save()
		return self.filter(pagina_ciudad = pagina_ciudad), client

class TiendaManager(models.Manager):
	def get_tienda(self, urls, pagina_ciudad):
		self.filter(ciudad = pagina_ciudad).update(disponible=False, ubicacion_lista=None)
		index = 0
		for u in urls:
			data = json.loads(u.data)
			for ind, i in enumerate(data):
				if "storePayload" in i["payload"]:
					tienda_nombre = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"]
					tienda_nombre = tienda_nombre.replace(" ","+")
					tienda_nombre = tienda_nombre.replace("&","and")
					tiendita = self.filter(uuid = i["uuid"])
					if (len(tiendita) == 0):
						self.create(
							nombre = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"],
							uuid = i["uuid"],
							ciudad = u.pagina_ciudad,
							latitud = 0.0,
							longitud = 0.0,
							calificacion = 0,
							disponible = str(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["subtitle"]["text"]).find("Min") > 0,
							ubicacion_lista = index,
							tipo_comida = json.dumps(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["tagline"]["text"]),
							nombre_google = '',
							direccion_google = ''
							)
					else:
						self.filter(uuid = i["uuid"]).update(
							nombre = i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["title"]["text"],
							disponible = str(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["subtitle"]["text"]).find("Min") > 0,
							ciudad = u.pagina_ciudad,
							ubicacion_lista = index,
							tipo_comida = json.dumps(i["payload"]["storePayload"]["stateMapDisplayInfo"]["available"]["tagline"]["text"])
							)
					index = index + 1

		return self.filter(ciudad = pagina_ciudad)

	def get_firts_restaurant_updated(self):
		delta_30_days = datetime.now(tz=timezone.utc) - timedelta(days=30)
		restaurants = self.exclude(Q(last_google__gte=delta_30_days) | ~Q(last_google=None))
		if len(restaurants) > 0:
			return restaurants.first()
		else:
			return False

	def get_firts_trend_updated(self):
		delta_6_days = datetime.now(tz=timezone.utc) - timedelta(days=6)
		restaurants = self.exclude(Q(last_trend__gte=delta_6_days) | ~Q(last_trend=None))
		if len(restaurants) > 0:
			return restaurants.first()
		else:
			return False

class ProductosManager(models.Manager):
	def get_productos(self, tiendas):
		for t in tiendas:
			self.filter(tienda = t).update(eliminado=True)
			data = json.loads(t.tipo_comida)
			data = data.replace(' ', '').replace('$', '')
			data = data.split('•')
			for ind, i in enumerate(data):
				if ind != 0:
					if len(self.filter(nombre=i)) == 0:
						self.create(nombre=i, tienda=t, eliminado=False)
					else:
						self.filter(nombre=i).update(eliminado=False)

class ProductoBusquedaManager(models.Manager):
	def get_productos_busqueda(self, menu, data):
		for index, row in data.iterrows():
			#print(index.hour, index)
			#fecha = datetime.strptime(index, '%Y-%m-%d %H:%M:%S')
			for name in menu:
				fecha_hora = index + timedelta(hours=int(name.tienda.ciudad.timezone))
				self.filter(
						hour__hour = str(fecha_hora.hour),
						day__day =	str(fecha_hora.weekday()),
						producto = name
					).update(busquedas=row[name.nombre])

class TiendaBusquedaManager(models.Manager):
	def get_tiendas_busqueda(self, restaurant, data):
		for index, row in data.iterrows():
			#fecha = datetime.strptime(index, '%Y-%m-%d %H:%M:%S')
			if restaurant.nombre_google == '':
				palabra = restaurant.nombre
			else:
				palabra = restaurant.nombre_google
			fecha_hora = index + timedelta(hours=int(restaurant.ciudad.timezone))
			self.filter(
					hour__hour = str(fecha_hora.hour),
					day__day =	str(fecha_hora.weekday()),
					tienda = restaurant
				).update(busquedas=row[palabra])

		'''
		for name in list(data):
			if name != 'isPartial':
				producto = self.filter(producto__nombre=name, producto__tienda=restaurant)
				if len(producto) == 0:
					self.create()
		'''