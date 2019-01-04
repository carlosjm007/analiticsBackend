from django.contrib import admin

# Register your models here.
from main.models import *

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
	pass

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
	pass