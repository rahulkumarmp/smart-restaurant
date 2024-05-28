from django.urls import include, re_path
from .views import *
from django.urls import path
from . import views
# urlpatterns = [
#     re_path('login/', login, name='login'),
#     re_path('home/', home, name='home'),
#     re_path('add_customer/', add_customer, name='add_customer'),
#     re_path('add_to_cart/', add_to_cart, name='add_to_cart'),
#     re_path('cart/', cart, name='cart'),
#     re_path('cart/delete/<int:cart_item_id>/', delete_cart_item, name='delete_cart_item'),
#     re_path('cart/increase/<int:cart_item_id>/', increase_quantity, name='increase_quantity'),
# ]
urlpatterns = [
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/increase/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),

]