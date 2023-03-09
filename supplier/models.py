from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from dheera.models import UUIDModel
from tyre.models import Brand
from customer.models import Country, ProductCategory, Designation
from tyre.models import StuffType, TyreSize, PR, TyreSet, Brand, Pattern, PaymentBasis, Stuff
# Create your models here.

class DesignatedPerson(UUIDModel):
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name="supplier_designated_person")
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE, related_name="supplier_designation_person")


class ProductSoldVolume(UUIDModel):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="supplier_product_sold_volume")
    volume_per_month = models.IntegerField(null=True, blank=True)
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE, related_name="supplier_product_sold_volume")



class Supplier(UUIDModel):
    name = models.CharField(max_length=100)
    address = models.TextField()
    buiseness_start_year = models.IntegerField(null=True, blank=True)
    inception_year = models.IntegerField(null=True, blank=True)
    brand = models.ManyToManyField(Brand)
    country = models.ManyToManyField(Country)
    aj_remarks = models.TextField(null=True, blank=True)
    ceo_remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name




class SupplierSKU(UUIDModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_sku")
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="supplier_sku")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="supplier_sku")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="supplier_sku")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="supplier_sku")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="supplier_sku")
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name="supplier_sku", null=True)
    quantity = models.IntegerField()
    number_of_containers = models.FloatField(null=True, verbose_name="No. of containers")
    cost = models.FloatField()


class SupplierSKUSummary(UUIDModel):
    sku = models.ForeignKey("SupplierSKU", on_delete=models.CASCADE, related_name="supplier_sku_summary", null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="supplier_sku_summary", null=True)
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="supplier_sku_summary", null=True)
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="supplier_sku_summary", null=True)
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="supplier_sku_summary", null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="supplier_sku_summary", null=True)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="supplier_sku_summary", null=True)
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name="supplier_sku_summary", null=True)
    quantity = models.IntegerField(null=True)
    number_of_containers = models.FloatField(null=True, verbose_name="No. of containers")
    cost = models.FloatField(null=True)


@receiver(post_save, sender=SupplierSKU)
def create_supplier_sku_summary(sender, instance=None, created=False, **kwargs):
    if instance:
        SupplierSKUSummary.objects.create(
            sku=instance,
            supplier = instance.supplier,
            tyre_size=instance.tyre_size,
            pr=instance.pr,
            tyre_set=instance.tyre_set,
            brand=instance.brand,
            pattern=instance.pattern,
            stuff=instance.stuff,
            quantity=instance.quantity,
            number_of_containers=instance.number_of_containers,
            cost=instance.cost,
            created_at=instance.updated_at
        )

