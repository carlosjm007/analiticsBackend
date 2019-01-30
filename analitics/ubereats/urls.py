from django.conf.urls import url, include
from rest_framework import routers
from ubereats import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

'''
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
'''

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	#url(r'^', include(router.urls)),
	#url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
	path('ciudad_solicitada_list/', views.ciudad_solicitada_list),
	path('ciudad_solicitada_detail/<int:pk>/', views.ciudad_solicitada_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)