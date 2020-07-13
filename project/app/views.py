from django.shortcuts import render

from .models import Route, Station


def project_view(request):
    context = {
        'routes': Route.objects.values('name').all(),
        'center': {'y': 55.753960, 'x': 37.620393},
    }
    return render(request, 'stations.html', context)


def route_view(request):
    context = {
        'stations': Station.objects.filter(routes__name=request.GET['route']).values('latitude',
                                                                                     'longitude',
                                                                                     'name',
                                                                                     'routes__name').all(),
        'routes': Route.objects.values('name').all(),
        'center': {'y': Station.objects.filter(routes__name=request.GET['route']).values('latitude')[0]['latitude'],
                   'x': Station.objects.filter(routes__name=request.GET['route']).values('longitude')[0]['longitude'],
                  },
    }
    return render(request, 'stations.html', context)
