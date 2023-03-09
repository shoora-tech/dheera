from django.db import models
from dheera.models import UUIDModel
from tyre.models import Brand
# Create your models here.

class TubeSize(UUIDModel):
    size = models.CharField(max_length=15)

    def __str__(self):
        return self.size

class ValveSize(UUIDModel):
    size = models.CharField(max_length=15)

    def __str__(self):
        return self.size

class Weight(UUIDModel):
    weight = models.IntegerField()

    def __str__(self):
        return self.weight

class QuantityType(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tube(UUIDModel):
    tube_size = models.ForeignKey(TubeSize, on_delete=models.CASCADE, related_name="tube")
    valve_size = models.ForeignKey(ValveSize, on_delete=models.CASCADE, related_name="tube")
    weight = models.ForeignKey(Weight, on_delete=models.CASCADE, related_name="tube")
    quantity_type = models.ForeignKey(QuantityType, on_delete=models.CASCADE, related_name="tube")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="tube")


