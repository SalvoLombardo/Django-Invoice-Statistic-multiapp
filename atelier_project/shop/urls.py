from django.urls import path
from .views import (
    show_shop_categories_list, show_category_detail ,AddItemToCartView
    )


urlpatterns = [
    # Lista categorie
    path("categories/", show_shop_categories_list, name='shop_categories_list'),
    path("category/<slug:slug>/", show_category_detail, name='shop_category_detail'),
    path('cart/add/<int:product_id>/', AddItemToCartView.as_view(), name='add_to_cart'),
]