from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(TransactionType)
admin.site.register(TransactionStatus)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "cs",
        "bl",
        "transaction_type",
        "transaction_status",
        "amount"
    )

