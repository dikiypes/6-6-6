from django.contrib import admin

from catalog.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_sale_price',
                    'product_category_name', )
    search_fields = ('product_name', 'product_description', )
    list_filter = ('product_category_name', )


@admin.register(Category)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', )
