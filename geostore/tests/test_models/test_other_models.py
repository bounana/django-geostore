from unittest import mock

from django.contrib.gis.geos import GEOSGeometry, Point
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils.text import slugify

from geostore import GeometryTypes
from geostore.models import LayerExtraGeom, Feature, geom_changed
from geostore import settings as app_settings
from geostore.tests.factories import LayerSchemaFactory


class LayerExtraGeomModelTestCase(TestCase):
    def setUp(self):
        self.layer_schema = LayerSchemaFactory()
        self.extra_layer = LayerExtraGeom.objects.create(layer=self.layer_schema,
                                                         geom_type=GeometryTypes.Point,
                                                         title='Test')

    def test_str(self):
        self.assertEqual(str(self.extra_layer),
                         f'{self.extra_layer.title} ({str(self.layer_schema)})')

    def test_name(self):
        self.assertEqual(self.extra_layer.name,
                         f'{slugify(self.extra_layer.layer.name)}-{self.extra_layer.slug}')


class FeatureTestCase(TestCase):
    def setUp(self):
        self.layer_schema = LayerSchemaFactory()

    def test_clean(self):
        feature = Feature.objects.create(layer=self.layer_schema,
                                         geom='POINT(0 0)',
                                         properties={
                                             'name': 'toto'
                                         })
        feature.clean()
        self.assertIsNotNone(feature.pk)

    def test_feature_geom_3d_to_2d(self):
        feature = Feature.objects.create(layer=self.layer_schema,
                                         geom='POINT(0 0 0)',
                                         properties={
                                             'name': 'toto'
                                         })
        self.assertEqual(feature.geom, Point(0, 0, srid=app_settings.INTERNAL_GEOMETRY_SRID))

    def test_constraint_feature_empty_geom(self):
        with self.assertRaises(IntegrityError):
            Feature.objects.create(layer=self.layer_schema,
                                   geom='POINT EMPTY',)

    def test_constraint_feature_valid_geom(self):
        with self.assertRaises(IntegrityError):
            Feature.objects.create(layer=self.layer_schema,
                                   geom='POLYGON((0 0, 1 1, 1 2, 1 1, 0 0))',)

    def test_feature_saving_signal(self):
        # Created
        with mock.patch('geostore.models.save_feature') as mock_create:
            feature = Feature.objects.create(layer=self.layer_schema,
                                             geom='POINT(0 1)')
            mock_create.assert_called_once_with(instance=feature, sender=Feature, signal=geom_changed)

        # Geom is not changed
        with mock.patch('geostore.models.save_feature') as mock_save_properties:
            feature.properties = {}
            feature.save()
            mock_save_properties.assert_not_called()

        # Geom is the same
        with mock.patch('geostore.models.save_feature') as mock_save_same_geom:
            feature.geom = GEOSGeometry('''{
                      "type": "Point",
                      "coordinates": [
                        0,
                        1
                      ]
                    }''')
            feature.save()
            mock_save_same_geom.assert_not_called()

        # Geom changed
        with mock.patch('geostore.models.save_feature') as mock_save_same_geom:
            feature.geom = GEOSGeometry('''{
                      "type": "Point",
                      "coordinates": [
                        2,
                        49
                      ]
                    }''')
            feature.save()
            mock_save_same_geom.assert_called_once_with(instance=feature, sender=Feature, signal=geom_changed)
