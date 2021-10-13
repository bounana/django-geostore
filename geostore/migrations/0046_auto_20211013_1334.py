# Generated by Django 3.2.7 on 2021-10-13 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geostore', '0045_auto_20210429_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='geom_type',
            field=models.IntegerField(choices=[(0, 'Point'), (1, 'LineString'), (3, 'Polygon'), (4, 'MultiPoint'), (5, 'MultiLineString'), (6, 'MultiPolygon'), (7, 'GeometryCollection')], null=True),
        ),
        migrations.AlterField(
            model_name='layerextrageom',
            name='geom_type',
            field=models.IntegerField(choices=[(0, 'Point'), (1, 'LineString'), (3, 'Polygon'), (4, 'MultiPoint'), (5, 'MultiLineString'), (6, 'MultiPolygon'), (7, 'GeometryCollection')], null=True),
        ),
    ]
