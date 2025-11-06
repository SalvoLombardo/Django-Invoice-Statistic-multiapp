# shop/models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255)
    # Lo slug è una versione del nome trasformata in una stringa adatta 
    # per essere usata in un URL (senza spazi, caratteri speciali, maiuscole, ecc.).
    # Django utilizza il campo SlugField, che si assicura che lo slug sia valido
    # e privo di caratteri non ammessi negli URL.
    #
    # In questo caso lo slug viene creato automaticamente per generare 
    # una parte dell’URL leggibile e “pulita”.
    # Questo permette di creare pagine dinamiche e modulari.
    #
    # Esempio: una categoria con nome "Pantaloni Donna" avrà slug "pantaloni-donna",
    # e potrà quindi essere raggiunta all’URL:
    #     /shop/category/pantaloni-donna
    #
    # In un template potrà anche essere usato direttamente nei link Django, ad esempio:
    #     {% url 'category_detail' category.slug %}
    # In questo modo andrà a cercare path('category_detail/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail')
    # negli urls.py. 
    # IMPORTANTE:   
    #           Bisogna passare lo slug come attributo della funzione in modo da tornarlo all'HTML
    #           class CategoryDetailView(View):
    #                def get(self, request, slug):
    #                category = get_object_or_404(Category, slug=slug)
    #                return render(request, 'shop/category_detail.html', {'category': category})
    # Routing del segnale : Si accede ad un endpoin che genera 
    
    slug = models.SlugField(unique=True, blank=True) 
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    created_at = models.DateField(default=timezone.now)
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    #FK
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.color})"


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    #FK
    client = models.ForeignKey("users.Client", on_delete=models.CASCADE, related_name="carts")


    def __str__(self):
        return f"Cart #{self.id} for {self.client}"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)


    #FK
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PAID", "Paid"),
            ("SHIPPED", "Shipped"),
            ("DELIVERED", "Delivered"),
            ("CANCELLED", "Cancelled"),
        ],
        default="PENDING",
    )

    #FK
    client = models.ForeignKey("users.Client", on_delete=models.CASCADE, related_name="orders")


    def __str__(self):
        return f"Order #{self.id} - {self.client} - {self.status}"


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    
    #FK
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product} x {self.quantity}"


class Payment(models.Model):
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(
        max_length=30,
        choices=[
            ("CARD", "Credit/Debit Card"),
            ("CASH", "Cash"),
            ("PAYPAL", "PayPal"),
        ],
    )
    is_successful = models.BooleanField(default=False)


    #FK
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")

    def __str__(self):
        return f"Payment for {self.order} ({'OK' if self.is_successful else 'FAIL'})"


