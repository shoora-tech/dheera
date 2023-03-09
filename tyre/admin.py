from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(TyreSize)
admin.site.register(PR)
admin.site.register(TyreSet)
admin.site.register(Brand)
admin.site.register(Pattern)
admin.site.register(Position)
admin.site.register(LoadIndex)
admin.site.register(SpeedRating)
admin.site.register(TyreDepth)
admin.site.register(ContainerType)
admin.site.register(PaymentBasis)
admin.site.register(Certificate)
admin.site.register(Stuff)
admin.site.register(StuffType)
admin.site.register(StuffMaster)

@admin.register(Tyre)
class TyreAdmin(admin.ModelAdmin):
    list_display = (
        "tyre_size",
        "pr",
        "tyre_set",
        "brand",
        "pattern",
        "position",
        "load_index",
        "speed_rating",
        "tyre_depth",
        "container_type",
        "stuff",
        "certificate"
    )

    search_fields = (
        "brand",
        "tyre_size",
        "pattern",
        "container_type"
    )
