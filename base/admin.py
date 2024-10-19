from django.contrib import admin
from . models import *
from django.db.models import Sum

# Register your models here.

admin.site.register(CustomUser)

class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductIngredientInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Ingredient)

admin.site.register(Category)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','order_summary','get_user_telefon', 'get_user_email','get_user_role',
                    'get_bezirk', 'get_street_address', 'get_hausnummer', 'get_plz_zip','get_subscription_type' , 'delivery_frequency' , 'being_delivered',
                    'get_total','ordered_date')
    list_editable = ('being_delivered',)  # Add this line to make 'being_delivered' editable

    def get_queryset(self, request):
        # Override get_queryset to include only orders where ordered = True
        return super().get_queryset(request).filter( ordered=True, being_delivered=False)

    def order_summary(self, obj):
        return ", ".join([f"{item.quantity} x {item.product.name}" for item in obj.items.all()])
    order_summary.short_description = 'Order Summary'




    def get_user_telefon(self, obj):
        return obj.user.atu_number if obj.user.atu_number else ""
    get_user_telefon.short_description = 'Telefon'

    def get_user_email(self, obj):
        return obj.user.email if obj.user.email else ""
    get_user_email.short_description = 'Email'

    def get_user_role(self, obj):
        return obj.user.role if obj.user.role else ""
    get_user_role.short_description = 'Role'


    def get_bezirk(self, obj):
        return obj.user.bezirk if obj.user else ""
    get_bezirk.short_description = 'Bezirk'

    def get_street_address(self, obj):
        return obj.user.street_address if obj.user else ""
    get_street_address.short_description = 'Street Address'

    def get_hausnummer(self, obj):
        return obj.user.hausnummer if obj.user else ""
    get_hausnummer.short_description = 'Hausnummer'

    def get_plz_zip(self, obj):
        return obj.user.plz_zip if obj.user else ""
    get_plz_zip.short_description = 'PLZ/ZIP'



    def get_total(self, obj):
            total = obj.transaction_order.aggregate(total_amount=Sum('amount'))['total_amount']
            return total if total else 0
    get_total.short_description = 'Total'

    def being_delivered(self, obj):
        return obj.being_delivered
    being_delivered.short_description = 'Delivered'

    def get_subscription_type(self, obj):
        # Get the most recent transaction related to this order
        latest_transaction = obj.transaction_order.order_by('-created_at').first()
        return latest_transaction.subscription_type if latest_transaction else ""
    get_subscription_type.short_description = 'Subscription Type'

admin.site.register(Order, OrderAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_summary', 'get_user_telefon', 'get_user_email', 'get_user_role',
                    'get_bezirk', 'get_street_address', 'get_hausnummer', 'get_plz_zip', 'get_subscription_type', 'delivery_frequency', 'being_delivered',
                    'get_total', 'ordered_date')
    list_editable = ('being_delivered',)  # Add this line to make 'being_delivered' editable

    def get_queryset(self, request):
        # Override get_queryset to include only orders where subscription_type is 'active' or 'non-active'
        return super().get_queryset(request).filter(transaction_order__subscription_type__in=['active', 'non-active'],being_delivered=False)

    def order_summary(self, obj):
        return ", ".join([f"{item.quantity} x {item.product.name}" for item in obj.items.all()])
    order_summary.short_description = 'Order Summary'

    def get_user_telefon(self, obj):
        return obj.user.atu_number if obj.user.atu_number else ""
    get_user_telefon.short_description = 'Telefon'

    def get_user_email(self, obj):
        return obj.user.email if obj.user.email else ""
    get_user_email.short_description = 'Email'

    def get_user_role(self, obj):
        return obj.user.role if obj.user.role else ""
    get_user_role.short_description = 'Role'

    def get_bezirk(self, obj):
        return obj.user.bezirk if obj.user else ""
    get_bezirk.short_description = 'Bezirk'

    def get_street_address(self, obj):
        return obj.user.street_address if obj.user else ""
    get_street_address.short_description = 'Street Address'

    def get_hausnummer(self, obj):
        return obj.user.hausnummer if obj.user else ""
    get_hausnummer.short_description = 'Hausnummer'

    def get_plz_zip(self, obj):
        return obj.user.plz_zip if obj.user else ""
    get_plz_zip.short_description = 'PLZ/ZIP'

    def get_total(self, obj):
        total = obj.transaction_order.aggregate(total_amount=Sum('amount'))['total_amount']
        return total if total else 0
    get_total.short_description = 'Total'

    def being_delivered(self, obj):
        return obj.being_delivered
    being_delivered.short_description = 'Delivered'

    def get_subscription_type(self, obj):
        # Get the most recent transaction related to this order
        latest_transaction = obj.transaction_order.order_by('-created_at').first()
        return latest_transaction.subscription_type if latest_transaction else ""
    get_subscription_type.short_description = 'Subscription Type'

admin.site.register(SubscriptionOrder, SubscriptionAdmin)

admin.site.register(Transaction)
admin.site.register(DeliveryAddress)

admin.site.register(Contact)
admin.site.register(ExcludedProduct)


admin.site.register(Coupon)

# Custom admin for Inactive Company Users# Custom admin for Inactive Company Users
class InactiveCompanyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'company_name', 'atu_number','is_active', 'date_joined', 'role')
    list_filter = ('is_active', 'role')
    search_fields = ('email', 'first_name', 'last_name', 'company_name')
    list_editable = ('is_active',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(role=CustomUser.COMPANY, is_active=False)

# Register the custom admin class for inactive company users
admin.site.register(InactiveCompanyUser, InactiveCompanyUserAdmin)




# admin.site.register(UserSubscription)
# admin.site.register(OrderItem)