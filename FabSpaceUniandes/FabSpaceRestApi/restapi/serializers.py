from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Img, Requeriments, veredas, WorldBorder

# UserModel = get_user_model()


class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['id', 'title', 'esa_uiid', 'filedir', 'state',
                  'ingestion_date', 'geom_img', 'origin_requirement']


class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requeriments
        fields = ['id', 'state', 'query_filename', 'title', 'description', 'group', 'title', 'ingestion_init_date', 'ingestion_end_date', 'sensing_end_date',
                  'sensing_init_date', 'time_in_hours', 'punto1', 'punto2', 'puntos', 'vereda', 'product_type', 'mission', 'instrument_name', 'cloud_cover', 'expected_total_img_number']


class VeredasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Img
        fields = ['objectid', 'dptompio', 'codigo_ver', 'nom_dep', 'nomb_mpio',
                  'nombre_ver', 'vigencia', 'fuente', 'descripcion', 'seudonimos', 'area_ha', 'cod_dpto', 'shape_leng', 'shape_area', 'geom']
