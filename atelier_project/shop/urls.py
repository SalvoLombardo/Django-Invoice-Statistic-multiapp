from django.urls import path
from .views import (
    show_shop_categories_list, show_category_detail ,AddItemToCartView, CartDashboardView, DeactivateCartView
    )


urlpatterns = [
    # Lista categorie
    path("categories/", show_shop_categories_list, name='shop_categories_list'),
    path("category/<slug:slug>/", show_category_detail, name='shop_category_detail'),
    path('cart/add/<int:product_id>/', AddItemToCartView.as_view(), name='add_to_cart'),
    path('cart/cart_dashboard/', CartDashboardView.as_view(), name='cart_dashboard'),
    path('cart/cart_dashboard/deactivate_cart/<int:pk>', DeactivateCartView.as_view(), name='deactivate_cart'),



]