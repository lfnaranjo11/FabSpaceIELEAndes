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
#from bs4 import BeautifulSoup
# SELECT the_geom FROM geom_tableWHERE ST_DWithin(the_geom, 'SRID=312;POINT(100000 200000)', 100)
# Select  ST_AsText(ST_SimplifyPreserveTopology(restapi_veredas.geom,1))  from restapi_veredas WHERE id=3


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
        #objectid = int(veredaid)
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


@ shared_task
def query_and_download(id):
    # TO-DO arreglar el poligono y revisar match de opciones
    # now
    query_file = './restapi/queryfiles/{}.csv'
    query_file_instance = query_file.format(id)
    reqmt = Requeriments.objects.filter(id=id).first()
    statnmt = check_search_values(reqmt)
    statnmt.append('-o')
    statnmt.append('all')
    statnmt.append('-C')
    statnmt.append(query_file_instance)
    proc = subprocess.check_call(statnmt)
    # try:
    #    outs, errs = proc.communicate(timeout=100)
    # except TimeoutExpired:
    #    proc.kill()
    #    outs, errs = proc.communicate()
    f = open(query_file_instance, "r")
    valores = f.read()
    [name, uuidd_copernicus] = valores.split(',')
    img_file = './PRODUCT/{}.zip'.format(name)
    proc = subprocess.check_call(['unzip', img_file])
   # response = urllib2.urlopen(
    #    'http://tutorialspoint.com/python/python_overview.htm')
    #html_doc = response.read()

    #soup = BeautifulSoup(html_doc, 'html.parser')

    # print(soup.title)

    return print(valores)

# INFUTURE


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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    # os.system(queryset)
    # leer el csv e ir escribiendo las imagenes a la base de datos


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
