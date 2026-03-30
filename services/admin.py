from django.contrib import admin
from .models import ServiceCategory, Service, PrintingOption, BindingOption, CustomPrintOption

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

class PrintingOptionInline(admin.TabularInline):
    model = PrintingOption
    extra = 1

class BindingOptionInline(admin.TabularInline):
    model = BindingOption
    extra = 1

class CustomPrintOptionInline(admin.TabularInline):
    model = CustomPrintOption
    extra = 1

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price', 'is_active']
    list_filter = ['category', 'is_active']
    inlines = [PrintingOptionInline, BindingOptionInline, CustomPrintOptionInline]
