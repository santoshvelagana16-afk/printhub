from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['service', 'quantity', 'unit_price', 'total_price',
                       'file_name', 'file_preview', 'configuration']
    fields = ['service', 'quantity', 'unit_price', 'total_price',
              'file_name', 'file_preview', 'configuration']

    def file_preview(self, obj):
        if not obj.uploaded_file:
            return format_html('<span style="color:#9ca3af;font-size:12px;">No file</span>')
        url  = obj.uploaded_file.url
        name = obj.file_name or 'file'
        ext  = name.lower().rsplit('.', 1)[-1] if '.' in name else ''

        if ext in ('jpg', 'jpeg', 'png', 'gif', 'webp'):
            return format_html(
                '<div style="display:flex;align-items:center;gap:10px;">'
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:56px;width:56px;object-fit:cover;border-radius:6px;border:1px solid #e5e7eb;" alt="{}">'
                '</a>'
                '<a href="{}" download="{}" style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:50px;font-size:11px;font-weight:700;text-decoration:none;">⬇ Download</a>'
                '</div>',
                url, url, name, url, name
            )
        elif ext == 'pdf':
            return format_html(
                '<div style="display:flex;align-items:center;gap:8px;">'
                '<span style="background:#fee2e2;color:#ef4444;padding:4px 10px;border-radius:6px;font-size:12px;font-weight:700;">📄 PDF</span>'
                '<a href="{}" target="_blank" style="background:#fef9c3;color:#a16207;padding:4px 12px;border-radius:50px;font-size:11px;font-weight:700;text-decoration:none;">👁 Preview</a>'
                '<a href="{}" download="{}" style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:50px;font-size:11px;font-weight:700;text-decoration:none;">⬇ Download</a>'
                '</div>',
                url, url, name
            )
        else:
            return format_html(
                '<a href="{}" download="{}" style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:50px;font-size:11px;font-weight:700;text-decoration:none;">⬇ Download {}</a>',
                url, name, name
            )
    file_preview.short_description = 'Uploaded File'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['order_number', 'user', 'status', 'payment_method',
                     'total_amount', 'file_count', 'created_at']
    list_filter   = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    list_editable = ['status']
    inlines       = [OrderItemInline]
    readonly_fields = ['order_number', 'user', 'subtotal', 'tax',
                       'total_amount', 'created_at']

    def file_count(self, obj):
        count = obj.items.exclude(uploaded_file='').exclude(uploaded_file=None).count()
        if count:
            return format_html(
                '<span style="background:#dbeafe;color:#1d4ed8;padding:2px 10px;border-radius:50px;font-size:11px;font-weight:700;">{} file{}</span>',
                count, 's' if count != 1 else ''
            )
        return format_html('<span style="color:#9ca3af;font-size:12px;">—</span>')
    file_count.short_description = 'Files'


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['service', 'quantity', 'unit_price', 'total_price',
                       'file_name', 'cart_file_preview']

    def cart_file_preview(self, obj):
        if not obj.uploaded_file:
            return format_html('<span style="color:#9ca3af;font-size:12px;">No file</span>')
        url  = obj.uploaded_file.url
        name = obj.file_name or 'file'
        return format_html(
            '<a href="{}" download="{}" style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:50px;font-size:11px;font-weight:700;text-decoration:none;">⬇ {}</a>',
            url, name, name
        )
    cart_file_preview.short_description = 'File'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_item_count', 'get_total', 'updated_at']
    inlines      = [CartItemInline]
