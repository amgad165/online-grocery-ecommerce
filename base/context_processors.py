from base.models import Order, OrderItem  # Import your Order and OrderItem models
from django.conf import settings

def cart_count(request):
    if request.user.is_authenticated:
        # Get the cart for the logged-in user
        user = request.user
        cart = Order.objects.filter(user=user, ordered=False).first()

        if cart:
            # Calculate the total number of items and their quantities in the cart
            cart_items = cart.items.all()
            total_quantity = sum(item.quantity for item in cart_items)
        else:
            total_quantity = 0
    else:
        total_quantity = 0

    return {'total_quantity': total_quantity}



def stripe_puplishable_key(request):
    return {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLISHABLE_KEY}