from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.home, name="home"),
    path("about/", views.about, name="about"),
    path("charity/", views.charity_view, name="charity"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-and-conditions/", views.terms, name="terms"),
    path("contact/", views.contact, name="contact"),

    path("super-admin/login/", views.custom_admin_login, name="super_admin_login"),
    path("logout/", views.custom_admin_logout, name="super_admin_logout"),
    path("super-admin/dashboard/", views.custom_admin_dashboard, name="super_admin_dashboard"),


    path('news/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/update/', views.news_update, name='news_update'),
    path('news/delete/<int:pk>/', views.news_delete, name='news_delete'),

    path("admin-charity/", views.charity_management, name="charity_management"),
    path("admin-charity/delete/<int:pk>/", views.charity_delete, name="charity_delete"),

    path("banners/", views.banner_list_view, name="banner-list"),
    path("banners/add/", views.banner_add_view, name="banner-add"),
    path("banners/<int:pk>/edit/", views.banner_edit, name="banner-edit"),
    path("banners/<int:pk>/delete/", views.banner_delete, name="banner-delete"),

    path('customers/', views.customer_list, name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('customer/delete/<int:id>/', views.delete_customer, name='delete_customer'),


    path("customers/<int:pk>/payments/modal/", views.payment_modal, name="payment_modal"),
    path("customers/<int:pk>/payments/add/", views.add_payment, name="add_payment"),
    path("customers/<int:pk>/change-password/modal/", views.change_password_modal, name="change_password_modal"),

    path("payments/", views.payments_list, name="payments_list"),
    path("payments/edit/", views.edit_payment, name="edit_payment"),

    path("about-us/", views.about_us_list, name="about-us-list"),
    path('about-us/add/', views.about_us_add, name='about-us-add'),
    path("about-us/image-delete/<int:pk>/", views.about_us_image_delete, name="about-us-image-delete"),

    path('register-customer/', views.register_customer, name='register_customer'),
    path('customer-login/', views.customer_login, name='customer-login'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/", views.reset_password, name="reset_password"),


    path("customer/dashboard/", views.customer_dashboard, name="customer_dashboard"),
    path('matching-profiles/', views.matching_profiles, name='matching_profiles'),
    path('send-interest/', views.send_interest, name='send_interest'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
   
]

