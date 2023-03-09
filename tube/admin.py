from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(TubeSize)
admin.site.register(ValveSize)
admin.site.register(Weight)
admin.site.register(QuantityType)
# admin.site.register(Brand)

@admin.register(Tube)
class TubeAdmin(admin.ModelAdmin):
    list_display = ("brand", "tube_size", "valve_size", "weight", "quantity_type")
    search_fields = ("brand", "tube_size", "valve_size", "weight", "quantity_type")