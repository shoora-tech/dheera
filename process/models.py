from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from dheera.models import UUIDModel
from supplier.models import Supplier
from tyre.models import StuffType, TyreSize, PR, TyreSet, Brand, Pattern, PaymentBasis, Stuff, ContainerType, StuffMaster
from customer.models import Country, Customer, Region
from django.utils import timezone
from datetime import datetime
from simple_history.models import HistoricalRecords
from account.models import User

# Create your models here.

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

class PaymentTerms(UUIDModel):
    terms = models.TextField()

    def __str__(self):
        return self.terms


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

    def __str__(self):
        return self.name


class SKU(UUIDModel):
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="sku")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="sku")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="sku")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="sku")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="sku")
    # stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name="sku", null=True)
    # )
    quantity = models.IntegerField(default=0)
    number_of_containers = models.FloatField(null=True, blank=True, verbose_name="No. of containers")
    price = models.FloatField()
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="sku", null=True, blank=True)
    stuffing = models.ForeignKey(StuffMaster, on_delete=models.CASCADE, null=True, blank=True)
    # expected_price
    quotaion = models.ForeignKey("Quotation", on_delete=models.CASCADE, related_name="sku")
    pi = models.ForeignKey("PerformaInvoice", on_delete=models.CASCADE, related_name="sku", null=True, blank=True)

    def save(self, *args, **kwargs):
        # save total_value and total_quantity
        quant = self.quotaion
        total_value = quant.total_value or 0
        total_quantity = quant.total_quantity or 0
        total_quantity += self.quantity
        total_value += self.price
        quant.total_value = total_value
        quant.total_quantity = total_quantity
        quant.save()
        # calculate number of containers
        pcs = self.stuff.pcs or 1
        containers = round((self.quantity / pcs), 2)
        self.number_of_containers = containers
        return super().save(*args, **kwargs)


class PurchaseOrderSKU(UUIDModel):
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="po_sku")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="po_sku")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="po_sku")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="po_sku")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="po_sku")
    quantity = models.IntegerField(default=0)
    number_of_containers = models.FloatField(null=True, blank=True, verbose_name="No. of containers")
    expected_price = models.FloatField(null=True, blank=True)
    expected_total_cost = models.FloatField(null=True, blank=True)
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="po_sku", null=True, blank=True)
    stuffing = models.ForeignKey(StuffMaster, on_delete=models.CASCADE, null=True, blank=True, related_name="po_sku")
    po = models.ForeignKey("PurchaseOrder", on_delete=models.CASCADE, related_name="po_sku")


class CostSheetSKU(UUIDModel):
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="co_sku")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="co_sku")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="co_sku")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="co_sku")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="co_sku")
    quantity = models.IntegerField(default=0)
    number_of_containers = models.FloatField(null=True, blank=True, verbose_name="No. of containers")
    # expected_price = models.FloatField(null=True, blank=True)
    # expected_total_cost = models.FloatField(null=True, blank=True)
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="co_sku", null=True, blank=True)
    stuffing = models.ForeignKey(StuffMaster, on_delete=models.CASCADE, null=True, blank=True, related_name="co_sku")
    co = models.ForeignKey("CostSheet", on_delete=models.CASCADE, related_name="co_sku")
    discount = models.FloatField(null=True)
    dcp = models.FloatField(null=True)
    sales_manager_commission = models.FloatField(null=True)
    vip = models.FloatField(null=True)
    advt = models.FloatField(null=True)
    net_fob = models.FloatField(null=True)
    profit = models.FloatField(null=True)

    # def save(self, *args, **kwargs):
    #     # save total_value and total_quantity
    #     quant = self.quotaion
    #     total_value = quant.total_value or 0
    #     total_quantity = quant.total_quantity or 0
    #     total_quantity += self.quantity
    #     total_value += self.price
    #     quant.total_value = total_value
    #     quant.total_quantity = total_quantity
    #     quant.save()
    #     # calculate number of containers
    #     pcs = self.stuff.pcs or 1
    #     containers = round((self.quantity / pcs), 2)
    #     self.number_of_containers = containers
    #     return super().save(*args, **kwargs)


class SKUSummary(UUIDModel):
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, related_name="sku_summary", null=True)
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="sku_summary")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="sku_summary")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="sku_summary")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="sku_summary")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="sku_summary")
    stuff = models.ForeignKey(Stuff, on_delete=models.CASCADE, related_name="sku_summary", null=True)
    quantity = models.IntegerField()
    number_of_containers = models.FloatField(null=True, verbose_name="No. of containers")
    price = models.FloatField()
    quotation_summary = models.ForeignKey("QuotationSummary", on_delete=models.CASCADE, related_name="sku_summary")


class AdvanceType(UUIDModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Advance(UUIDModel):
    advance_type = models.ForeignKey(AdvanceType, on_delete=models.CASCADE, related_name="advance")
    percentage = models.FloatField()
    remarks = models.TextField()
    quotaion = models.ForeignKey("Quotation", on_delete=models.CASCADE, related_name="advance")


def get_quotation_number():
    now = timezone.now()
    formatted = now.strftime("%Y-%m-%dT%HH-%MM-%SS")
    return "QT-"+formatted

def get_po_number():
    now = timezone.now()
    formatted = now.strftime("%Y-%m-%dT%HH-%MM-%SS")
    return "PO-"+formatted

def get_po_number():
    now = timezone.now()
    formatted = now.strftime("%Y-%m-%dT%HH-%MM-%SS")
    return "CS-"+formatted

class Quotation(UUIDModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="quotation")
    quote_number = models.CharField( null=True, blank=True, max_length=60)
    payment_basis = models.ForeignKey(PaymentBasis, on_delete=models.CASCADE, related_name="quotation", null=True)
    stuff_type = models.ForeignKey(StuffType, on_delete=models.CASCADE, related_name="quotation", null=True)
    currency = models.ForeignKey(Currency, on_delete=models.Case, related_name="quotation", null=True)
    exchange_rate = models.FloatField(null=True)
    total_value = models.FloatField(null=True, blank=True)
    total_quantity = models.FloatField(null=True, blank=True)
    pi = models.ForeignKey("PerformaInvoice", on_delete=models.CASCADE, null=True, blank=True, related_name="quotation")
    # history = HistoricalRecords()

    # def save(self, *args, **kwargs):
    #     # create a new entry with given data and update this in history
    #     print("\n----save is called---\n")
    #     super().save(*args, **kwargs)


class QuotationSummary(UUIDModel):
    quotation = models.ForeignKey("Quotation", on_delete=models.CASCADE, related_name="quotation_summary")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="quotation_summary", null=True)
    quote_number = models.CharField( null=True, blank=True, max_length=60)
    payment_basis = models.ForeignKey(PaymentBasis, on_delete=models.CASCADE, related_name="quotation_summary", null=True)
    stuff_type = models.ForeignKey(StuffType, on_delete=models.CASCADE, related_name="quotation_summary", null=True)
    currency = models.ForeignKey(Currency, on_delete=models.Case, related_name="quotation_summary", null=True)
    exchange_rate = models.FloatField(null=True)
    total_value = models.FloatField(null=True, blank=True)
    total_quantity = models.FloatField(null=True, blank=True)

@receiver(post_save, sender=Quotation)
def create_quotation_summary(sender, instance=None, created=False, **kwargs):
    # print("\n--------creating quotation summary------------\n")
    # flag = False
    # create_quotation_summary = getattr(instance, '_create_quotation_summary', True)
    # print("quotr bool ", create_quotation_summary)
    print("post save is called")

    if created:
        print("instance is created and updating its quotr number")
        # flag = True
        # create quotation number
        # QUOT-YYY-MM-DD-HH-MM-SS
        quote_number = get_quotation_number()
        instance.quote_number = quote_number
        instance._create_quotation_summary = False
        instance.save()

    # if create_quotation_summary:
    #     print("continue create summary")
        
    #     if instance:
    #         print("going for quotation creation")
    #         QuotationSummary.objects.create(
    #             quotation=instance,
    #             customer = instance.customer,
    #             quote_number=instance.quote_number,
    #             payment_basis=instance.payment_basis,
    #             stuff_type=instance.stuff_type,
    #             currency=instance.currency,
    #             exchange_rate=instance.exchange_rate,
    #             total_value=instance.total_value,
    #             total_quantity=instance.total_quantity
    #         )
    #         print(f"quotation summary created for {instance.pk}")


class PerformaInvoice(UUIDModel):
    sender_address = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    pi_number = models.CharField( null=True, blank=True, max_length=60)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    shipping_marks = models.ForeignKey(ShippingMarks, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    from_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="from_performa_invoice", null=True)
    to_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="to_performa_invoice", null=True)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    pi_remarks = models.ForeignKey(PIRemarks, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    packing = models.ForeignKey(PackingType, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    pi_date = models.DateField(null=True)


class PurchaseOrder(UUIDModel):
    receiving_address = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, related_name="purchase_order", null=True)
    po_number = models.CharField( default=get_po_number ,null=True, blank=True, max_length=60)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="purchase_order", null=True)
    shipping_marks = models.ForeignKey(ShippingMarks, on_delete=models.CASCADE, related_name="purchase_order", null=True)
    from_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="from_purchase_order", null=True)
    to_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="to_purchase_order", null=True)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="purchase_order", null=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, related_name="purchase_order", null=True)
    po_remarks = models.ForeignKey(PORemarks, on_delete=models.CASCADE, related_name="purchase_order", null=True)
    packing = models.ForeignKey(PackingType, on_delete=models.CASCADE, related_name="purchase_order", null=True)
    po_date = models.DateField(null=True)
    pi = models.ForeignKey(PerformaInvoice, on_delete=models.CASCADE, null=True, blank=True)



class AgentCommission(UUIDModel):
    name = models.CharField(max_length=30)
    commison_percent = models.FloatField(null=True, blank=True, default=0)
    commison_value = models.FloatField(null=True, blank=True, default=0)
    cost_sheet = models.ForeignKey("CostSheet", on_delete=models.CASCADE)


class Status(UUIDModel):
    name = models.CharField(max_length=15)

class InspectionInstruction(UUIDModel):
    name = models.CharField(max_length=15)

class PackagingInstruction(UUIDModel):
    name = models.CharField(max_length=15)

class SpecialInstruction(UUIDModel):
    name = models.CharField(max_length=15)

class LCTTInstruction(UUIDModel):
    name = models.CharField(max_length=15)

# class Status(UUIDModel):
#     name = models.CharField(max_length=15)


class CostSheet(UUIDModel):
    cs_number = models.CharField(default=get_po_number ,null=True, blank=True, max_length=60)
    co_date = models.DateField()
    company = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, related_name="cost_sheet")
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cost_sheet")
    buyer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cost_sheet")
    price_terms = models.ForeignKey(PriceTerms, on_delete=models.CASCADE, null=True, related_name="cost_sheet")
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, related_name="cost_sheet")
    discharge_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="discharge_cost_sheet")
    final_destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="final_cost_sheet")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="cost_sheet")
    sales_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales_manager_cost_sheet")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cost_sheet")
    freight_cost = models.FloatField(null=True)
    insurance_cost = models.FloatField(null=True)
    dcp_cost = models.FloatField(null=True)
    advt_cost_percent = models.FloatField(null=True)
    inspection_instruction = models.ForeignKey(InspectionInstruction, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    packaging_instruction = models.ForeignKey(PackagingInstruction, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    special_instruction = models.ForeignKey(SpecialInstruction, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    lc_tt_instruction = models.ForeignKey(LCTTInstruction, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    purchase_pay_term = models.ForeignKey(PurchasePayTerms, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    sales_contract_number = models.CharField(max_length=30)
    expected_deliver_date = models.DateField(null=True)


    

# @receiver(post_save, sender=SKU)
# def create_sku_summary(sender, instance=None, created=False, **kwargs):
#     print("\n--------creating sku summary------------\n")
#     if instance:
#         sku = instance
#         # get related quotation summary
#         # quotation_summary = sku.quotation.quotation_summary
#         # if quo
#         # create quotation summary
#         quotation_summary = sku.quotaion.quotation_summary.last()
#         # create SKU summary for all
#         SKUSummary.objects.create(
#             sku=sku,
#             tyre_size=sku.tyre_size,
#             pr = sku.pr,
#             tyre_set = sku.tyre_set,
#             brand = sku.brand,
#             pattern = sku.pattern,
#             stuff = sku.stuff,
#             quantity = sku.quantity,
#             number_of_containers = sku.number_of_containers,
#             price = sku.price,
#             quotation_summary = quotation_summary,
#         )
        
