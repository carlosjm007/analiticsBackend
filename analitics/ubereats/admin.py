from django.contrib import admin

# Register your models here.
from ubereats.models import *
from import_export.admin import ImportExportActionModelAdmin

@admin.register(PaginaCiudad)
class PaginaCiudadAdmin(admin.ModelAdmin):
	pass

@admin.register(Urls)
class UrlsAdmin(admin.ModelAdmin):
	pass

@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
	pass

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
	pass

@admin.register(HourDay)
class ProductosAdmin(admin.ModelAdmin):
	pass

@admin.register(DayWeek)
class ProductosAdmin(admin.ModelAdmin):
	pass

@admin.register(ProductoBusqueda)
class ProductosAdmin(admin.ModelAdmin):
	pass

@admin.register(TiendaBusqueda)
class ProductosAdmin(admin.ModelAdmin):
	pass

@admin.register(PaisRequested)
class ProductosAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	pass

@admin.register(CiudadRequested)
class ProductosAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
	pass