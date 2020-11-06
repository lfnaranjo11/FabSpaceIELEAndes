from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework import viewsets, permissions, parsers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from .serializers import ImgSerializer, RequirementsSerializer
from .models import Img, Requeriments
from django.views.decorators.vary import vary_on_headers
from .tasks import query_and_download
from django.core.serializers import serialize
from .models import veredas, WorldBorder


# class verjson(APIView):

#   permission_classes = (AllowAny,)


# def get(self, request):
# serialize('geojson', veredas.objects.filter(nom_dep='VALLE DEL CAUCA', nomb_mpio='YUMBO',
#                                          nombre_ver = "SANTA INES"), geometry_field='geom', fields=('nombre_ver',))


# class worldborders(APIView):


#permission_classes = (AllowAny,)


# def get(self, request):
#  serialize('geojson', WorldBorder.objects.filter(),
#           geometry_field='mpoly', fields=('name',))


class Imgs(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Img.objects.all()
        serializer = ImgSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImgSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class Now(APIView):
    # debe enviar a la cola inmediatamente.
    # recibe menos de 5 y manda a la cola de una vez el trabajo de querry & download
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RequirementsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            query_and_download.apply_async(
                args=[serializer.data['id'], ], acks_late=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class Infuture(APIView):
    # recibe la zona de interes y el tiempo o lo que sea.
    # escribe el requerimiento.
    # luego el worker revisa los requerimientos y escribe las imagenes y luego otro worker las escribe de a poquitos
    # (esto no permite que las futuras imagenes aparezcan a menos de que se haga una actualizacion del modelo de requerimientos es decir una nueva consulta)
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RequirementsSerializer(data=request.data)
        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class WatchList(APIView):
    permission_classes = (AllowAny,)
    # recibe la zona de interes sin tiempo
    # verifica que no haya nuevas en la API y si las hay las descarga.

    def post(self, request):
        serializer = RequirementsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(state)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
