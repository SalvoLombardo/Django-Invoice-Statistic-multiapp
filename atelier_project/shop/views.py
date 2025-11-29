from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product, Cart,CartItem, Order, OrderItem
from .forms import AddItemToCartForm, ConfirmCartForm
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

            # Get or create cart, if it will be created, the created variable
            # will be True, 
            # Filter by if the cart is active
            cart, created = Cart.objects.get_or_create(
                client=client,
                is_active = True,
                defaults={}
                
                )

            # Same thing but we search by cart, products
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                new_quantity = cart_item.quantity + quantity
            else:
                new_quantity = quantity

            # check if there are enough items in stock
            # i cannot use something like :
            # return self.get(request) -> to call again the get section
            # because this view has no get section, so i have to recreate the get funcition
            # like the view (function) above :
            # def show_category_detail(request... ecc
            if product.stock < new_quantity:
                messages.error(request, f"Attenzione: solo {product.stock} pezzi disponibili di {product.name}.")
                category = product.category
                products = Product.objects.filter(category=category, stock__gt=0)
                form = AddItemToCartForm()
                return render(request, 'shop/category_detail.html', {
                    'category': category,
                    'products': products,
                    'form': form
    })

            
            cart_item.quantity = new_quantity
            cart_item.save()

            
            product.stock -= quantity
            product.save()

            messages.success(request, f"{product.name} added to cart!")
            return redirect('shop_categories_list')

        return redirect('homepage')
    

class CartDashboardView(LoginRequiredMixin, View):
    template_name = 'shop/cart_dashboard.html'

    def get(self, request):
        client = request.user.client_profile

        
        carts = Cart.objects.filter(client=client, is_active=True).first()

        
        if not carts:
            return render(request, self.template_name, {'cart': None, 'cart_items': []})

        # Recuperiamo direttamente gli item collegati
        cart_items = carts.items.all()  # grazie al related_name="items"

        return render(request, self.template_name, {
            'carts': carts,
            'cart_items': cart_items
        })
    

    def post(self, request):
        form_confirm= ConfirmCartForm(request.POST)
        if form_confirm.is_valid():


            client = request.user.client_profile
            cart = Cart.objects.filter(client=client, is_active=True).first()

            if not cart or not cart.items.exists():
                messages.error(request, "Il carrello è vuoto!")
                return redirect('cart_dashboard')

            
            order = Order.objects.create(
                client=client,
                total=cart.total_price(),
                status="PENDING"
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            
            cart.is_active = False
            cart.save()

            messages.success(request, "Ordine confermato con successo!")
            return redirect('homepage')
        
        
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, self.template_name, {
            "cart_items": cart_items,
            "form_confirm": form_confirm,
        })


class DeactivateCartView(LoginRequiredMixin, View):
    template_name='shop/deactivate_cart.html'


    def post(self,request,pk):
        cart=get_object_or_404(Cart, pk=pk, client=request.user.client_profile)
        
        

        for item in cart.items.all():
                product=item.product
                product.stock+=item.quantity
                product.save()

        cart.is_active=False
        cart.save()
        

        messages.success(request,'Carrello cancellato')
        return redirect ('cart_dashboard')
