from uuid import uuid4
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from django.http import HttpResponseRedirect

from transaction.models import Transaction
from .models import *
from simple_history.admin import SimpleHistoryAdmin
from .forms import CustomFooForm
from django.template.loader import get_template
# from fieldsets_with_inlines import FieldsetsInlineMixin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from django.forms.models import ModelForm

# Register your models here.

admin.site.register(Currency)
admin.site.register(AdvanceType)
admin.site.register(PackingType)
admin.site.register(SenderAddress)
admin.site.register(PaymentTerms)
admin.site.register(ShippingMarks)
admin.site.register(PIRemarks)
admin.site.register(PORemarks)
admin.site.register(Location)
admin.site.register(AdvanceTT)
admin.site.register(BalanceTerm)
admin.site.register(DaysETA)
admin.site.register(Status)
admin.site.register(InspectionInstruction)
admin.site.register(PackagingInstruction)
admin.site.register(SpecialInstruction)
admin.site.register(LCTTInstruction)
admin.site.register(PriceTerms)
admin.site.register(PurchasePayTerms)
admin.site.register(DeliveryTerm)
admin.site.register(ShipmentMode)

class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        """ Should returns True if data differs from initial. 
        By always returning true even unchanged inlines will get validated and saved."""
        return True

def get_pi_number():
    now = timezone.now()
    formatted = now.strftime("%Y-%m-%dT%HH-%MM-%SS")
    return "PI-"+formatted


class SKUInline(admin.TabularInline):
    fields = (
        "tyre_size",
        "pr",
        "tyre_set",
        "brand",
        "pattern",
        "quantity",
        "container_type",
        # "stuffing",
        # "number_of_containers",
        "price",
    )
    readonly_fields = ("stuffing", "number_of_containers")
    extra = 0
    model = SKU
    form = AlwaysChangedModelForm


class PerformaInvoiceSKUInline(admin.TabularInline):
    fields = (
        "tyre_size",
        "pr",
        "tyre_set",
        "brand",
        "pattern",
        "quantity",
        "container_type",
        "stuffing",
        "number_of_containers",
        "price",
    )
    exclude = ("quotaion",)
    extra = 0
    model = SKU


class PurchaseOrderSKUInline(admin.TabularInline):
    fields = (
        "tyre_size",
        "pr",
        "tyre_set",
        "brand",
        "pattern",
        "quantity",
        "container_type",
        "stuffing",
        "number_of_containers",
        "price",
        "expected_price",
    )
    exclude = ("pi",)
    extra = 0
    model = PurchaseOrderSKU




class CostSheetSKUline(admin.TabularInline):
    readonly_fields = (
        "tyre_size",
        "pr",
        "tyre_set",
        "brand",
        "pattern",
        "quantity",
        "container_type",
        "stuffing",
        "sales_price",
        "purchase_price",
        "number_of_containers",
        "discount_percentage",
        "discount_amount",
        "sales_manager_commission",
        "vip",
        "advt",
        "agents_commison",
        "net_fob",
        "profit",

    )
    extra = 0
    model = CostSheetSKU
    form = AlwaysChangedModelForm


class AgentCommissionInline(admin.TabularInline):
    fields = (
        "name",
        "commison_percent",
        "commison_value",
    )
    extra = 0
    model = AgentCommission


class SKUSummaryInline(admin.TabularInline):
    fields = (
        "tyre_size",
        "pr",
        "tyre_set",
        "brand",
        "pattern",
        "quantity",
        "stuffing",
        "number_of_containers",
        "containers",
        "price",
    )
    extra = 0
    model = SKUSummary



class AdvanceInline(admin.TabularInline):
    fields = ("advance_type", "percentage", "remarks")
    extra = 0
    model = Advance


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "total_quantity",
        "total_value",
         "create_PI",
    )
    
    fieldsets = (
        (None, {
                    'fields': ('customer', "quote_number", "payment_term", "currency", "exchange_rate", ),
                }
        ),
        ("Total", {
                    'fields': ('total_value', "total_quantity",),
                }
        ),
    )
    inlines = [SKUInline]
    # fields = ('customer', "quote_number", "payment_basis", "currency", "exchange_rate", "sku_inline", 'total_value', "total_quantity")
    readonly_fields = ("total_quantity", "total_value", "pi", "quote_number",)
    form = AlwaysChangedModelForm
    
    # change_form_template = 'admin/process/quotation/change_quotation_form.html'

    # def sku_inline(self, *args, **kwargs):
    #     context = getattr(self.response, 'context_data', None) or {}
    #     inline = context['inline_admin_formset'] = context['inline_admin_formsets'].pop(0)
    #     return get_template(inline.opts.template).render(context, self.request)
    
    # def render_change_form(self, request, *args, **kwargs):
    #     self.request = request
    #     self.response = super().render_change_form(request, *args, **kwargs)
    #     return self.response


    def customer_name(self, obj):
        return obj.customer.company_name
    
    def create_PI(self, obj):
        if not obj.pi:
            return format_html(
                    '<a class="button" href="{}">Create PI</a>&nbsp;',
                    reverse('admin:pi-create', args=(obj.pk, )),
                )
        return "PI Created"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<quotation_id>/create-pi/",
            self.admin_site.admin_view(self.create_pi),
            name='pi-create'
            ),
            
        ]
        return custom_urls + urls
    
    def create_pi(self, request, quotation_id, *args, **kwargs):
        # create transit for this nomination using default values
        quotation = self.get_object(request, quotation_id)
        pi = PerformaInvoice.objects.create(
            pi_date = timezone.now().date(),
            pi_number = get_pi_number(),
            customer = quotation.customer
        )
        quotation.pi = pi
        quotation._create_quotation_summary = False
        quotation.save()
        # for each sku in quotation add this pi there as well
        skus = quotation.sku.all()
        for sku in skus:
            sku.pi = pi
            sku.save()
        return HttpResponseRedirect(reverse('admin:process_performainvoice_change', args=(pi.id,)))
    


@admin.register(QuotationSummary)
class QuotationSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "stuff_type",
        "total_quantity",
        "total_value",
    )
    readonly_fields = ("total_quantity", "total_value")
    inlines = (SKUSummaryInline, )

    def customer_name(self, obj):
        return obj.customer.company_name
    
    def has_change_permission(self, request, obj=None):
        return False


class QuotationInline(admin.StackedInline):
    readonly_fields = (
        "customer",
        "quote_number",
        "payment_term",
        "currency",
        "exchange_rate",
        "total_value",
        "total_quantity"
    )
    model = Quotation
    extra = 0



@admin.register(PerformaInvoice)
class PerformaInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "pi_number",
        "customer",
        "from_port",
        "to_port",
        "create_PO"

    )
    readonly_fields = ("customer", )
    inlines = (QuotationInline, PerformaInvoiceSKUInline)

    def create_PO(self, obj):
        # create PO related to this PI
        
        return format_html(
                '<a class="button" href="{}">Create PO</a>&nbsp;',
                reverse('admin:po-create', args=(obj.pk, )),
            )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<pi_id>/create-po/",
            self.admin_site.admin_view(self.create_po),
            name='po-create'
            ),
            
        ]
        return custom_urls + urls
    
    def create_po(self, request, pi_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, pi_id)
        po = PurchaseOrder.objects.create(
                po_date = timezone.now().date(),
                from_port = obj.from_port,
                to_port = obj.to_port,
                country_of_origin = obj.country_of_origin,
                packing = obj.packing,
                pi = obj,
                receiving_address = obj.sender_address
            )
        skus = obj.sku.all()
        for sku in skus:
            # for each sku create PO according to their seller (size+pattern+pr)
            PurchaseOrderSKU.objects.create(
                tyre_size = sku.tyre_size,
                tyre_set = sku.tyre_set,
                brand = sku.brand,
                pattern = sku.pattern,
                stuffing = sku.stuffing,
                quantity = sku.quantity,
                container_type = sku.container_type,
                price = sku.price,
                pr = sku.pr,
                number_of_containers = sku.number_of_containers,
                po = po
            )
        return HttpResponseRedirect(reverse('admin:process_purchaseorder_change', args=(po.id,)))
    
    
    

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        "po_number",
        "supplier",
        "from_port",
        "to_port",
        "create_SPI"

    )
    readonly_fields = ("receiving_address", "po_number", "from_port", "to_port", "country_of_origin", "packing", "pi")
    inlines = (PurchaseOrderSKUInline, )

    def create_SPI(self, obj):
        # create SPI related to this PO
        
        return format_html(
                '<a class="button" href="{}">Create SPI</a>&nbsp;',
                reverse('admin:spi-create', args=(obj.pk, )),
            )
        # return "<p> PO Done</p>"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<po_id>/create-spi/",
            self.admin_site.admin_view(self.create_spi),
            name='spi-create'
            ),
            
        ]
        return custom_urls + urls
    
    def create_spi(self, request, po_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, po_id)
        spi = SupplierPerformaInvoice.objects.create(
                spi_date = timezone.now().date(),
                from_port = obj.from_port,
                to_port = obj.to_port,
                country_of_origin = obj.country_of_origin,
                packing = obj.packing,
                po = obj,
                receiving_address = obj.receiving_address,
                supplier = obj.supplier,
                shipping_marks = obj.shipping_marks,
            )
        skus = obj.po_sku.all()
        for sku in skus:
            # for each sku create PO according to their seller (size+pattern+pr)
            SupplierPerformaInvoiceSKU.objects.create(
                tyre_size = sku.tyre_size,
                tyre_set = sku.tyre_set,
                brand = sku.brand,
                pattern = sku.pattern,
                stuffing = sku.stuffing,
                quantity = sku.quantity,
                container_type = sku.container_type,
                price = sku.price,
                pr = sku.pr,
                number_of_containers = sku.number_of_containers,
                spi = spi
            )
        return HttpResponseRedirect(reverse('admin:process_supplierperformainvoice_change', args=(spi.id,)))
    

class SupplierPerformaInvoiceSKUInline(admin.TabularInline):
    fields = (
        "tyre_size",
        "pr",
        "tyre_set",
        "brand",
        "pattern",
        "quantity",
        "container_type",
        "stuffing",
        "number_of_containers",
        "price",
    )
    extra = 0
    model = SupplierPerformaInvoiceSKU

    
@admin.register(SupplierPerformaInvoice)
class SupplierPerformaInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "spi_number",
        "supplier",
        "from_port",
        "to_port",
        "create_cost_sheet"

    )
    readonly_fields = ("spi_number", "from_port", "to_port", "country_of_origin", "packing", "po")
    inlines = (SupplierPerformaInvoiceSKUInline, ) 

    def create_cost_sheet(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Create Cost Sheet</a>&nbsp;',
                reverse('admin:cs-create', args=(obj.pk, )),
            )
        # return "<p> PO Done</p>"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<spi_id>/create-cs/",
            self.admin_site.admin_view(self.create_cs),
            name='cs-create'
            ),
            
        ]
        return custom_urls + urls
    
    def create_cs(self, request, spi_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, spi_id)
        cs = CostSheet.objects.create(
                co_date = timezone.now().date(),
                discharge_port = obj.from_port,
                final_destination = obj.to_port,
                buyer_name = obj.po.pi.customer,
                company = obj.po.pi.sender_address,
                payment_terms = obj.payment_terms,
                status = Status.objects.get(name="In Progress"),
                sales_manager = request.user,
                raised_by = request.user,
                region = obj.country_of_origin.region

            )
        obj.cost_sheet = cs
        obj.save()
        # pi
        pi = obj.po.pi
        pi.cost_sheet = cs
        pi.save()
        skus = obj.spi_sku.all()
        for sku in skus:
            # for each sku create PO according to their seller (size+pattern+pr)
            # get pi sku price
            pi_sku = pi.sku.get(
                        tyre_size = sku.tyre_size,
                        tyre_set = sku.tyre_set,
                        brand = sku.brand,
                        pattern = sku.pattern,
                        stuffing = sku.stuffing,
                        quantity = sku.quantity,
                        container_type = sku.container_type,
                        pr = sku.pr
                    )
            CostSheetSKU.objects.create(
                tyre_size = sku.tyre_size,
                tyre_set = sku.tyre_set,
                brand = sku.brand,
                pattern = sku.pattern,
                stuffing = sku.stuffing,
                quantity = sku.quantity,
                container_type = sku.container_type,
                pr = sku.pr,
                number_of_containers = sku.number_of_containers,
                purchase_price = sku.price,
                sales_price = pi_sku.price,
                co = cs
            )
        return HttpResponseRedirect(reverse('admin:process_costsheet_change', args=(cs.id,)))
    


# CS has PI and SPI, it needs both inlines
class PISKUInline(NestedTabularInline):
    model = SKU
    fk_name = "pi"
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
      return False

class PIInline(NestedStackedInline):
    readonly_fields = (
        "sender_address",
        "pi_number",
        "customer",
        "shipping_marks",
        "from_port",
        "to_port",
        "country_of_origin",
        "payment_terms",
        "pi_remarks",
        "packing",
        "pi_date",
    )
    fk_name = "cost_sheet"
    inlines = [PISKUInline]
    model = PerformaInvoice
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
      return False


class SPISKUInline(NestedTabularInline):
    model = SupplierPerformaInvoiceSKU
    fk_name = "spi"
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
      return False

class SPIInline(NestedStackedInline):
    fk_name = "cost_sheet"
    inlines = [SPISKUInline]
    model = SupplierPerformaInvoice
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
      return False


class ContainerSKUInline(NestedTabularInline):
    readonly_fields = ("supplier_amount", "customer_price", "customer_amount")
    model = ContainerSKU
    fk_name = "box"
    extra = 1

class CustomerContainerSKUInline(NestedTabularInline):
    readonly_fields = ("supplier_amount", "customer_amount")
    model = ContainerSKU
    fk_name = "box"
    extra = 1

class ContainersManagementInline(NestedStackedInline):
    readonly_fields = ("customer_invoice", "customer_packging_list")
    model = ContainerBox
    inlines = [ContainerSKUInline]
    fk_name = "box_bl"
    extra = 1


class CustomerContainersManagementInline(NestedStackedInline):
    model = ContainerBox
    inlines = [CustomerContainerSKUInline]
    fk_name = "customer_invoice"
    extra = 1


class BLInline(NestedStackedInline):
    fk_name = "cost_sheet"
    inlines = [ContainersManagementInline]
    model = BL
    extra = 0


@admin.register(CostSheet)
class CostSheetAdmin(NestedModelAdmin):
    list_display = (
        "cs_number",
        "supplier_advance_pay",
        "customer_advance_pay",
        "create_bl",
        "view_bl",

    )
    fieldsets = (
        (None, {
                    'fields': ('cs_number', "company", "raised_by", "buyer_name", "region", "price_terms", "payment_terms","discharge_port", "final_destination", "status", "sales_manager", "purchase_pay_term", "expected_deliver_date"),
                }
        ),
        ("Purchase", {
                    'fields': ('freight_purchase', "insurance_purchase", "sales_manager_commission"),
                }
        ),
        ("Sales", {
                    'fields': ('freight_sale', "insurance_sale", "total_discount_percentage", "total_advt_percentage", "total_vip_percentage", "sales_contract_number", ),
                }
        ),
        ("Instructions", {
                    'fields': ('inspection_instruction', "packaging_instruction", "special_instruction", "lc_tt_instruction",),
                }
        ),
    )
    inlines = (PIInline , SPIInline ,AgentCommissionInline, CostSheetSKUline, BLInline )

    def supplier_advance_pay(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Supplier Advance</a>&nbsp;',
                reverse('admin:supplier-advance-create', args=(obj.pk, )),
            )

    def customer_advance_pay(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Customer Advance</a>&nbsp;',
                reverse('admin:customer-advance-create', args=(obj.pk, )),
            )
        # return "<p> PO Done</p>"
    def create_bl(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Create BL</a>&nbsp;',
                reverse('admin:bl-create', args=(obj.pk, )),
            )
        # return "<p> PO Done</p>"
    
    
    def view_bl(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Views BLs</a>&nbsp;',
                reverse('admin:process_bl_changelist')+'?cost_sheet='+str(obj.id),
            )
        # return "<p> PO Done</p>"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<cs_id>/create-bl/",
            self.admin_site.admin_view(self.create_BL),
            name='bl-create'
            ),
            path("<cs_id>/supplier-advance-create/",
            self.admin_site.admin_view(self.create_supplier_advance),
            name='supplier-advance-create'
            ),
            path("<cs_id>/customer-advance-create/",
            self.admin_site.admin_view(self.create_customer_advance),
            name='customer-advance-create'
            ),
            
        ]
        return custom_urls + urls
    
    def create_BL(self, request, cs_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, cs_id)
        bl = BL.objects.create(
                cost_sheet = obj

            )
        return HttpResponseRedirect(reverse('admin:process_bl_change', args=(bl.id,)))

    def create_supplier_advance(self, request, cs_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, cs_id)
        supplier_advance = Transaction.objects.create(
                cost_sheet = obj

            )
        return HttpResponseRedirect(reverse('admin:transaction_transaction_change', args=(supplier_advance.id,)))

    def create_customer_advance(self, request, cs_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, cs_id)
        customer_advance = Transaction.objects.create(
                cost_sheet = obj

            )
        return HttpResponseRedirect(reverse('admin:transaction_transaction_change', args=(customer_advance.id,)))
    


@admin.register(BL)
class BLAdmin(NestedModelAdmin):
    list_display = (
        "bl_number",
        "cost_sheet",
        "create_ci",
        "create_pl",
        "supplier_balance_pay",
        "customer_balance_pay",

    )
    inlines = (ContainersManagementInline, )

    def create_ci(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Create Customer Invoice</a>&nbsp;',
                reverse('admin:ci-create', args=(obj.pk, )),
            )
        # return "<p> PO Done</p>"
    
    
    def create_pl(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Create Packaging List</a>&nbsp;',
                reverse('admin:pl-create', args=(obj.pk, )),
            )
        # return "<p> PO Done</p>"
    
    def supplier_balance_pay(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Supplier Balance Pay</a>&nbsp;',
                reverse('admin:supplier-balance-create', args=(obj.pk, )),
            )

    def customer_balance_pay(self, obj):
        # create CS related to this SPI
        
        return format_html(
                '<a class="button" href="{}">Customer Balance Pay</a>&nbsp;',
                reverse('admin:customer-balance-create', args=(obj.pk, )),
            )
        # return "<p> PO Done</p>"
    
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<bl_id>/create-ci/",
            self.admin_site.admin_view(self.create_CI),
            name='ci-create'
            ),
            path("<bl_id>/create-pl/",
            self.admin_site.admin_view(self.create_PL),
            name='pl-create'
            ),
            path("<bl_id>/supplier-balance-create/",
            self.admin_site.admin_view(self.create_supplier_balance),
            name='supplier-balance-create'
            ),
            path("<bl_id>/customer-balance-create/",
            self.admin_site.admin_view(self.create_customer_balance),
            name='customer-balance-create'
            ),
            
        ]
        return custom_urls + urls
    
    def create_CI(self, request, bl_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, bl_id)
        print(obj.cost_sheet)
        pi = obj.cost_sheet.performa_invoice.last()
        ci = CustomerInvoice.objects.create(
                bl = obj,
                customer = pi.customer,
                shipping_marks = pi.shipping_marks,
                from_port = pi.from_port,
                to_port = pi.to_port,
                country_of_origin = pi.country_of_origin,
                payment_terms = pi.payment_terms,
                packing = pi.packing,
                shipment_mode = obj.shipment_mode,
                vessel_flight_number = obj.vessel_flight_number,
                port_of_discharge = obj.cost_sheet.discharge_port,
                final_destination = obj.cost_sheet.final_destination,
                # country_final_destination = obj.cost_sheet.country_final_destination
            )
        # create ccm_sku
        boxes = obj.container_box.all()
        for box in boxes:
            box.customer_invoice = ci
            box.save()
        # attach this to 
        return HttpResponseRedirect(reverse('admin:process_customerinvoice_change', args=(ci.id,)))
    
    def create_PL(self, request, bl_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, bl_id)
        pl = PackagingList.objects.create(
                bl = obj,
            )
        return HttpResponseRedirect(reverse('admin:process_packaginglist_change', args=(pl.id,)))
    
    def create_supplier_balance(self, request, cs_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, cs_id)
        supplier_balance = Transaction.objects.create(
                cost_sheet = obj.cost_sheet,
                bl = obj

            )
        return HttpResponseRedirect(reverse('admin:transaction_transaction_change', args=(supplier_balance.id,)))

    def create_customer_balance(self, request, cs_id, *args, **kwargs):
        # create transit for this nomination using default values
        obj = self.get_object(request, cs_id)
        customer_balance = Transaction.objects.create(
                cost_sheet = obj.cost_sheet,
                bl = obj

            )
        return HttpResponseRedirect(reverse('admin:transaction_transaction_change', args=(customer_balance.id,)))
    


@admin.register(PackagingList)
class PackagingAdmin(admin.ModelAdmin):
    list_display = (
        "pl_number",
    )
    
    inlines = (SKUInline, )



@admin.register(CustomerInvoice)
class CustomerInvoiceAdmin(NestedModelAdmin):
    list_display = (
        "invoice_number",
        "bl",
        "cost_sheet",

    )
    inlines = (CustomerContainersManagementInline, )

    def cost_sheet(self, obj):
        return obj.bl.cost_sheet
