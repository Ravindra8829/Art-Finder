from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields = ['product']
    # readonly_fields


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False


class DispatchAdmin(admin.AdminSite):
    site_header = 'Dispatch Admin'


dispatch_site = DispatchAdmin(name='DispatchAdmin')

dispatch_site.register(Order)
