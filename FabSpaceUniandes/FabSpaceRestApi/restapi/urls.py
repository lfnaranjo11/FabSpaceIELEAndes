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
    path('now/', views.Now.as_view())


]
