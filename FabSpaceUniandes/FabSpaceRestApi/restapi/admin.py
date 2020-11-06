from .models import WorldBorder, veredas

from django.contrib.gis import admin
#from django.contrib import admin
from .models import Img

# Register your models here.
# admin.site.register(Img)

admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(veredas, admin.GeoModelAdmin)
admin.site.register(Img)
