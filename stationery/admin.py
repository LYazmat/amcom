from django.contrib import admin
from .models import Product, Customer, Seller, DefaultComission


@admin.register(Product, Customer, Seller, DefaultComission)
class DefaultAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
