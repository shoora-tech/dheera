from django.db import models
from customer.models import Country
from dheera.models import UUIDModel

class PackingType(UUIDModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Currency(UUIDModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class SenderAddress(UUIDModel):
    head = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.head

class AdvanceTT(UUIDModel):
    advance_percentage = models.CharField(max_length=50)

    def __str__(self):
        return str(self.advance_percentage)

class BalanceTerm(UUIDModel):
    term = models.CharField(max_length=50)

    def __str__(self):
        return self.term

class DaysETA(UUIDModel):
    eta = models.CharField(max_length=50)

    def __str__(self):
        return self.eta
    


class PaymentTerms(UUIDModel):
    advacne_tt = models.ForeignKey(AdvanceTT, null=True, blank=True, on_delete=models.CASCADE, related_name="payment_term")
    balance_term = models.ForeignKey(BalanceTerm, null=True, blank=True, on_delete=models.CASCADE, related_name="payment_term")
    days_eta = models.ForeignKey(DaysETA, null=True, blank=True, on_delete=models.CASCADE, related_name="payment_term")

    def __str__(self):
        if self.advacne_tt and self.advacne_tt.advance_percentage:
            return f"{self.advacne_tt.advance_percentage} {self.balance_term} {self.days_eta}"
        return f"{self.balance_term} {self.days_eta}"


class PurchasePayTerms(UUIDModel):
    terms = models.TextField()

    def __str__(self):
        return self.terms


class PriceTerms(UUIDModel):
    terms = models.TextField()

    def __str__(self):
        return self.terms


class ShippingMarks(UUIDModel):
    remarks = models.TextField()

    def __str__(self):
        return self.remarks


class PIRemarks(UUIDModel):
    remarks = models.TextField()

    def __str__(self):
        return self.remarks


class PORemarks(UUIDModel):
    remarks = models.TextField()

    def __str__(self):
        return self.remarks



class Location(UUIDModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="location", null=True, blank=True)

    def __str__(self):
        return self.name


class AdvanceType(UUIDModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Advance(UUIDModel):
    advance_type = models.ForeignKey(AdvanceType, on_delete=models.CASCADE, related_name="advance")
    percentage = models.FloatField()
    remarks = models.TextField()
    quotaion = models.ForeignKey("Quotation", on_delete=models.CASCADE, related_name="advance")

    def __str__(self):
        return f"{self.advance_type} -- {self.percentage}"


class Status(UUIDModel):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class InspectionInstruction(UUIDModel):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class PackagingInstruction(UUIDModel):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class SpecialInstruction(UUIDModel):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class LCTTInstruction(UUIDModel):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class ShipmentMode(UUIDModel):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class DeliveryTerm(UUIDModel):
    name = models.TextField()

    def __str__(self):
        return self.name


class Consignee(UUIDModel):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name
