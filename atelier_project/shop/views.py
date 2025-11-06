from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product


#*******************************************************************************************************************************
# SHOP for Not-logged-in User
#*******************************************************************************************************************************
def show_shop_categories_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/categories_list.html', {'categories': categories})

def show_category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category_detail.html', {'category': category, 'products': products})

