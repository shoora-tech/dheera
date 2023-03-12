from django.db import models
from dheera.models import UUIDModel
from process.models import BL, CostSheet
# Create your models here.

class TransactionType(UUIDModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class TransactionStatus(UUIDModel):
    CREDIT = "credit"
    DEBIT = "debit"

    TRANSACTION_STATUS_CHOICES = (
        (DEBIT, "Debit"),
        (CREDIT, "Credit"),
    )

    status = models.CharField(
        choices=TRANSACTION_STATUS_CHOICES,
        default=DEBIT,
        max_length=10
    )

    def __str__(self):
        return self.status


class Transaction(UUIDModel):
    bl = models.ForeignKey(BL, on_delete=models.CASCADE, related_name="transaction", null=True, blank=True)
    cs = models.ForeignKey(CostSheet, on_delete=models.CASCADE, related_name="transaction")
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name="transaction")
    transaction_status = models.ForeignKey(TransactionStatus, on_delete=models.CASCADE, related_name="transaction")
    amount = models.FloatField()
