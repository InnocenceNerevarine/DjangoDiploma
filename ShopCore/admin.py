from django.contrib import admin
from .models import Category, Product, Contact, Commentary, OrderProduct, Order, Payment
from import_export.admin import ImportExportModelAdmin


@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("email", "date")
    list_filter = ['date']
    search_fields = ['email']


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body', 'created', 'active')
    list_filter = ('active', 'created', 'update')
    search_fields = ('name', 'email', 'body')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'price', 'is_active', 'updated')
    list_filter = ('category', 'is_active', 'updated')
    search_fields = ('title',)


admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Payment)

