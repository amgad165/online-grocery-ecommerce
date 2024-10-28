
from django.contrib import admin
from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('signup/', views.signup,name='signup'),
    path('login/', views.login_view,name='login_view'),
    path('submit_contact/', views.submit_contact,name='submit_contact'),
    path('success_contact/', views.success_contact,name='success_contact'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('products/', views.products,name='products'),

    # path('submit_payment/', views.submit_payment, name='submit_payment'),

    # path('update_product/', views.update_product, name='update_product'),
    
    # path('create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),

    path('create_subscription/', views.create_subscription, name='create_subscription'),
    path('create_one_time_payment/', views.create_one_time_payment, name='create_one_time_payment'),
    path('submit_cash_payment/', views.submit_cash_payment, name='submit_cash_payment'),
    path('submit_order_without_price/', views.submit_order_without_price, name='submit_order_without_price'),

    # path('load_modal_data/', views.load_modal_data, name='load_modal_data'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('success_page/', views.success_page, name='success_page'),
    path('fail_page/', views.fail_page, name='fail_page'),


    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('get_orders/', views.get_orders, name='get_orders'),
    path('get_personal_info/', views.get_personal_info, name='get_personal_info'),
    path('update_email/', views.update_email, name='update_email'),
    path('password_change/', views.password_change, name='password_change'),
    path('get_address/', views.get_address, name='get_address'),
    path('address_change/', views.address_change, name='address_change'),
    path('calculate-price/', views.calculate_price, name='calculate_price'),

    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('confirm_address/', views.confirm_address, name='confirm_address'),

    path('logout/', views.logout_view, name='logout'),
    # path('error/', views.error, name='error'),




    path('impressum/', views.impressum, name='impressum'),
    path('datenschutzerklarung /', views.datenschutzerklarung, name='datenschutzerklarung'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
