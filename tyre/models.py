from django.db import models
from dheera.models import UUIDModel
# Create your models here.

class TyreSize(UUIDModel):
    size = models.CharField(max_length=15)

    def __str__(self):
        return self.size

class PR(UUIDModel):
    pr = models.CharField(max_length=15)

    def __str__(self):
        return self.pr

class TyreSet(UUIDModel):
    tyre_set = models.CharField(
        verbose_name="SET",
        max_length=15
    )

    def __str__(self):
        return self.tyre_set

class Brand(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Pattern(UUIDModel):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Position(UUIDModel):
    position_type = models.CharField(max_length=15)

    def __str__(self):
        return self.position_type

class LoadIndex(UUIDModel):
    index = models.CharField(max_length=15)

    def __str__(self):
        return self.index

class SpeedRating(UUIDModel):
    speed_rating = models.CharField(max_length=15)

    def __str__(self):
        return self.speed_rating

class TyreDepth(UUIDModel):
    depth = models.CharField(max_length=15)

    def __str__(self):
        return self.depth

class ContainerType(UUIDModel):
    container_type = models.CharField(max_length=15)

    def __str__(self):
        return self.container_type

class PaymentBasis(UUIDModel):
    payment_basis = models.CharField(max_length=15)

    def __str__(self):
        return self.payment_basis

class Certificate(UUIDModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Stuff(UUIDModel):
    pcs = models.IntegerField()

    def __str__(self):
        return str(self.pcs)


class StuffType(UUIDModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tyre(UUIDModel):
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="tyre")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="tyre")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="tyre")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="tyre")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="tyre")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="tyre")
    load_index = models.ForeignKey(LoadIndex, on_delete=models.CASCADE, related_name="tyre")
    speed_rating = models.ForeignKey(SpeedRating, on_delete=models.CASCADE, related_name="tyre")
    tyre_depth = models.ForeignKey(TyreDepth, on_delete=models.CASCADE, related_name="tyre")
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name="tyre", null=True)
    stuff_type = models.ForeignKey(StuffType, on_delete=models.CASCADE, related_name="tyre", null=True)
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="tyre")
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, related_name="tyre")


class StuffMaster(UUIDModel):
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="stuff_master")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="stuff_master")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="stuff_master")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="stuff_master")
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="stuff_master")
    stuff = models.FloatField()
