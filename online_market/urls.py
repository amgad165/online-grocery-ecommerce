"""online_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('products/', views.products,name='products'),
    path('signup/', views.signup,name='signup'),
    path('login/', views.login_view,name='login_view'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_item/', views.remove_item, name='remove_item'),

    # path('submit_payment/', views.submit_payment, name='submit_payment'),

    # path('update_product/', views.update_product, name='update_product'),
    
    # path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),

    path('create_subscription/', views.create_subscription, name='create_subscription'),

    path('load_modal_data/', views.load_modal_data, name='load_modal_data'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('success_page/', views.success_page, name='success_page'),
    path('fail_page/', views.fail_page, name='fail_page'),


    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('get_orders/', views.get_orders, name='get_orders'),
    path('get_personal_info/', views.get_personal_info, name='get_personal_info'),
    path('update_email/', views.update_email, name='update_email'),
    path('password_change/', views.password_change, name='password_change'),
    path('get_address/', views.get_address, name='get_address'),
    path('address_change/', views.address_change, name='address_change'),


    path('logout/', views.logout_view, name='logout'),
    # path('error/', views.error, name='error'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)