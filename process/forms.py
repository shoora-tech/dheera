from django import forms
from .models import PurchaseOrder


class CustomFooForm(forms.ModelForm):
    a = forms.CharField()
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        widgets = {
            'a': forms.TextInput(),
        }