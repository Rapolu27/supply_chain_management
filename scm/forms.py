# forms.py
from django import forms
from .models import Supplier, Product, PurchaseOrder
from django.db import models
from django.core.exceptions import ValidationError
from scm_core.validator import (
    validate_supplier_name, 
    validate_supplier_mobile, 
    validate_active_supplier
)
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name', 
            'email', 
            'phone_number', 
            'address', 
            'city', 
            'country', 
            'company_name'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Full Address', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        validate_supplier_mobile(mobile)
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        active = cleaned_data.get('active')
        address = cleaned_data.get('address')
        email = cleaned_data.get('email')
        return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'supplier']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Product Description', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Quantity'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }
        constraints = [
            models.UniqueConstraint(fields=['name', 'supplier'], name='unique_product_supplier')
        ]
        def clean(self):
            if self.quantity < 0:
                raise ValidationError(("Quantity cannot be less than 0."))

        def __str__(self):
            return self.name

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'product', 'quantity',  'delivery_date', 'status']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            # 'order_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }