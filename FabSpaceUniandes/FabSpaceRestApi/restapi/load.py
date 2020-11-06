from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import WorldBorder, veredas
from django.contrib.gis.gdal import DataSource
world_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'mpoly': 'MULTIPOLYGON',
}


# Auto-generated `LayerMapping` dictionary for veredas model
veredas_mapping = {
    'objectid': 'OBJECTID',
    'dptompio': 'DPTOMPIO',
    'codigo_ver': 'CODIGO_VER',
    'nom_dep': 'NOM_DEP',
    'nomb_mpio': 'NOMB_MPIO',
    'nombre_ver': 'NOMBRE_VER',
    'vigencia': 'VIGENCIA',
    'fuente': 'FUENTE',
    'descripcio': 'DESCRIPCIO',
    'seudonimos': 'SEUDONIMOS',
    'area_ha': 'AREA_HA',
    'cod_dpto': 'COD_DPTO',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON25D',
}
# str(world_shp)
world_shp = Path(__file__).resolve().parent / 'data' / \
    'TM_WORLD_BORDERS-0.3'/'TM_WORLD_BORDERS-0.3.shp'
ds = DataSource(str(world_shp))
lyr = ds[0]
srs = lyr.srs

world_shp2 = Path(__file__).resolve().parent / 'data' / \
    'VEREDASv28'/'VEREDAS_V27.shp'
ds2 = DataSource(str(world_shp2))


def run(verbose=True):
    print(str(world_shp))
    # print(ds)
    # print(srs)
    # print('hola')
    lm = LayerMapping(WorldBorder, ds, world_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
    lm2 = LayerMapping(veredas, ds2, veredas_mapping, transform=False)
    lm2.save(strict=True, verbose=verbose)
