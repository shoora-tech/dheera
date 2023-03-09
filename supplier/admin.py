from uuid import uuid4
from django.contrib import admin
from .models import *
# Register your models here.

class DesignatedPersonInline(admin.TabularInline):
    fields = ("name", "email", "phone", "designation")
    extra = 0
    model = DesignatedPerson

class ProductSoldVolumeInline(admin.TabularInline):
    fields = ("product_category", "volume_per_month")
    extra = 0
    model = ProductSoldVolume

@admin.register(Supplier)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "buiseness_start_year",
    )
    inlines = (
        DesignatedPersonInline,
        ProductSoldVolumeInline,
    )

@admin.register(SupplierSKU)
class SupplierSKUAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "tyre_size",
        "pr",
        "pattern",
        "cost",
        "created_at",
        "updated_at"
    )


@admin.register(SupplierSKUSummary)
class SupplierSKUSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "tyre_size",
        "pr",
        "pattern",
        "cost",
        "created_at",
        "updated_at"
    )
    
    def has_change_permission(self, request, obj=None):
        return False
