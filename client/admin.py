from django.contrib import admin

from .models import ContactMessage, JobApplication, JobOffer, Order, Product


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


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'contract_type', 'is_active', 'created_at')
    list_filter = ('is_active', 'contract_type', 'department')
    search_fields = ('title', 'department', 'description', 'profile')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'offer', 'is_spontaneous', 'is_processed', 'created_at')
    list_filter = ('is_spontaneous', 'is_processed', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'position', 'message')
    list_editable = ('is_processed',)
    readonly_fields = (
        'offer', 'is_spontaneous', 'first_name', 'last_name', 'email',
        'phone', 'position', 'cv_link', 'message', 'created_at',
    )
    ordering = ('-created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
    ordering = ('-created_at',)
