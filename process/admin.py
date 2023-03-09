from uuid import uuid4
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.urls import path
from django.http import HttpResponseRedirect
from .models import *
from simple_history.admin import SimpleHistoryAdmin
from .forms import CustomFooForm
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
        "stuffing",
        "number_of_containers",
        "price",
    )
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
        "expected_price",
    )
    extra = 0
    model = PurchaseOrderSKU


class CostSheetSKUline(admin.TabularInline):
    fields = (
        "tyre_size",
        "pr",
        "tyre_set",
        "brand",
        "pattern",
        "quantity",
        "container_type",
        "stuffing",
        # "number_of_containers",
        "discount",
        "dcp",
        "sales_manager_commission",
        "vip",
        "advt",
        "net_fob",
        "profit",
    )
    extra = 0
    model = CostSheetSKU


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
        "stuff_type",
        "total_quantity",
        "total_value",
         "create_PI",
    )
    readonly_fields = ("total_quantity", "total_value")
    inlines = (SKUInline, )

    def customer_name(self, obj):
        return obj.customer.company_name
    
    def create_PI(self, obj):
        if not obj.pi:
            return format_html(
                    '<a class="button" href="{}">Create PI</a>&nbsp;',
                    reverse('admin:pi-create', args=(obj.pk, )),
                )
        return "<p> PI Done</p>"
    
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
            pi_number = get_pi_number()
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
    fields = (
        "customer",
        "quote_number",
        "payment_basis",
        "stuff_type",
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
    inlines = (QuotationInline, SKUInline)

    def create_PO(self, obj):
        # create PO related to this PI
        
        return format_html(
                '<a class="button" href="{}">Create PO</a>&nbsp;',
                reverse('admin:po-create', args=(obj.pk, )),
            )
        # return "<p> PO Done</p>"
    
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
        obj = PerformaInvoice.objects.get(id=pi_id)
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
                stuff = sku.stuff,
                quantity = sku.quantity,
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
        # "total_value"

    )
    inlines = (PurchaseOrderSKUInline, )


@admin.register(CostSheet)
class CostSheetAdmin(admin.ModelAdmin):
    list_display = (
        "cs_number",
        # "total_value"

    )
    inlines = (CostSheetSKUline, AgentCommissionInline )


# @admin.register(PurchaseOrder)
# class PurchaseOrderAdmin(admin.ModelAdmin):
#     list_display = (
#         "po_number",
#         "supplier",
#         "from_port",
#         "to_port",
#         # "total_value"

#     )
#     form = CustomFooForm
#     fieldsets = (
#         (None, {
#             'fields': ('a', "po_number"),
#         }),
#     )
    # inlines = (PurchaseOrderSKUInline, )
    
    
    
    
    

