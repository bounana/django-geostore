import mercantile

from django.views.generic import View

from django.contrib.gis.geos.geometry import GEOSGeometry
from django.core.serializers import serialize
from django.db.models import Count, Value
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import get_object_or_404


from .funcs import ST_Intersects, ST_Transform, ST_MakeEnvelope, ST_AsMvtGeom
from ..models import Layer, Feature

class MVTView(View):
    def get_tile(self):
        bounds = mercantile.bounds(self.x, self.y, self.z)
        xmin, ymin = mercantile.xy(bounds.west, bounds.south)
        xmax, ymax = mercantile.xy(bounds.east, bounds.north)
        
        layer_query = self.layer.features.annotate(
                bbox=ST_MakeEnvelope(xmin, ymin, xmax, ymax, 3857)
            ).annotate(
                intersect=ST_Intersects(
                            ST_Transform('geom', 3857),
                            'bbox'
                        ),
            ).filter(
                intersect=True
            ).annotate(
                geometry=ST_AsMvtGeom(
                    ST_Transform('geom', 3857),
                    'bbox',
                    4096,
                    256,
                    True
                )
            )
        
        mvt_query = Feature.objects.raw(
            f'''
            WITH tilegeom as ({layer_query.query})
            SELECT {self.layer.pk} AS id, count(*) AS count, ST_AsMVT(tilegeom, 'name', 4096, 'geometry') AS mvt
            FROM tilegeom
            '''
        )
        return mvt_query[0]

    def get(self, request, layer_pk, z, x, y):
        self.layer = get_object_or_404(Layer, pk=layer_pk)
        self.z = z
        self.x = x
        self.y = y

        qs = self.get_tile()
        if qs.count > 0:
            return HttpResponse(qs.mvt, content_type="application/vnd.mapbox-vector-tile")
        else:
            return HttpResponseNotFound()


class IntersectView(View):
    def post(self, request, layer_pk):
        layer = get_object_or_404(Layer, pk=layer_pk)

        try:
            geometry = GEOSGeometry(request.POST.get('geom', None))
        except TypeError:
            return HttpResponseBadRequest(content='Provided geometry is nod valid')

        return HttpResponse(
                serialize('geojson',
                        layer.features.intersects(geometry),
                        fields=('properties',),
                        geometry_field='geom',
                        properties_field='properties'),
                content_type='application/vnd.geo+json'
                )
