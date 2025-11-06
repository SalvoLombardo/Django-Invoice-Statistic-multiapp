from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product, Cart,CartItem
from .forms import AddItemToCartForm
from django.views import View
from django.contrib import messages
#*******************************************************************************************************************************
# SHOP for Not-logged-in User
#*******************************************************************************************************************************
def show_shop_categories_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/categories_list.html', {'categories': categories})

def show_category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, stock__gt=0) #__gt: Queryset for greater then
    form=AddItemToCartForm()
    return render(request, 'shop/category_detail.html', {'category': category, 'products': products, 'form': form})


class AddItemToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        form = AddItemToCartForm(request.POST)
        product = get_object_or_404(Product, id=product_id)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            client=request.user.client_profile

            # Recupera o crea il carrello dell’utente
            cart, created = Cart.objects.get_or_create(client=client)

            # Se l’oggetto è già nel carrello, aggiorna la quantità
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, f"{product.name} aggiunto al carrello!")
            return redirect('shop_categories_list')  # o alla pagina che vuoi

        return redirect('homepage')
