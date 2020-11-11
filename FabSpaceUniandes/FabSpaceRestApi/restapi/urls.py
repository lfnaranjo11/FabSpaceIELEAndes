from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as authviews
from . import views
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('api-auth/', authviews.obtain_auth_token),
    path('imgscache/', cache_page(60 * 15)(views.Imgs.as_view())),
    path('imgsnocache/', views.Imgs.as_view()),
    path('imgbyid/', views.Imgs.as_view()),
    path('now/', views.Now.as_view()),
    path('listdeptos/', views.ListDeptos.as_view()),
    path('deptogeojson/<str:depto_cdgo>',
         views.Deptosjson.as_view(), name='get enterprise info p'),
    path('listmpios/<str:depto_cdgo>', views.ListMpios.as_view()),
    path('mpiosgeojson/<str:depto_cdgo>',
         views.Municipiosjson.as_view(), name='get mpios geogson by dpto'),
    path('veredasgeojson/<str:mpio_cdgo>',
         views.Verjson.as_view(), name='get veredas geogson by mpio'),
    path('listvdas/<str:mpio_cdgo>', views.ListVdas.as_view()),




]
