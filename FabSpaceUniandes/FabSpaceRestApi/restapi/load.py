from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import WorldBorder, veredas, MunicipiosVeredas, DepartamentosVeredas
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
    'cod_dpto': {'dpto_ccdgo': 'COD_DPTO'},  # foreign key field
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON25D',
}

# Auto-generated `LayerMapping` dictionary for DepartamentosVeredas model
departamentosveredas_mapping = {
    'dpto_ccdgo': 'DPTO_CCDGO',
    'geom': 'MULTIPOLYGON25D',
}
# Auto-generated `LayerMapping` dictionary for MunicipiosVeredas model
municipiosveredas_mapping = {
    'dptompio': 'DPTOMPIO',
    #  'dpto_ccdgo': 'DPTO_CCDGO',
    'dpto_ccdgo': {'dpto_ccdgo': 'DPTO_CCDGO'},
    'mpio_ccdgo': 'MPIO_CCDGO',
    'mpio_cnmbr': 'MPIO_CNMBR',
    'mpio_ccnct': 'MPIO_CCNCT',
    'geom': 'MULTIPOLYGON25D',
}
# str(world_shp)
world_shp = Path(__file__).resolve().parent / 'data' / \
    'TM_WORLD_BORDERS-0.3'/'TM_WORLD_BORDERS-0.3.shp'
ds = DataSource(str(world_shp))


world_shp2 = Path(__file__).resolve().parent / 'data' / \
    'VEREDASv28'/'VEREDAS_V27.shp'
ds2 = DataSource(str(world_shp2))

world_shp3 = Path(__file__).resolve().parent / 'data' / \
    'VEREDASv28'/'DepartamentosVeredas.shp'
ds3 = DataSource(str(world_shp3))

world_shp4 = Path(__file__).resolve().parent / 'data' / \
    'VEREDASv28'/'MunicipiosVeredas.shp'
ds4 = DataSource(str(world_shp4))


def run(verbose=True):
    numfeatures_veredas=32305

    #lm = LayerMapping(WorldBorder, ds, world_mapping, transform=False)
   #lm.save(strict=True, verbose=verbose)
    lm2 = LayerMapping(veredas, ds2, veredas_mapping, transaction_mode= 'autocommit',transform=False)
    lm2.save(strict=False, fid_range=(0,5000),verbose=False,progress=True,step=500)
    lm2.save(strict=False,fid_range=(5001,15000), verbose=False,progress=True,step=500)
       lm2.save(strict=False,fid_range=(15001,20000), verbose=False,progress=True,step=500)
    lm2.save(strict=False,fid_range=(20001,25000), verbose=False,progress=True,step=500)
    lm2.save(strict=False,fid_range=(25001,32305), verbose=False,progress=True,step=500)

    # lm3 = LayerMapping(DepartamentosVeredas, ds3,
    #                 departamentosveredas_mapping, transform = False)
    # lm3.save(strict=True, verbose=verbose)
    # lm4 = LayerMapping(MunicipiosVeredas, ds4,
    #                 municipiosveredas_mapping, transform = False)
    # lm4.save(strict=True, verbose=verbose)
