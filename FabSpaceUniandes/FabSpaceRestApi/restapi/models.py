from django.db import models
from django.contrib.gis.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
NOT_PROCESSED = 'NP'
ADDED = 'ADDED'
PROCESSED_CHOICES = [
    (NOT_PROCESSED, 'Not proccesed'),
    (ADDED, 'Added url')
]


DOWNLOAD_STATE_CHOICES = [
    ('EN-PROCESO', 'EN-PROCESO'),
    ('DISPONIBLE', 'DISPONIBLE'),
    ('CORTADA', 'CORTADA')
]


REQUIREMENT_STATE_CHOICES = [
    ('WATCHLIST', 'WATCHLIST'),
    ('NOW', 'NOW'),
    ('EVENTUAL', 'EVENTUAL')
]

MISSION_CHOICES = [
    ('Sentinel-1', 'Sentinel-1'),
    ('Sentinel-2', 'Sentinel-2'),
    ('Sentinel-3', 'Sentinel-3'),
    ('Sentinel-5 P', 'Sentinel-5 P')

]


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name


class DepartamentosVeredas(models.Model):
    dpto_ccdgo = models.CharField(max_length=2, primary_key=True, unique=True)
    geom = models.MultiPolygonField(srid=4326)


class MunicipiosVeredas(models.Model):
    dptompio = models.CharField(max_length=5, primary_key=True, unique=True)
    dpto_ccdgo = models.ForeignKey(
        DepartamentosVeredas, on_delete=models.CASCADE)
    mpio_ccdgo = models.CharField(max_length=3)
    mpio_cnmbr = models.CharField(max_length=60)
    mpio_ccnct = models.CharField(max_length=5)
    geom = models.MultiPolygonField(srid=4326)


class veredas(models.Model):

    objectid = models.IntegerField(primary_key=True)
    dptompio = models.CharField(max_length=5)
    codigo_ver = models.CharField(max_length=11)
    nom_dep = models.CharField(max_length=50)
    nomb_mpio = models.CharField(max_length=50)
    nombre_ver = models.CharField(max_length=50)
    vigencia = models.CharField(max_length=4)
    fuente = models.CharField(max_length=50)
    descripcio = models.CharField(max_length=50)
    seudonimos = models.CharField(max_length=250)
    area_ha = models.FloatField()
    cod_dpto = models.ForeignKey(
        DepartamentosVeredas, on_delete=models.CASCADE)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)


class Requeriments(models.Model):
    # requirement identification. used to identify the type of query
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)  # unique identifier
    state = models.TextField(
        max_length=100, choices=REQUIREMENT_STATE_CHOICES)

    # filename of the qery valid for everyone but usefull for future
    query_filename = models.TextField(max_length=100, blank=True,  null=True
                                      )
    # title of the requirement given by the user to help with identification
    title = models.CharField(max_length=300,  blank=True,  null=True
                             )
    # description  of the requirement given by the user to help with identification
    description = models.TextField(max_length=300,  blank=True, null=True
                                   )
    group = models.TextField(max_length=500,  blank=True, null=True)

    # group given by the user to help with identification

    ##############################################################
    ###################query options##############################
    ##############################################################
    # time related
    ingestion_init_date = models.DateField(blank=True, null=True)  # -s
    ingestion_end_date = models.DateField(blank=True, null=True)  # -e
    sensing_end_date = models.DateField(blank=True,  null=True)  # -S
    sensing_init_date = models.DateField(blank=True, null=True)  # -E
    time_in_hours = models.IntegerField(blank=True,  null=True)  # -t

    # location related.
    # cuando la ubicacion se usa entre dos puntos parametro -c p1:p2
    punto1 = models.TextField(blank=True, null=True)
    punto2 = models.TextField(blank=True, null=True)
    # TEMPORAL TO BE DEPRECATED. usar solo cuando los puntos no son parte de la base de datos #temporal
    puntos = models.MultiPolygonField(srid=4326,  blank=True, null=True)
    vereda = models.ForeignKey(
        veredas, on_delete=models.CASCADE,  blank=True, null=True)

    product_type = models.TextField(blank=True, null=True)
    mission = models.TextField(
        choices=MISSION_CHOICES,   blank=True, null=True)  # -m
    instrument_name = models.TextField(blank=True, null=True)
    cloud_cover = models.DecimalField(
        decimal_places=2, max_digits=3,  blank=True,  null=True)
    # number of results  if eventual max is mayor if now max is just 3 if watchlist dont midn
    expected_total_img_number = models.IntegerField(blank=True,  null=True, validators=[MinValueValidator(1),
                                                                                        MaxValueValidator(100)])  # l

    ##############################################################
    #######################query options end #####################
    ##############################################################
    # deprecated
   # img_uiid = models.TextField(max_length=100)
    # multi = models.IntegerField(max_length=100)


class Img(models.Model):
    ##############################################################
    ################### database and user identificators ###################
    ##############################################################
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    # esa_copernicus_identifier
    esa_uiid = models.TextField(max_length=100)

    state = models.TextField(
        max_length=100, choices=DOWNLOAD_STATE_CHOICES)  # estado de descarga de la imagen.
    # direction of the image & files
    filedir = models.TextField(max_length=100)

    ##############################################################
    ################### informacion geografica ###################
    ##############################################################

    ingestion_date = models.DateTimeField()
    geom_img = models.MultiPolygonField(srid=4326)  # la locacion de la imagen
    origin_requirement = models.ForeignKey(
        Requeriments, on_delete=models.CASCADE)

    # TO-DO cortar pedazos y crear nueva imagen. esa_uuid null


class APIUsers(models.Model):
    usuario = models.CharField(max_length=300)
    clave = models.TextField(max_length=500)
    details = models.TextField(max_length=500)
