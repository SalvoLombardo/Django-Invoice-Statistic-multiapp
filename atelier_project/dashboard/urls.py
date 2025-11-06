from django.urls import path
from .views import (
    dashboard_home, dashboard_shop_menu,
    dashboard_atelier_menu, dashboard_billing_menu, dashboard_shop_menu, 

    AddNewProductView,update_product_category_section, 
    update_product_product_section, 
    UpdateProductPage, AddNewCategoryView,

    invoice_create,invoice_detail,invoice_list,
    invoice_pdf_admin,invoice_update
)

urlpatterns = [
    #Dashboard Menu
    path("", dashboard_home, name="dashboard_home"),
    path("shop/",dashboard_shop_menu, name='dashboard_shop_menu'),
    path("atelier/", dashboard_atelier_menu, name="dashboard_atelier_menu"),
    #path("billing/", dashboard_billing_menu, name="dashboard_billing_menu"),
    path('invoices/', invoice_list, name='dashboard_invoice_list'),

    #Shop Section
    path("shop/add_new_product", AddNewProductView.as_view(),name='add_new_product'),
    path("shop/update_product_category/", update_product_category_section,name='update_product_category_section'),
    path("shop/update_product_product/<slug:slug>/", update_product_product_section,name='update_product_product_section'),
    path("shop/update_product_product/update_product_page/<int:pk>/", UpdateProductPage.as_view(),name='update_product_page'),
    path("shop/add_new_category", AddNewCategoryView.as_view(),name='add_new_category'),

    #Invoice section
    path('invoices/<int:pk>/', invoice_detail, name='dashboard_invoice_detail'),
    path('invoices/<int:pk>/edit/', invoice_update, name='dashboard_invoice_update'),
    path('invoices/new/', invoice_create, name='dashboard_invoice_create'),
    path('invoices/<int:pk>/pdf/', invoice_pdf_admin, name='dashboard_invoice_pdf'),

]

