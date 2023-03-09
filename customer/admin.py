from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *
# Register your models here.

admin.site.register(Country)
admin.site.register(Designation)
admin.site.register(ProductCategory)
admin.site.register(OtherBuissness)

admin.site.register(SMRecomendationreason)
class SMRecomendationreasonInline(admin.TabularInline):
    fields = ("reason", )
    extra = 0
    model = SMRecomendationreason

@admin.register(DesignatedPerson)
class DesignatedPersonAdmin(ModelAdmin):
    list_display = ("name", "email", "phone", "designation")

class DesignatedPersonInline(admin.TabularInline):
    fields = ("name", "email", "phone", "designation")
    extra = 0
    model = DesignatedPerson



@admin.register(CountryPotentialVolume)
class CountryPotentialVolumeAdmin(ModelAdmin):
    list_display = ("country", "potential", "volume_per_month")

class CountryPotentialVolumeInline(admin.TabularInline):
    fields = ("country", "potential", "volume_per_month")
    extra = 0
    model = CountryPotentialVolume

@admin.register(PastTurnouver)
class PastTurnouverAdmin(ModelAdmin):
    list_display = ("year", "turnover")

class PastTurnouverInline(admin.TabularInline):
    fields = ("year", "turnover")
    extra = 0
    model = PastTurnouver

@admin.register(BrandShare)
class BrandShareAdmin(ModelAdmin):
    list_display = ("brand", "brand_share",)

class BrandShareInline(admin.TabularInline):
    fields = ("brand", "brand_share",)
    extra = 0
    model = BrandShare

@admin.register(ProductSoldVolume)
class ProductSoldVolumeAdmin(ModelAdmin):
    list_display = ("product_category", "volume_per_month")

class ProductSoldVolumeInline(admin.TabularInline):
    fields = ("product_category", "volume_per_month")
    extra = 0
    model = ProductSoldVolume

@admin.register(OtherBuisennessTurnover)
class OtherBuisennessTurnoverAdmin(ModelAdmin):
    list_display = ("other_buiseness", "turnover")

class OtherBuisennessTurnoverInline(admin.TabularInline):
    fields = ("other_buiseness", "turnover")
    extra = 0
    model = OtherBuisennessTurnover

@admin.register(PotentialSale)
class PotentialSaleAdmin(ModelAdmin):
    list_display = ("year", "turnover")

class PotentialSaleInline(admin.TabularInline):
    fields = ("year", "turnover")
    extra = 0
    model = PotentialSale

@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = (
        "company_name",
        "address",
        "buiseness_start_year",
    )
    inlines = (
        DesignatedPersonInline,
        CountryPotentialVolumeInline,
        PastTurnouverInline,
        BrandShareInline,
        ProductSoldVolumeInline,
        OtherBuisennessTurnoverInline,
        PotentialSaleInline,
        SMRecomendationreasonInline
    )

