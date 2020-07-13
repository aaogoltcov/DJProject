import csv
import os

import tqdm as tqdm
from django.core.management.base import BaseCommand, CommandError

from app.models import Station, Route
from project.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Import stations from CSV'

    def handle(self, *args, **options):
        self.db_upload(os.path.join(BASE_DIR, 'project/moscow_bus_stations.csv'))

    @staticmethod
    def station_save_to_db(item, station):
        # Если записи в БД нет - создаем запись
        item = Station(latitude=station['latitude'],
                       longitude=station['longitude'],
                       name=station['name'], )
        item.save()
        # Делаем привязку к routes
        for route in station['routes']:
            item.routes.add(Route.objects.filter(name=route).values('id')[0]['id'])
            item.save()

    def db_upload(self, file):
        print(f'Читаем файл {file} ...')
        with open(file, encoding='Windows-1251') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            csv_list = []
            routes_list = []
            for row in reader:
                csv_list.append({'latitude': row['Latitude_WGS84'],
                                 'longitude': row['Longitude_WGS84'],
                                 'name': row['Name'],
                                 'routes': row['RouteNumbers']})
            # Очистка списка от одинаковых словарей
            csv_list = [dict(tuple_item) for tuple_item in {tuple(dictionary.items()) for dictionary in csv_list}]

            # Переводим направления в список, а также получаем список направлений
            for item in csv_list:
                item['routes'] = item['routes'].split('; ')
                routes_list.extend(item['routes'])

            # При записи в БД направлений предварительно убираем дубликаты
            print('Записываем направления...')
            for route in set(routes_list):
                try:
                    if Route.objects.filter(name=route).values('name')[0]['name'] == route:
                        pass
                    else:
                        Route(name=route).save()
                except IndexError:
                    Route(name=route).save()

            # Записываем в БД станции (дубликаты уже все убраны)
            print('Записываем станции...')
            for station in csv_list:
                try:
                    if len(Station.objects.filter(name=station['name']).values('routes__name').all()) > 0 and \
                            len(Station.objects.filter(name=station['name']).values('name').all()) > 0:
                        for routes__name in Station.objects.filter(name=station['name']).values('routes__name').all():
                            # Если запись в БД существует - пропускаем
                            if len(Station.objects.filter(name=station['name']).values('routes__name').all()) > 0 and \
                                    routes__name['routes__name'] in station['routes'] and \
                                    Station.objects.filter(name=station['name']).values('name')[0]['name'] == station['name']:
                                pass
                            else:
                                self.station_save_to_db(item, station)
                    else:
                        self.station_save_to_db(item, station)
                except IndexError:
                    self.station_save_to_db(item, station)
