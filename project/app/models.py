from django.db import models


class Station(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    routes = models.ManyToManyField('Route', related_name="stations", verbose_name='Направления')
    name = models.CharField(max_length=40, verbose_name='Имя направлений')

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=40, verbose_name='Имя направления')

    def __str__(self):
        return self.name
