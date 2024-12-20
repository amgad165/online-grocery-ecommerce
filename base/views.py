import json
from django.utils import timezone
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseServerError, JsonResponse
from .models import *
# from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
from django.urls import reverse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .utilities import mail
stripe.api_key = settings.STRIPE_SECRET_KEY
# The endpoint secret from Stripe webhook settings

# Create your views here.

def home(request):
    try:
        order = Order.objects.get(user = request.user, ordered=False)
    except:
        order = None

    try:
        best_products = Product.objects.filter(view_homepage = True)

    except:
        best_products = None

    context = {'order':order,'best_products':best_products}

    return render(request,"index.html", context)

@login_required
def edit_profile(request):

    try:
        orders_true = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')

    except:
        orders_true = None

    try:
        order = Order.objects.get(user = request.user, ordered=False)

    except:
        order = None

    orders_html = render_to_string('edit_profile_divs/orders_template.html', {'orders_true': orders_true})
    context = {'orders_true': orders_true,'order':order, 'orders_html': orders_html}

    return render(request,"editProfile.html", context)


@login_required
def products(request):

    # for inline_category in categories:
    #     private_products_by_category[inline_category.name] = Product.objects.filter(category='privat', inline_category=inline_category)
    #     business_products_by_category[inline_category.name] = Product.objects.filter(category='business', inline_category=inline_category)

    # # Get categories for private and business products
    # private_categories = [Category.get(name=category) for category, products in private_products_by_category.items() if products.exists()]
    # business_categories = [Category.get(name=category)  for category, products in business_products_by_category.items() if products.exists()]

    categories = Category.objects.all()

    products = Product.objects.select_related('inline_category').all()

    private_products_by_category = {}
    business_products_by_category = {}

    # Filter products by category and store them in dictionaries
    for inline_category in categories:
        private_products = products.filter(category='privat', inline_category=inline_category)
        business_products = products.filter(category='business', inline_category=inline_category)
        
        if private_products.exists():
            private_products_by_category[inline_category.name] = private_products
        if business_products.exists():
            business_products_by_category[inline_category.name] = business_products

    # Get categories for private and business products
    private_categories = [inline_category for inline_category in categories if inline_category.name in private_products_by_category]
    business_categories = [inline_category for inline_category in categories if inline_category.name in business_products_by_category]

    print(type(private_categories[0]))
    # privat_products = Product.objects.filter(category='privat')
    business_products = Product.objects.filter(category='business')


    try:
        order = Order.objects.get(user = request.user, ordered=False)
    except:
        order = None

    # Pass the filtered products to the template
    context = {
        'private_products_by_category': private_products_by_category,
        'business_products_by_category': business_products_by_category,
        'private_categories': private_categories,
        'business_categories': business_categories,

        'order' : order,
        'categories': categories
        
    }
    return render(request,"products.html", context)


@login_required
def submit_cash_payment(request):
    # Determine the type of transaction based on billing_reason
    
    try:
        order = Order.objects.filter(user=request.user, ordered=False).first()
        order.ordered = True
        order.save()


        order_items = order.items.all()
        order_items.update(ordered=True)
        # Start building items_lists as an HTML table
        items_lists = """
        <table style="width:100%; border-collapse: collapse; margin-top:20px;">
            <thead>
                <tr style="background-color:#f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Nummer</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Titel</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Artkilname</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Einheit</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Anz</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Populate each item and its ingredients in the table
        for index, item in enumerate(order_items, start=1):
            # Row for the item itself
            item_nummer = order.id + 10000
            items_lists += f"""
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{item}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                </tr>
            """
            
            # Rows for each ingredient within the item
            for ingredient in item.ingredients_customized.all():
                ingredient_nummer = ingredient.id + 10000
                items_lists += f"""
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient_nummer}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;"></td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.ingredient}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.ingredient.unit}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.quantity}</td>
                    </tr>
                """

        items_lists += "</tbody></table>"
        # Record the transaction
        Transaction.objects.create(
            user=order.user,
            amount=order.get_final_total(),  # Convert cents to euros
            order=order,
            subscription_type="cash"  # Set based on billing_reason
        )

        mail(order,settings.EMAIL_HOST_USER, items_lists)


        return redirect('success_page')
    except:
        return redirect('fail_page')


# if the order has products with no price , the user will be redirected to this view , the client and the owner should organize the money things
@login_required
def submit_order_without_price(request):
    # Determine the type of transaction based on billing_reason
    
    try:
        order = Order.objects.filter(user=request.user, ordered=False).first()


        order_items = order.items.all()

        # Start building items_lists as an HTML table
        items_lists = """
        <table style="width:100%; border-collapse: collapse; margin-top:20px;">
            <thead>
                <tr style="background-color:#f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Nummer</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Titel</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Artkilname</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Einheit</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Anz</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Populate each item and its ingredients in the table
        for index, item in enumerate(order_items, start=1):
            # Row for the item itself
            items_lists += f"""
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{item}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                </tr>
            """
            
            # Rows for each ingredient within the item
            for ingredient in item.ingredients_customized.all():
                ingredient_nummer = ingredient.id + 10000
                items_lists += f"""
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient_nummer}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;"></td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.ingredient}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.ingredient.unit}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.quantity}</td>
                    </tr>
                """

        items_lists += "</tbody></table>"
        # Record the transaction
        Transaction.objects.create(
            user=order.user,
            amount=order.get_final_total(),  # Convert cents to euros
            order=order,
            subscription_type="order without price"  # Set based on billing_reason
        )

        mail(order=order,sender = settings.EMAIL_HOST_USER,items_lists= items_lists, kind='order_without_price')

        order.ordered = True
        order.save()
        order_items.update(ordered=True)
        return redirect('success_page')
    except:
        return redirect('fail_page')

@login_required
def create_subscription(request):
    data = json.loads(request.body)
    payment_method_id = data.get('paymentMethodId')
    delivery_period = data.get('delivery_period')

    print(delivery_period)
    
    if not payment_method_id:
        return JsonResponse({'error': 'Payment Method ID is required'}, status=400)

    user = request.user
    profile, created = UserSubscription.objects.get_or_create(user=user)

    try:
        if not profile.stripe_customer_id:
            # Create a new Stripe customer and attach the payment method
            customer = stripe.Customer.create(
                email=user.email,
                payment_method=payment_method_id,
                invoice_settings={'default_payment_method': payment_method_id},
            )
            profile.stripe_customer_id = customer.id
            profile.save()
        else:
            # Retrieve the existing customer
            customer = stripe.Customer.retrieve(profile.stripe_customer_id)
            # Attach the payment method to the customer if not already attached
            try:
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=customer.id
                )
            except stripe.error.InvalidRequestError as e:
                if "already attached" not in str(e):
                    raise e
            # Set the payment method as the default for invoices
            stripe.Customer.modify(
                customer.id,
                email=user.email,
                invoice_settings={'default_payment_method': payment_method_id},
            )

        # Retrieve or create the order
        order = Order.objects.filter(user=user, ordered=False).first()
        if not order:
            return JsonResponse({'error': 'No active order found'}, status=404)
        
        order.delivery_frequency  = delivery_period
        order.save()

        # Calculate the total price based on the order
        total_price = order.get_final_total()

        # Create a price object dynamically
        price = stripe.Price.create(
            unit_amount=total_price,
            currency='eur',
            recurring={'interval': 'month'},
            product='prod_Q4rxAhFpks5pCn',
            metadata={'order_id': order.id}  
        )

        # Create the subscription using the dynamically created price
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': price.id}],
            expand=['latest_invoice.payment_intent'],
            metadata={'order_id': order.id}  
        )

        return JsonResponse({'status': 'success', 'subscription_id': subscription.id})
    except stripe.error.StripeError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def create_one_time_payment(request):
    data = json.loads(request.body)


    user = request.user
    profile, created = UserSubscription.objects.get_or_create(user=user)

    try:
        if not profile.stripe_customer_id:
            # Create a new Stripe customer and attach the payment method
            customer = stripe.Customer.create(
                email=user.email,
            )
            profile.stripe_customer_id = customer.id
            profile.save()
        else:
            # Retrieve the existing customer
            customer = stripe.Customer.retrieve(profile.stripe_customer_id)
            # Attach the payment method to the customer if not already attached

            # Set the payment method as the default for invoices
            stripe.Customer.modify(
                customer.id,  
                email=user.email,    
            )

        user = request.user

        # Retrieve or create the order
        order = Order.objects.filter(user=user, ordered=False).first()
        if not order:
            return JsonResponse({'error': 'No active order found'}, status=404)

        amount = order.get_final_total()

        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            customer=customer.id,
            amount=int(amount * 100),  # Convert to cents
            currency='eur',
            payment_method_types=['card'],
            metadata={'order_id': order.id}
        )

        return JsonResponse({'clientSecret': intent.client_secret})
    except stripe.error.StripeError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



# def load_modal_data(request):
#     order = Order.objects.filter(user=request.user, ordered=False).first()
#     if not order:
#         return JsonResponse({'error': 'No active order found'}, status=404)

#     total_price = order.get_total()  # Assuming get_total() returns the total as a float
#     print(total_price)
#     return JsonResponse({
#         'total_price': total_price,
    
#     })





@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.ENDPOINT_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        response_content = {
            "status": "error",
            "message": "Invalid payload",
            "detail": str(e)
        }
        return HttpResponse(json.dumps(response_content), status=400, content_type='application/json')
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        response_content = {
            "status": "error",
            "message": "Invalid signature",
            "detail": str(e)
        }
        return HttpResponse(json.dumps(response_content), status=400, content_type='application/json')

    # Dispatch event type to appropriate handler
    event_handlers = {
        'invoice.payment_succeeded': handle_payment_success,
        'invoice.payment_failed': handle_payment_failure,
        'customer.subscription.created': handle_subscription_created,
        'customer.subscription.updated': handle_subscription_updated,
        'customer.subscription.deleted': handle_subscription_deleted,
        'charge.refunded': handle_charge_refunded,
        'charge.failed': handle_charge_failed,
        'payment_intent.succeeded': handle_payment_intent_succeeded,
    }

    handler = event_handlers.get(event['type'])
    if handler:
        try:
            handler(event['data']['object'])
        except Exception as e:
            response_content = {
                "status": "error",
                "message": f"Error handling event {event['type']}",
                "detail": str(e)
            }
            return HttpResponse(json.dumps(response_content), status=500, content_type='application/json')
    else:
        response_content = {
            "status": "error",
            "message": f"Unhandled event type {event['type']}"
        }
        return HttpResponse(json.dumps(response_content), status=400, content_type='application/json')

    return HttpResponse(status=200)

def handle_payment_success(invoice):
    # Determine the type of transaction based on billing_reason
    billing_reason = invoice.get('billing_reason')
    if billing_reason == 'subscription_create' or billing_reason == 'subscription_cycle':
        transaction_type = 'active'
    else:
        transaction_type = 'one time purchase'

    # Extract order_id safely
    subscription_details = invoice.get('subscription_details', {})
    metadata = subscription_details.get('metadata', {})
    order_id = metadata.get('order_id')
    if not order_id:
        print("No order_id found in invoice metadata.")
        return

    try:
        order = Order.objects.get(id=order_id)
        order.ordered = True
        order.save()


        order_items = order.items.all()
        order_items.update(ordered=True)
        items_lists = """
        <table style="width:100%; border-collapse: collapse; margin-top:20px;">
            <thead>
                <tr style="background-color:#f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Nummer</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Titel</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Artkilname</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Einheit</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Anz</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Populate each item and its ingredients in the table
        for index, item in enumerate(order_items, start=1):
            # Row for the item itself
            item_nummer = order.id + 10000
            items_lists += f"""
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">{item_nummer}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{item}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                </tr>
            """
            
            # Rows for each ingredient within the item
            for ingredient in item.ingredients_customized.all():
                items_lists += f"""
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;"></td>
                        <td style="border: 1px solid #ddd; padding: 8px;"></td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.ingredient}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.ingredient.unit}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.quantity}</td>
                    </tr>
                """

        items_lists += "</tbody></table>"
    
        # Record the transaction
        Transaction.objects.create(
            user=order.user,
            amount=invoice['amount_paid'] / 100,  # Convert cents to dollars
            order=order,
            subscription_type=transaction_type  # Set based on billing_reason
        )

        mail(order,settings.EMAIL_HOST_USER, items_lists)


        print("Payment succeeded for invoice:", invoice['id'])
        return JsonResponse({"status": "success"}, status=200)

    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist.")


def handle_payment_intent_succeeded(payment_intent):
    # Determine the type of transaction based on billing_reason

    transaction_type = 'one time purchase'

    # Extract order_id safely
    metadata = payment_intent.get('metadata', {})
    order_id = metadata.get('order_id')
    if not order_id:
        print("No order_id found in payment_intent metadata.")
        return

    try:
        order = Order.objects.get(id=order_id)
        order.ordered = True
        order.save()


        order_items = order.items.all()
        order_items.update(ordered=True)
        items_lists = """
        <table style="width:100%; border-collapse: collapse; margin-top:20px;">
            <thead>
                <tr style="background-color:#f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Nummer</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Titel</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Artkilname</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Einheit</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Anz</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Populate each item and its ingredients in the table
        for index, item in enumerate(order_items, start=1):
            # Row for the item itself
            item_nummer = order.id + 10000
            items_lists += f"""
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">{item_nummer}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{item}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                    <td style="border: 1px solid #ddd; padding: 8px;"></td>
                </tr>
            """
            
            # Rows for each ingredient within the item
            for ingredient in item.ingredients_customized.all():
                items_lists += f"""
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;"></td>
                        <td style="border: 1px solid #ddd; padding: 8px;"></td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.ingredient}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.ingredient.unit}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{ingredient.quantity}</td>
                    </tr>
                """

        items_lists += "</tbody></table>"
    
        # Record the transaction
        Transaction.objects.create(
            user=order.user,
            amount=payment_intent['amount'] / 100,  # Convert cents to euros
            order=order,
            subscription_type=transaction_type  # Set based on billing_reason
        )


        mail(order,settings.EMAIL_HOST_USER, items_lists)


        print("Payment succeeded for payment intent:", payment_intent['id'])
        return JsonResponse({"status": "success"}, status=200)

    except Order.DoesNotExist as e:
        print(f"Order with id {order_id} does not exist.")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def handle_payment_failure(invoice):
    print("Payment failed for invoice:", invoice['id'])

def handle_subscription_created(subscription):
    customer_id = subscription['customer']
    try:
        
        user_subscription, created = UserSubscription.objects.get_or_create(stripe_customer_id=customer_id)

        user = user_subscription.user
        user_subscription.stripe_customer_id = customer_id
        user_subscription.save()

        # Assuming the initial transaction is handled here, no need to duplicate in handle_payment_success
        print("Subscription created for user:", user.email)
        return JsonResponse({"status": "success"}, status=200)

    except CustomUser.DoesNotExist as e:
        print(f"No user found with email {user.email}. Subscription not linked.")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    except stripe.error.StripeError as e:
        print(f"Stripe API error occurred: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def handle_subscription_updated(subscription):
    customer_id = subscription['customer']
    user_subscription = UserSubscription.objects.get(stripe_customer_id=customer_id)
    user = user_subscription.user 
    subscription_status = subscription['status']

    metadata = subscription.get('metadata', {})
    order_id = metadata.get('order_id')
    
    try:
        order = Order.objects.get(id=order_id)
        transaction = Transaction.objects.get(order=order, user=user)
    except Order.DoesNotExist as e:
        print(f"Order with id {order_id} does not exist.")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
 
    except Transaction.DoesNotExist as e:
        print(f"No transaction found for order ID {order_id} and user {user.email}.")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    if subscription_status == 'canceled':
        transaction.subscription_type = 'non active'
    elif subscription_status == 'active':
        transaction.subscription_type = 'active'
    elif subscription_status == 'paused':
        transaction.subscription_type = 'paused'
    elif subscription_status == 'incomplete' or subscription_status == 'past_due':
        transaction.subscription_type = 'non active'

    transaction.save()
    print(f"Subscription {subscription_status}:", subscription['id'])



    
def handle_subscription_deleted(subscription):
    customer_id = subscription['customer']

    try:
        user_subscription = UserSubscription.objects.get(stripe_customer_id=customer_id)
        user = user_subscription.user
    except UserSubscription.DoesNotExist:
        print(f"No user subscription found for customer ID {customer_id}.")
        return

    subscription_status = subscription['status']
    metadata = subscription.get('metadata', {})
    order_id = metadata.get('order_id')

    print(order_id)
    if not order_id:
        print("No order_id found in subscription metadata.")
        return

    try:
        # Assuming `order_id` is the ID of an Order object
        order = Order.objects.get(id=order_id)
        transaction = Transaction.objects.get(order=order, user=user)
    except Order.DoesNotExist as e:
        print(f"Order with id {order_id} does not exist.")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    except Transaction.DoesNotExist as e :
        print(f"No transaction found for order ID {order_id} and user {user.email}.")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    # Update the subscription type based on the subscription status
    if subscription_status == 'canceled':
        transaction.subscription_type = 'non active'
    else:
        print(f"Unhandled subscription status {subscription_status}")
        return

    transaction.save()
    print("Subscription deleted and transaction updated:", subscription['id'])
    return JsonResponse({'status': 'success', 'message': "Subscription deleted and transaction updated:"}, status=200)

def handle_charge_refunded(charge):
    customer_id = charge['customer']
    user_subscription = UserSubscription.objects.get(stripe_customer_id=customer_id)
    user = user_subscription.user 
    subscription_status = charge['status']

    metadata = charge.get('metadata', {})
    order_id = metadata.get('order_id')
    try:
        # Assuming `order_id` is the ID of an Order object
        order = Order.objects.get(id=order_id)
        transaction = Transaction.objects.get(order=order, user=user)
    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist.")
        return
    except Transaction.DoesNotExist:
        print(f"No transaction found for order ID {order_id} and user {user.email}.")
        return

    transaction.amount = -charge['amount_refunded'] / 100  # Convert cents to dollars
    transaction.save()
    print("Charge refunded:", charge['id'])
    return JsonResponse({'status': 'success', 'message': "refunded success"}, status=200)

def handle_charge_failed(charge):
    print("Charge failed:", charge['id'])


@login_required
def get_orders(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
    except Order.DoesNotExist:
        orders = []

    orders_html = render_to_string('edit_profile_divs/orders_template.html', {'orders_true': orders})

    return JsonResponse({'orders_html': orders_html})

@login_required
def get_address(request):
    if request.method == 'GET':
        user = request.user
        address_html = render_to_string('edit_profile_divs/address_div.html', {'user': user})
        return JsonResponse({'address_html': address_html})

@login_required
def address_change(request):
    if request.method == 'POST':
        
        bezirk = request.POST.get('bezirk')
        print(bezirk,'hhh')
        street_address = request.POST.get('street_address')
        hausnummer = request.POST.get('hausnummer')
        plz_zip = request.POST.get('plz_zip')

        user = request.user

        # Update the user's password
        user.bezirk = bezirk
        user.street_address = street_address
        user.hausnummer = hausnummer
        user.plz_zip = plz_zip

        user.save()

        return JsonResponse({'success': True, 'message': 'Address changed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_personal_info(request):
    if request.method == 'GET':
        user = request.user
        personal_html = render_to_string('edit_profile_divs/personal_data.html', {'user': user})
        return JsonResponse({'personal_html': personal_html})
    elif request.method == 'POST':
        # Update user details
        first_name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        tel = request.POST.get('tel')

        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.atu_number = tel

        user.save()
        personal_html = render_to_string('edit_profile_divs/personal_data.html', {'user': user})

        return JsonResponse({'personal_html': personal_html, 'success': True, 'message': 'User details updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        email_confirm = request.POST.get('email_confirm')
        password = request.POST.get('password')

        user = request.user

        # Validate email and email confirmation
        if email != email_confirm:
            return JsonResponse({'error': 'Email and email confirmation do not match'}, status=400)

        # Validate password
        if not check_password(password, user.password):
            return JsonResponse({'error': 'Ungültiges Passwort'}, status=400)

        # Check if the email already exists
        if CustomUser.objects.exclude(pk=user.pk).filter(email=email).exists():
            return JsonResponse({'error': 'Email is already in use'}, status=400)
        
        # Update user's email
        user.email = email
        user.save()

        return JsonResponse({'success': True, 'message': 'User email updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def password_change(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        new_pass = request.POST.get('newPass')
        confirm_newpass = request.POST.get('confirmNewPass')

        user = request.user

        # Check if the new password and confirmed new password match
        if new_pass != confirm_newpass:
            return JsonResponse({'error': 'New password and confirmed password do not match.'}, status=400)

        # Check if the new password is different from the old password
        if user.check_password(new_pass):
            return JsonResponse({'error': 'New password must be different from the old password.'}, status=400)

        # Update the user's password
        user.set_password(new_pass)
        user.save()

        return JsonResponse({'success': True, 'message': 'User Password changed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def my_orders_view(request):
    orders = ...  # Retrieve orders from the database
    orders_html = render_to_string('orders_template.html', {'orders': orders})
    return render(request, 'my_orders_page.html', {'orders_html': orders_html})




@login_required
def confirm_order(request):
    try:
        order = Order.objects.get(user = request.user, ordered=False)
    except:
        order = None

    context = {'order':order}


    return render(request, 'confirm_order.html',context)
    



def calculate_price(request):
    if request.method == 'POST':
        subscription_type = request.POST.get('subscription', 'one_time')
        coupon_code = request.POST.get('coupon_code', '')

        # Get the user's current order
        try:
            order = Order.objects.get(user=request.user, ordered=False)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'No active order found'}, status=404)

        # Set the delivery frequency in the order
        order.delivery_frequency = subscription_type
        order.save()

        # Attach coupon if provided
        coupon_message = ''

        if order.coupon :
            if order.coupon.is_valid():
                coupon_message = f"Rabattcode angewendet: {order.coupon.percent_off}%"

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid():
                    order.coupon = coupon
                    coupon.usage_count += 1
                    coupon.save()
                    order.save()
                    coupon_message = f"neu Rabattcode angewendet: {coupon.percent_off}%"
                else:
                    coupon_message = "Rabattcode ungültig oder abgelaufen."
            except Coupon.DoesNotExist:
                coupon_message = "bitte gib einen gültigen Rabattcode ein ."


        # Calculate the final price with the new `get_final_total` method
        final_price = order.get_final_total()
        
        # Minimum charge message, if applied
        min_charge_message = ''
        if final_price == 50:
            min_charge_message =  f"Die Bestellsumme beträgt: €{order.get_total_with_coupon():.2f}. Mindestgebühr in Höhe von €50 wurde angewendet."

        # Response messages for clarity
        response_message = {
            'coupon_message': coupon_message,
            'min_charge_message': min_charge_message,
        }


        return JsonResponse({
            'final_price': f"{final_price:.2f}",
            'messages': response_message
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)






@login_required
def confirm_address(request):
    delivery_address = None
    if request.method == 'POST':
        address_type = request.POST.get('addressType')
        
        if address_type == 'delivery':
            # Get the shipping address fields from the form
            bezirk = request.POST.get('input7_shipping')
            street_address = request.POST.get('input4_shipping')
            hausnummer = request.POST.get('input8_shipping')
            plz_zip = request.POST.get('input6_shipping')
            additional_info = request.POST.get('input5_shipping')
            phone = request.POST.get('input9_shipping')
            # Check if the user already has a delivery address
            delivery_address, created = DeliveryAddress.objects.get_or_create(user=request.user)
            
            # Update the delivery address
            delivery_address.bezirk = bezirk
            delivery_address.street_address = street_address
            delivery_address.hausnummer = hausnummer
            delivery_address.plz_zip = plz_zip
            delivery_address.additional_info = additional_info
            delivery_address.phone_number = phone
            delivery_address.save()

            current_user = request.user
            current_user.address_type = 'delivery'
            current_user.save()

            return redirect('confirm_order')  
            
        else:
            current_user = request.user
            current_user.address_type = 'billing'
            current_user.save()
            return redirect('confirm_order')  

    else:
        # Check if the user already has a delivery address
        try:
            delivery_address = DeliveryAddress.objects.get(user=request.user)
        except DeliveryAddress.DoesNotExist:
            delivery_address = None

    try:
        order = Order.objects.get(user = request.user, ordered=False)
    except:
        order = None

    context = {'order':order,'delivery_address': delivery_address}

    return render(request, 'confirm_address.html', context)

def signup(request):
    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            if user.role == "company":
                user.is_active = False
                mail(None,settings.EMAIL_HOST_USER, None, user = user,kind = "company_confirmation")
                user.save()
                return JsonResponse({'waiting_acceptance': "your account has been created and waiting for approval"})

            else:
                login(request, user)
                return JsonResponse({'success': True})  # Return success JSON response


        else:
            error_message = list(form.errors.values())[0][0]
            return JsonResponse({'error': error_message}, status=400)
        




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})  # Redirect or return success JSON response
        else:
            return JsonResponse({'error': 'ungültige Anmeldedaten'}, status=400)  # Return errors JSON response with status 400
        




def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        
        # get customized ingredient quantities from product detail modal
        ingredient_quantities = request.POST.get('ingredient_quantities')
        ingredient_quantities = json.loads(ingredient_quantities) if ingredient_quantities else {}

        # Filter out items with a quantity of 0
        ingredient_quantities = {k: v for k, v in ingredient_quantities.items() if v != 0}

        # Check if all values were zero (dictionary is empty after filtering)
        if not ingredient_quantities:
            return JsonResponse({'error': 'Die Mengen aller Zutaten dürfen nicht Null sein.'}, status=400)

        # Continue processing ingredient_quantities here if not empty
        print("Filtered ingredient quantities:", ingredient_quantities)

        if ingredient_quantities:

            current_user = request.user
            product = get_object_or_404(Product, id=product_id)

            # Create an empty list to store order items
            order_items = []

            # Create OrderItem for the product
            order_item = OrderItem.objects.create(product=product, user=current_user, ordered=False)

            # save the customized quantity for each ingredient in the product in a model
            # Attach the product's ingredients and their quantities to the OrderItem
            for ingredient_id, quantity in ingredient_quantities.items():
                ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    
                # Set the product_id when creating the ProductIngredient object
                product_ingredient = IngredientUserCustomize.objects.create(product=product, ingredient=ingredient, quantity=quantity)
                order_item.ingredients_customized.add(product_ingredient)

            # Append the OrderItem to the list
            order_items.append(order_item)
            
            # Create or retrieve the user's open order
            order_qs = Order.objects.filter(user=current_user, ordered=False)
            if order_qs.exists():
                order = order_qs.first()
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user=current_user, ordered_date=ordered_date)

            # Add the OrderItems to the order
            for item in order_items:
                order.items.add(item)

            # Get total quantity of items in the cart
            cart_items = order.items.all()
            total_quantity = sum(item.quantity for item in cart_items)

            return JsonResponse({'success': 'Item added to cart', 'cart_items_count': total_quantity})
        else:
            print('error')
            return JsonResponse({'error': 'Invalid quantity , please try again'}, status=400)  # Return HTTP 400 Bad Request for invalid quantity

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def update_cart(request):
    
    if request.method == "POST":

        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')

        # Get the order item corresponding to the item ID and current user
        order_item = OrderItem.objects.filter(id=item_id, user=request.user).first()

        if order_item:
            # Update the quantity of the order item
            order_item.quantity = quantity
            order_item.save()

            product_price = order_item.get_total_item_price()
            item_weight = order_item.get_total_order_quantity()
            print(product_price)
            order = Order.objects.filter(items=order_item).first()
            order_total = order.get_total()
            
            # Get total quantity of items in the cart
            cart_items = order.items.all()
            total_quantity = sum(item.quantity for item in cart_items)

            # Return a JSON response indicating success
            return JsonResponse({"message": "Cart updated successfully","order_total":order_total,"product_price":product_price,"item_weight":item_weight,'cart_items_count': total_quantity}, status=200)
        else:
            # Return an error response if the order item is not found
            return JsonResponse({"error": "Order item not found"}, status=404)

    # Return an error response for non-POST requests
    return JsonResponse({"error": "Invalid request method"}, status=405)





@login_required
def remove_item(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        user = request.user
        
        # Delete the OrderItem
        order_item = OrderItem.objects.filter(
            product__id=product_id,
            user=user,
            ordered=False
        ).first()
        
        if order_item:
            order_item.delete()
        
        order = Order.objects.get(user=user, ordered=False) 
        if order:
            
            cart_items = order.items.all()
            
            total_quantity = sum(item.quantity for item in cart_items)

            # Calculate the updated total price
            updated_total_price = float(order.get_total())

            # Return the updated total price as JSON response
            return JsonResponse({'order_total': updated_total_price,"cart_items_count":total_quantity})
        
    return JsonResponse({'message': 'Invalid request'}, status=400)






def success_page(request):
    try:
        order = Order.objects.filter(user=request.user).order_by('-ordered_date').first()
    except:
        order = None

    context = {'order':order}

    return render(request, 'success_page.html', context)

def fail_page(request):
    try:
        order = Order.objects.get(user = request.user, ordered=False)
    except:
        order = None

    context = {'order':order}
    return render(request, 'failed_page.html', context)







def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        message = request.POST.get('message')
        
        # Create and save the contact instance
        contact = Contact(
            name=name,
            email=email,
            telephone_number=phone,
            address = address,
            message=message
        )
        contact.save()

        # Redirect to a success page
        return redirect('success_contact')
    
    return render(request, 'index.html')  # If not POST, render the index page again


def success_contact(request):
    try:
        order = Order.objects.get(user = request.user, ordered=False)
    except:
        order = None

    context = {'order':order}
    return render(request, 'success_contact.html', context)



def impressum(request):
    try:
        order = Order.objects.get(user = request.user, ordered=False)
    except:
        order = None

    context = {'order':order}

    return render(request, 'impressum.html', context)

def datenschutzerklarung(request):
    try:
        order = Order.objects.get(user = request.user, ordered=False)
    except:
        order = None

    context = {'order':order}

    return render(request, 'datenschutzerklarung.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  