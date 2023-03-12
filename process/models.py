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
from .basemodel import *
from .utils import *

# Create your models here.
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
    ci = models.ForeignKey("CustomerInvoice", on_delete=models.CASCADE, related_name="sku", null=True, blank=True)
    pl = models.ForeignKey("PackagingList", on_delete=models.CASCADE, related_name="sku", null=True, blank=True)

    def save(self, *args, **kwargs):
        print("re saving ...")
        # save total_value and total_quantity
        quant = self.quotaion
        print(quant.total_value)
        total_value = quant.total_value or 0
        total_quantity = quant.total_quantity or 0
        total_quantity += self.quantity
        total_value += (self.price * self.quantity)
        quant.total_value = total_value
        quant.total_quantity = total_quantity
        quant.save()
        # calculate number of containers
        # get stuffing
        stuffing = StuffMaster.objects.get(tyre_size=self.tyre_size, pr=self.pr, brand=self.brand, pattern=self.pattern, container_type=self.container_type)
        if stuffing:
            pcs = stuffing.stuff
            containers = round((self.quantity / pcs), 2)
            self.number_of_containers = containers
            self.stuffing = stuffing
        return super().save(*args, **kwargs)


class PurchaseOrderSKU(UUIDModel):
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="po_sku")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="po_sku")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="po_sku")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="po_sku")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="po_sku")
    quantity = models.IntegerField(default=0)
    number_of_containers = models.FloatField(null=True, blank=True, verbose_name="No. of containers")
    price = models.FloatField(default=0)
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="po_sku", null=True, blank=True)
    expected_price = models.FloatField(null=True, blank=True)
    expected_total_cost = models.FloatField(null=True, blank=True)
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
    discount_percentage = models.FloatField(null=True)
    discount_amount = models.FloatField(null=True)
    sales_manager_commission = models.FloatField(null=True)
    vip = models.FloatField(null=True)
    advt = models.FloatField(null=True)
    agents_commison = models.FloatField(null=True)
    sales_price = models.FloatField(null=True)
    purchase_price = models.FloatField(null=True)
    net_fob = models.FloatField(null=True)
    profit = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        print("saving skus .")
        # save total_value and total_quantity
        cost_sheet = self.co
        cost_price = self.purchase_price
        sales_price = self.sales_price
        # calculate individuka stuff
        self.discount_percentage = cost_sheet.total_discount_percentage
        self.discount_amount = (cost_sheet.total_discount_percentage * sales_price)/100
        self.sales_manager_commission = (cost_sheet.sales_manager_commission * cost_price)/100
        self.vip = (cost_sheet.total_vip_percentage * sales_price)/100
        self.advt = (cost_sheet.total_advt_percentage * sales_price)/100


        # agents commison
        ag_com = 0
        agent_comms = cost_sheet.agent_comms.all()
        for com in agent_comms:
            temp = (com.commison_percent * sales_price)/100
            ag_com += temp
        
        self.agents_commison = ag_com
        total_purchase_cost = cost_price + self.discount_amount + self.sales_manager_commission + self.vip + self.advt + ag_com
        profit = sales_price - total_purchase_cost
        self.net_fob = total_purchase_cost
        self.profit = profit

        # net profit and fob for costsheet
        co_fob = cost_sheet.net_fob
        co_profit = cost_sheet.net_profit
        co_fob += total_purchase_cost
        co_profit += profit
        cost_sheet.net_fob = co_fob
        cost_sheet.net_profit = co_profit
        cost_sheet.save()

        return super().save(*args, **kwargs)


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




#  Actual Process Starts Here

class Quotation(UUIDModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="quotation")
    quote_number = models.CharField( null=True, blank=True, max_length=60)
    # payment_basis = models.ForeignKey(PaymentBasis, on_delete=models.CASCADE, related_name="quotation", null=True)
    # supplier_address = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    payment_term = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, related_name="quotation", null=True)
    price_term = models.ForeignKey(PriceTerms, on_delete=models.CASCADE, related_name="quotation", null=True)
    # stuff_type = models.ForeignKey(StuffType, on_delete=models.CASCADE, related_name="quotation", null=True)
    currency = models.ForeignKey(Currency, on_delete=models.Case, related_name="quotation", null=True)
    exchange_rate = models.FloatField(null=True)
    total_value = models.FloatField(null=True, blank=True)
    total_quantity = models.FloatField(null=True, blank=True)
    pi = models.ForeignKey("PerformaInvoice", on_delete=models.CASCADE, null=True, blank=True, related_name="quotation")

    # def save(self, *args, **kwargs):
    #     # save total_value and total_quantity
    #     self.total_value = 0
    #     self.total_quantity = 0
    #     return super().save(*args, **kwargs)


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
    from_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="from_performa_invoice", null=True, verbose_name="Port of Loading")
    to_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="to_performa_invoice", null=True, verbose_name="Port of Discharge")
    destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="destination_performa_invoice", null=True, verbose_name="Destination")
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    pi_remarks = models.ForeignKey(PIRemarks, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    packing = models.ForeignKey(PackingType, on_delete=models.CASCADE, related_name="performa_invoice", null=True)
    pi_date = models.DateField(null=True)
    cost_sheet = models.ForeignKey("CostSheet", on_delete=models.CASCADE, null=True, blank=True, related_name="performa_invoice")


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
    cost_sheet = models.ForeignKey("CostSheet", on_delete=models.CASCADE, related_name="agent_comms")



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
    freight_purchase = models.FloatField(null=True, default=0)
    insurance_purchase = models.FloatField(null=True, default=0)
    freight_sale = models.FloatField(null=True, default=0)
    insurance_sale = models.FloatField(null=True, default=0)
    total_discount_percentage = models.FloatField(null=True, default=0)
    total_advt_percentage = models.FloatField(null=True, default=0)
    total_vip_percentage = models.FloatField(null=True, default=0)
    inspection_instruction = models.ForeignKey(InspectionInstruction, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    packaging_instruction = models.ForeignKey(PackagingInstruction, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    special_instruction = models.ForeignKey(SpecialInstruction, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    lc_tt_instruction = models.ForeignKey(LCTTInstruction, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    purchase_pay_term = models.ForeignKey(PurchasePayTerms, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="cost_sheet", null=True)
    sales_manager_commission = models.FloatField(null=True, default=0)
    sales_contract_number = models.CharField(max_length=30)
    expected_deliver_date = models.DateField(null=True)
    net_fob = models.FloatField(default=0)
    net_profit = models.FloatField(default=0)

        


class SupplierPerformaInvoiceSKU(UUIDModel):
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="spi_sku")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="spi_sku")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="spi_sku")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="spi_sku")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="spi_sku")
    quantity = models.IntegerField(default=0)
    number_of_containers = models.FloatField(null=True, blank=True, verbose_name="No. of containers")
    price = models.FloatField(default=0)
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, related_name="spi_sku", null=True, blank=True)
    stuffing = models.ForeignKey(StuffMaster, on_delete=models.CASCADE, null=True, blank=True, related_name="spi_sku")
    spi = models.ForeignKey("SupplierPerformaInvoice", on_delete=models.CASCADE, related_name="spi_sku")


class SupplierPerformaInvoice(UUIDModel):
    receiving_address = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, related_name="spi", null=True)
    spi_number = models.CharField( default=get_spi_number ,null=True, blank=True, max_length=60)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="spi", null=True)
    shipping_marks = models.ForeignKey(ShippingMarks, on_delete=models.CASCADE, related_name="spi", null=True)
    from_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="spi_from", null=True)
    to_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="spi_to", null=True)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="spi", null=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, related_name="spi", null=True)
    spo_remarks = models.ForeignKey(PORemarks, on_delete=models.CASCADE, related_name="spi", null=True)
    packing = models.ForeignKey(PackingType, on_delete=models.CASCADE, related_name="spi", null=True)
    spi_date = models.DateField(null=True)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True, related_name="spi")
    cost_sheet = models.ForeignKey(CostSheet, on_delete=models.CASCADE, null=True, blank=True, related_name="spi")


class BL(UUIDModel):
    bl_number = models.CharField(max_length=20, null=True, blank=True)
    bl_document = models.FileField(null=True, blank=True)
    shipping_line = models.TextField(null=True)
    shipped_on_date = models.DateField(null=True)
    eta = models.DateField(null=True, blank=True)
    shipment_mode = models.ForeignKey(ShipmentMode, on_delete=models.CASCADE, related_name="bl", null=True)
    vessel_flight_number = models.CharField(max_length=50, null=True)
    supplier_insuarance_number = models.CharField(max_length=20,null=True, blank=True)
    supplier_insuarance_document = models.FileField(null=True, blank=True)
    supplier_invoice_number = models.CharField(max_length=20,null=True, blank=True)
    supplier_invoice_document = models.FileField(null=True, blank=True)
    insuarance_invoice_number = models.CharField(max_length=20,null=True, blank=True)
    insuarance_invoice_document = models.FileField(null=True, blank=True)
    freight_invoice_number = models.CharField(max_length=20, null=True, blank=True)
    freight_invoice_document = models.FileField(null=True, blank=True)
    cost_sheet = models.ForeignKey(CostSheet, on_delete=models.CASCADE, null=True, blank=True, related_name="bl")
    total_supplier_invoice_amount = models.FloatField(default=0)


class ContainerBox(UUIDModel):
    box_bl = models.ForeignKey(BL, on_delete=models.CASCADE, null=True, blank=True, related_name="container_box")
    customer_invoice = models.ForeignKey("CustomerInvoice", on_delete=models.CASCADE, null=True, blank=True, related_name="container_box")
    customer_packging_list = models.ForeignKey("PackagingList", on_delete=models.CASCADE, null=True, blank=True, related_name="container_box")
    total_container_weight = models.FloatField(default=0, verbose_name="Total Weight (KGS)")
    measurement = models.FloatField(default=0, verbose_name="Measurement (CBM)")


class ContainerSKU(UUIDModel):
    tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="cm_sku")
    pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="cm_sku")
    tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="cm_sku")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="cm_sku")
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="cm_sku")
    quantity = models.IntegerField(default=0)
    box = models.ForeignKey(ContainerBox, on_delete=models.CASCADE, null=True, blank=True, related_name="cm_sku")
    supplier_price = models.FloatField(default=0)
    customer_price = models.FloatField(default=0)
    supplier_amount = models.FloatField(default=0)
    customer_amount = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # save total_value and total_quantity
        bl = self.box.box_bl
        ci = self.box.customer_invoice

        if not ci:
        
            total_supplier_invoice_amount = bl.total_supplier_invoice_amount
            self.supplier_amount = self.supplier_price * self.quantity
            

            total_supplier_invoice_amount += self.supplier_amount
            bl.total_supplier_invoice_amount = total_supplier_invoice_amount
            bl.save()

        if ci:
            self.customer_amount = self.customer_price * self.quantity
            total_customer_invoice_amount = ci.total_customer_invoice_amount
            total_customer_invoice_amount += self.customer_amount
            ci.total_customer_invoice_amount = total_customer_invoice_amount
            ci.save()
        return super().save(*args, **kwargs)
    


# class CustomerContainerSKU(UUIDModel):
#     tyre_size = models.ForeignKey(TyreSize, on_delete=models.CASCADE, related_name="ccm_sku")
#     pr = models.ForeignKey(PR, on_delete=models.CASCADE, related_name="ccm_sku")
#     tyre_set = models.ForeignKey(TyreSet, on_delete=models.CASCADE, related_name="ccm_sku")
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="ccm_sku")
#     pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name="ccm_sku")
#     quantity = models.IntegerField(default=0)
#     box = models.ForeignKey(ContainerBox, on_delete=models.CASCADE, null=True, blank=True, related_name="ccm_sku")
    


class CustomerInvoice(UUIDModel):
    bl = models.ForeignKey(BL, on_delete=models.CASCADE)
    sender_address = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    consignee = models.TextField(null=True)
    invoice_number = models.CharField( null=True, blank=True, max_length=60)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    shipping_marks = models.ForeignKey(ShippingMarks, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    from_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="from_customer_invoice", null=True)
    to_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="to_customer_invoice", null=True)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    delivery_terms = models.ForeignKey(DeliveryTerm, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    invoice_remarks = models.ForeignKey(PIRemarks, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    packing = models.ForeignKey(PackingType, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    shipment_mode = models.ForeignKey(ShipmentMode, on_delete=models.CASCADE, related_name="customer_invoice", null=True)
    receipt_place = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="rec_customer_invoice", null=True)
    vessel_flight_number = models.CharField(max_length=50, null=True)
    port_of_discharge = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="discharge_customer_invoice", null=True)
    final_destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="destination_customer_invoice", null=True)
    country_final_destination = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="dest_customer_invoice", null=True)
    total_customer_invoice_amount = models.FloatField(default=0)
    invoice_date = models.DateField(null=True)


class PackagingList(UUIDModel):
    bl = models.ForeignKey(BL, on_delete=models.CASCADE)
    sender_address = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, related_name="packaging_list", null=True)
    consignee = models.TextField(null=True)
    pl_number = models.CharField( null=True, blank=True, max_length=60)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="packaging_list", null=True)
    shipping_marks = models.ForeignKey(ShippingMarks, on_delete=models.CASCADE, related_name="packaging_list", null=True)
    from_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="from_packaging_list", null=True)
    to_port = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="to_packaging_list", null=True)
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="packaging_list", null=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, related_name="packaging_list", null=True)
    delivery_terms = models.ForeignKey(DeliveryTerm, on_delete=models.CASCADE, related_name="packaging_list", null=True)
    invoice_remarks = models.ForeignKey(PIRemarks, on_delete=models.CASCADE, related_name="packaging_list", null=True)
    packing = models.ForeignKey(PackingType, on_delete=models.CASCADE, related_name="packaging_list", null=True)
    shipment_mode = models.ForeignKey(ShipmentMode, on_delete=models.CASCADE, related_name="packaging_list")
    receipt_place = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="rec_packaging_list")
    vessel_flight_number = models.CharField(max_length=50)
    port_of_discharge = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="discharge_packaging_list")
    final_destination = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="destination_packaging_list")
    country_final_destination = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="dest_packaging_list", null=True)

    invoice_date = models.DateField(null=True)


# class ContainerConfiguration(UUIDModel):




