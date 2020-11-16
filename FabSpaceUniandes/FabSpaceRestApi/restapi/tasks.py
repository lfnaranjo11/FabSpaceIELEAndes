# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery import task
from time import sleep
import subprocess
import os
from .models import Requeriments, Img, veredas
from .serializers import ImgSerializer
from django.db import connection
from pathlib import Path
from .serializers import ImgSerializer, RequirementsSerializer
from bs4 import BeautifulSoup
from PIL import Image
from django.contrib.gis.geos import GEOSGeometry
import json


# from bs4 import BeautifulSoup
# SELECT the_geom FROM geom_tableWHERE ST_DWithin(the_geom, 'SRID=312;POINT(100000 200000)', 100)
# Select  ST_AsText(ST_SimplifyPreserveTopology(restapi_veredas.geom,1))  from restapi_veredas WHERE id=3

# checking and checking


def my_custom_sql(id_vereda):
    with connection.cursor() as cursor:
        cursor.execute(
            "Select ST_AsText(ST_SimplifyPreserveTopology(restapi_veredas.geom,1))  from restapi_veredas WHERE objectid=%s", [id_vereda])
        row = cursor.fetchone()
    return row


def check_value(value):
    if bool(value):
        return value
    else:
        return ''


def check_time_value(time):
    if bool(time):
        return str(str(time) + 'T00:00:00.000Z')
    else:
        return ''


def check_points(punto2, punto1):
    if bool(punto2) and bool(punto1):
        return str(punto1 + ':'+punto2)
    else:
        return ''


def check_vereda_poligon(vereda_object):
    if bool(vereda_object):
        print(vereda_object.objectid)
        # objectid = int(veredaid)
        resultado = my_custom_sql(vereda_object.objectid)
        print(resultado[0])
        return """'( footprint:"Intersects({})")'""".format(resultado[0])
    else:
        return ''


def appendtolist(listx, value, prefix):
    if bool(value):
        listx.append(prefix)
        listx.append(value)
        return listx
    else:
        return listx


def check_search_values(reqmt):
    user = 'lfnaranjo11'
    password = 'tijgAb-dyzxu2-pypsum'
    # query = """./restapi/dhusget.sh -l {} -u {} -p {} -m {} -T {} -s {} -e {} -S {} -E {} -c {} -F '(footprint:"Intersects(POLYGON(({})))")'  -o all """
    # qery =
    mission = check_value(reqmt.mission)
    ingestion_init_date = check_time_value(reqmt.ingestion_init_date)
    ingestion_end_date = check_time_value(reqmt.ingestion_end_date)
    sensing_init_date = check_time_value(reqmt.ingestion_end_date)
    sensing_end_date = check_time_value(reqmt.ingestion_end_date)
    product_type = check_value(reqmt.product_type)
    points = check_points(reqmt.punto1, reqmt.punto2)
    vereda_poligon = check_vereda_poligon(reqmt.vereda)
    original_qery = """./restapi/dhusget.sh"""
    querylist = [original_qery, '-l', '1', '-u', user, '-p', password]
    query = appendtolist(querylist, mission, '-m')
    query = appendtolist(querylist, ingestion_init_date, '-s')
    query = appendtolist(querylist, ingestion_end_date, '-e')
    query = appendtolist(querylist, sensing_init_date, '-S')
    query = appendtolist(querylist, sensing_end_date, '-E')
    query = appendtolist(querylist, product_type, '-T')
    query = appendtolist(querylist, points, '-c')
    query = appendtolist(querylist, vereda_poligon, '-F')
    return query

    # return query.format('1', user, password, mission, product_type, ingestion_init_date, ingestion_end_date, sensing_init_date, sensing_end_date, points, vereda_poligon)


def read_MTD(file_name, id):
    file_name2 = file_name+'.SAFE'
    path_file = Path(__file__).resolve().parent
    path_file = path_file.resolve().parent
    path_file = path_file.joinpath(file_name2)
    imgs_location = str(path_file)
    path_file = path_file.joinpath('MTD_MSIL2A.xml')
    path_string = str(path_file)
    print("img location is:", imgs_location)

    with open(path_string, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    cordenadas = Bs_data.Global_Footprint.EXT_POS_LIST.string
    image_uri = Bs_data.PRODUCT_URI.string
    hora = Bs_data.PRODUCT_START_TIME.string
    print(cordenadas)
    print(cordenadas.split(" "))
    pnt = points_to_multipoligon_object(str(cordenadas))
    print(str(pnt))
    print(hora)
    requri = Requeriments.objects.get(id=id)
    imagen = Img(title='call an ambulance', esa_uiid=image_uri, state='DISPONIBLE',
                 filedir=imgs_location, geom_img=GEOSGeometry(pnt), ingestion_date=hora,
                 origin_requirement=requri)
    salvada = imagen.save()
    print(salvada)
    #serializer = ImgSerializer(data=data)
    # if not serializer.is_valid():
    #    print(serializer.errors)
    #    print('not ok')
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #    serializer.save()
    #    print('super ok')
    # return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Bs_data.PRODUCT_TYPE


def odd_even_sieve(lista):
    output = lista[:]
    even_index, odd_index = 0, 1
    for i in range(len(lista)):
        if i % 2 == 0:
            output[even_index] = float(lista[i+1])
            even_index += 2
        else:
            output[odd_index] = float(lista[i-1])
            odd_index += 2
    return output


def points_to_multipoligon_object(points_string):
    points_list = points_string.split(" ")
    points_list = points_list[:-1]
    list_even_odd_ex = odd_even_sieve(points_list)
    chunks = [list_even_odd_ex[x:x+2]
              for x in range(0, len(list_even_odd_ex), 2)]
    data = {}
    data["type"] = "MultiPolygon"
    cord = [[chunks]]
    data["coordinates"] = cord
    print(str(data))
    pnt = GEOSGeometry(str(data))
    return pnt


def cropimage(path, name):
    #m = Image.open("hopper.jpg")
    # The crop method from the Image module takes four coordinates as input.
    # The right can also be represented as (left+width)
    # and lower can be represented as (upper+height).
    (left, upper, right, lower) = (20, 20, 100, 100)
    im = Image.open(path+'/'+name + ".jp2")
    # Here the image "im" is cropped and assigned to new variable im_crop
    im_crop = im.crop((left, upper, right, lower))
    im_crop.save(path + '/'+name + "croped.jp2")


def createThumbnail(path, name):
    size = 128, 128
    im = Image.open(path+'/'+name + ".jp2")
    im_resized = im.resize(size)
    #im.save(path + ".thumbnail", "JPEG")
    im_resized.save(path + '/'+name + "resized.jp2")


@ shared_task
def query_and_download(id):
    # TO-DO arreglar el poligono y revisar match de opciones
    # id es el id del requerimiento
    query_file = './restapi/queryfiles/{}.csv'
    query_file_instance = query_file.format(id)
    reqmt = Requeriments.objects.filter(id=id).first()
    statnmt = check_search_values(reqmt)
    statnmt.append('-o')
    statnmt.append('all')
    statnmt.append('-C')
    statnmt.append(query_file_instance)
    proc = subprocess.check_call(statnmt)
    f = open(query_file_instance, "r")
    valores = f.read()
    [name, uuidd_copernicus] = valores.split(',')
    img_file = './PRODUCT/{}.zip'.format(name)
    proc = subprocess.check_call(['unzip', img_file])
    read_MTD(name, id)
    return print(valores)


@ shared_task
def write_interest_zone_query():
    # parte 1 de infuture
    requiriments = Requeriments.objects.filter(download_state='EN-PROCESO')
    # un for talvez pero entonces solo de a 1.

    for rq in requiriments:
        byrequirement.apply_async(args=[rq.id, ])


@ shared_task
def byrequirement(rq_id):
    user = 'lfnaranjo11'
    rq = Requeriments.objects.filter(id=rq_id)
    password = 'tijgAb-dyzxu2-pypsum'
    mission = rq.mission
    qery2 = """./restapi/dhusget.sh -u {} -p {} -m {} -l 25 -F '(footprint:"Intersects(POLYGON(({})))")' -C './restapi/queryfiles/{rq_id}.csv' """
    queryset = qery2.format(user, password, mission)
    os.system(queryset)
    resultfile = open('./restapi/queryfiles/{rq_id}.csv', 'r')
    for line in resultfile:
        linea = line.split(',')
        print(line)
        serializer = ImgSerializer(img_uiid=linea[1])
        if not serializer.is_valid():
            print('error')
        else:
            serializer.save()
            print('bien escrita')


@ shared_task
def download_imgs_in_queu():
    imgs = Img.objects.filter(download_state='EN-PROCESO')
    for img in imgs:
        proccess_image.apply_async(args=[img.id, ])


@ shared_task
def proccess_image(img_id):
    # averiguar si esto se puede dejar sin terminar
    img = Img.objects.filter(id=img_id)
    img.img_uiid
    os.system(img.img_uiid)
    print('hola')

# WATCH LIST


@ shared_task
def watch_list():
    requiriments = Requeriments.objects.filter(watchlist='verdadero')
    for re in requiriments:
        qery2 = """./restapi/dhusget.sh -u {} -p {} -m {re.mission}  -F '(footprint:"Intersects(POLYGON(({re.vereda})))")'  -o ${bold}all${normal} -l 1 -t 24 """
