from django.contrib import admin
from .models import Category, Product, Contact, Commentary, OrderProduct, Order, Payment
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("email", "date")
    list_filter = ['date']
    search_fields = ['email']


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'price', 'is_active', 'updated')
    list_filter = ('category', 'is_active', 'updated')
    search_fields = ('title',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')
    list_filter = ('timestamp',)


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'ordered')
    list_filter = ('ordered',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered', 'payment', 'ordered_date', 'order_receive_date', 'status')
    list_filter = ('ordered', 'ordered_date', 'order_receive_date', 'status')


admin.site.register(Category)




