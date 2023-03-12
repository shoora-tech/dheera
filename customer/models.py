from django.db import models
from dheera.models import UUIDModel
from tyre.models import Brand
# Create your models here.

class Region(UUIDModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Country(UUIDModel):
    name = models.CharField(max_length=20)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="country", null=True)

    def __str__(self):
        return self.name

class Designation(UUIDModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class DesignatedPerson(UUIDModel):
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name="designated_person")
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="designation_person")


class CountryPotentialVolume(UUIDModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_potential_volume")
    potential = models.CharField(max_length=15, null=True, blank=True)
    volume_per_month = models.IntegerField(null=True, blank=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="country_potential_volume")

class PastTurnouver(UUIDModel):
    year = models.IntegerField()
    turnover = models.FloatField()
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="past_turnover")

class BrandShare(UUIDModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="brand_share")
    brand_share = models.FloatField(null=True, blank=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="brand_share")


class ProductCategory(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductSoldVolume(UUIDModel):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="product_sold_volume")
    volume_per_month = models.IntegerField(null=True, blank=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="product_sold_volume")


class OtherBuissness(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class OtherBuisennessTurnover(UUIDModel):
    other_buiseness = models.ForeignKey(OtherBuissness, on_delete=models.CASCADE, related_name="other_buiseness_turnover")
    turnover = models.FloatField()
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="other_buiseness_turnover")


class PotentialSale(UUIDModel):
    year = models.IntegerField()
    turnover = models.FloatField()
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="potential_sale")


class SMRecomendationreason(UUIDModel):
    reason = models.TextField()
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="recommendation")

    


class Customer(UUIDModel):
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    buiseness_start_year = models.IntegerField(null=True, blank=True)
    # smr_recommendation_reason = models.ManyToManyField(SMRecomendationreason)
    aj_remarks = models.TextField(null=True, blank=True)
    ceo_remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name
