from django.contrib import admin
from .models  import Product, Size,ProductReview


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}



admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(ProductReview)