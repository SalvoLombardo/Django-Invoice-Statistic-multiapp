from django.urls import path
from .views import (
    show_shop_categories_list, show_category_detail ,
    )


urlpatterns = [
    # Lista categorie
    path("categories/", show_shop_categories_list, name='shop_categories_list'),
    path("category/<slug:slug>/", show_category_detail, name='shop_category_detail'),
     
]