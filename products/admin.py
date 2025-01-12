from django.contrib import admin
from .models import Product, Category, DeviceType, Review

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'device_type', 
        'price',
        'price_good', 
        'price_amazing',
        'rating',
        'image',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

class DeviceTypeAdmin(admin.ModelAdmin):  
    list_display = (
        'name',
        'friendly_name',
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'rating')
    list_filter = ('rating', 'created_at')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)
admin.site.register(Review, ReviewAdmin)