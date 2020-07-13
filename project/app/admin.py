from django.contrib import admin


from .models import Station, Route


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass
