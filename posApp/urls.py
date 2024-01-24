# posApp/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('redirect-admin/', RedirectView.as_view(url="/admin"), name="redirect-admin"),
    path('', views.home, name="home-page"),
    # path('login/', auth_views.LoginView.as_view(template_name='posApp/login.html', redirect_authenticated_user=True), name="login"),
    # path('userlogin/', views.login_user, name="login-user"),
    # path('logout/', views.logoutuser, name="logout"),
    # path('register/', views.register, name='register'),  # Add registration URL
    path('category/', views.category, name="category-page"),
    path('manage_category/', views.manage_category, name="manage_category-page"),
    path('save_category/', views.save_category, name="save-category-page"),
    path('delete_category/', views.delete_category, name="delete-category"),
    path('products/', views.products, name="product-page"),
    path('manage_products/', views.manage_products, name="manage_products-page"),
    path('test/', views.test, name="test-page"),
    path('save_product/', views.save_product, name="save-product-page"),
    path('delete_product/', views.delete_product, name="delete-product"),
    path('pos/', views.pos, name="pos-page"),
    path('checkout-modal/', views.checkout_modal, name="checkout-modal"),
    path('save-pos/', views.save_pos, name="save-pos"),
    path('sales/', views.salesList, name="sales-page"),
    path('receipt/', views.receipt, name="receipt-modal"),
    path('delete_sale/', views.delete_sale, name="delete-sale"),
]

