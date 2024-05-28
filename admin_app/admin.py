from django.contrib import admin
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import format_html

from admin_app.models import Table, Menu, Invoice
from user_app.global_functions import generate_invoice_pdf
from user_app.models import Cart
from django.urls import path


# Register your models here.
class TableAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Table._meta.fields]
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')
    # change_list_template = "admin_app/template/actions.html"

    actions = ['generate_invoice']

    def generate_invoice(self, request, queryset):
        for table in queryset:
            self.create_invoice(table)
        self.message_user(request, "Invoices generated successfully")

    generate_invoice.short_description = "Generate Invoice for selected tables"

    def create_invoice(self, table):
        # Get all cart items for the table
        cart_items = Cart.objects.filter(table=table)
        print(cart_items)
        if not cart_items:
            return

        # Generate PDF Invoice
        generate_invoice_pdf(table, cart_items)

        # Mark cart items as closed
        cart_items.update(is_closed=True)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-invoice/<int:table_id>/', self.admin_site.admin_view(self.generate_invoice_view),
                 name='generate_invoice'),
        ]
        return custom_urls + urls

    def generate_invoice_view(self, request, table_id):
        table = get_object_or_404(Table, pk=table_id)
        self.create_invoice(table)
        self.message_user(request, "Invoice generated successfully")
        return redirect('admin:admin_app_table_changelist')

class MenuAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Menu._meta.fields]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('table', 'created_at', 'updated_at', 'download_link')

    def download_link(self, obj):
        if obj.file:
            return format_html('<a href="{}">Download</a>', obj.file.url)
        return "No file"

    download_link.short_description = 'Download Invoice'

    download_link.short_description = 'Download Invoice'

admin.site.register(Table,TableAdmin)
admin.site.register(Menu, MenuAdmin)
# admin.site.register(Invoice)
