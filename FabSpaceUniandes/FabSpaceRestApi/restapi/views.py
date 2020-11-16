from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework import viewsets, permissions, parsers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from .serializers import ImgSerializer, RequirementsSerializer
from .models import Img, Requeriments, DepartamentosVeredas, MunicipiosVeredas
from django.views.decorators.vary import vary_on_headers
from .tasks import query_and_download
from django.core.serializers import serialize
from .models import veredas, WorldBorder
from django.core.serializers.json import DjangoJSONEncoder
import json


#   permission_classes = (AllowAny,)

# def get(self, request):
# serialize('geojson', veredas.objects.filter(nom_dep='VALLE DEL CAUCA', nomb_mpio='YUMBO',
#                                            nombre_ver="SANTA INES"), geometry_field='geom', fields=('nombre_ver',))

# class worldborders(APIView):

# permission_classes = (AllowAny,)

# def get(self, request):
#  serialize('geojson', WorldBorder.objects.filter(),
#           geometry_field='mpoly', fields=('name',))
class ListReq(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = Requeriments.objects.all()
        serializer = RequirementsSerializer(queryset, many=True)
        return Response(serializer.data)


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
        print(request.data)
        serializer = RequirementsSerializer(data=request.data)
        print(serializer)
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


class Deptosjson(APIView):
    permission_classes = (AllowAny,)
    # recibe la zona de interes sin tiempo
    # verifica que no haya nuevas en la API y si las hay las descarga.

    def get(self, request, depto_cdgo):
        sx = serialize('geojson', DepartamentosVeredas.objects.filter(dpto_ccdgo=depto_cdgo),
                       geometry_field='geom', fields=('dpto_ccdgo',))
        m = json.loads(sx)
        return Response(m)


class Municipiosjson(APIView):
    permission_classes = (AllowAny,)
    # recibe la zona de interes sin tiempo
    # verifica que no haya nuevas en la API y si las hay las descarga.

    def get(self, request, depto_cdgo):
        print('hola')
        sx = serialize('geojson', MunicipiosVeredas.objects.filter(dpto_ccdgo=depto_cdgo
                                                                   ), geometry_field='geom', fields=('mpio_cnmbr',))
        m = json.loads(sx)
        return Response(m)


class ListDeptos(APIView):
    permission_classes = (AllowAny,)

    # lista todos los nombres de los deptos y sus codigos.
    def get(self, request):
        qery = veredas.objects.values('nom_dep', 'cod_dpto').distinct()
        return Response(qery)


class ListMpios(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, depto_cdgo):
        qery = MunicipiosVeredas.objects.filter(
            dpto_ccdgo=depto_cdgo).values('mpio_cnmbr', 'mpio_ccdgo', 'dptompio', 'mpio_ccnct')
        print(depto_cdgo)
        print(qery)
        print('siga')
        return Response(qery)


class Verjson(APIView):
    permission_classes = (AllowAny,)

    # recibe la zona de interes sin tiempo
    # verifica que no haya nuevas en la API y si las hay las descarga.

    def get(self, request, mpio_cdgo):
        print('santiago')
        sx = serialize('geojson', veredas.objects.filter(dptompio=mpio_cdgo
                                                         ), geometry_field='geom', fields=('nombre_ver',))
        m = json.loads(sx)
        return Response(m)


class ListVdas(APIView):
    permission_classes = (AllowAny,)

    # lista las veredas dado el codigo de un municipio

    def get(self, request, mpio_cdgo):
        print('MANDE')
        query = veredas.objects.filter(
            dptompio=mpio_cdgo).values('nombre_ver', 'codigo_ver')
        return Response(query)


class JsonImgs(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        sx = serialize('geojson', Img.objects.all(),
                       geometry_field='geom_img', fields=('title', 'filedir', 'ingestion_date'))
        m = json.loads(sx)
        return Response(m)


class JsonImgsByReq(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, req):
        requri = Requeriments.objects.get(id=req)
        sx = serialize('geojson', Img.objects.filter(origin_requirement=requri),
                       geometry_field='geom_img', fields=('title', 'filedir', 'ingestion_date'))
        m = json.loads(sx)
        return Response(m)
