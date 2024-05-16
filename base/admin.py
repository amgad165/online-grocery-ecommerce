from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(CustomUser)

class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductIngredientInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Ingredient)


admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(UserSubscription)
admin.site.register(Transaction)
