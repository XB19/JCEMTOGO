from django.contrib import admin

from .models import Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('category', 'name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_reference', 'first_name', 'last_name', 'phone', 'status', 'payment_method', 'total_amount', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone', 'email', 'address', 'company')
    list_filter = ('status', 'payment_method', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'order_reference')
    fieldsets = (
        ('Client', {
            'fields': ('order_reference', 'first_name', 'last_name', 'company', 'phone', 'email')
        }),
        ('Livraison', {
            'fields': ('address', 'instructions', 'delivery_slot', 'status')
        }),
        ('Commande', {
            'fields': ('products', 'total_amount', 'payment_method', 'notes')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
