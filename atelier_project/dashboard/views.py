from .forms import AddNewCategoryAdmin, AddOrUpdateNewProductAdmin
from shop.models import Category, Product

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from billing.models import Invoice
from .forms import InvoiceAdminForm

from users.decorators import admin_required
from users.mixins import AdminRequiredMixin

from django.core.cache import cache

######Import for statistics section
from django.utils import timezone
from datetime import timedelta
from shop.models import Order
from shop.forms import DateRangeForm
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models.functions import TruncDate
from django.db.models import Sum




import matplotlib
matplotlib.use('Agg')  # Usa backend non interattivo
import matplotlib.pyplot as plt

#*******************************************************************************************************************************
# DASHBOARD MENU
#*******************************************************************************************************************************

@admin_required
def dashboard_home(request):
    
    return render(request, 'dashboard/home.html')



@admin_required
def dashboard_atelier_menu(request):
    
    return render(request, 'dashboard/atelier_menu.html')

@admin_required
def dashboard_billing_menu(request):
    
    return render(request, 'dashboard/billing_menu.html')







#*******************************************************************************************************************************
# SHOP for Admin
#*******************************************************************************************************************************
@admin_required
def dashboard_shop_menu(request):
    
    return render(request,'dashboard/dashboard_shop_menu.html')

#----------------------------------
# CREATE Category section (admin)
class AddNewCategoryView(AdminRequiredMixin, View):
    template_name='dashboard/add_new_category.html'
    def get(self, request):
        
        form= AddNewCategoryAdmin()
        return render(request,self.template_name, {'form':form})

    def post(self, request):
        
        
        form= AddNewCategoryAdmin(request.POST)
        if form.is_valid():
            product= form.save(commit=False)
            product.save()
            cache.delete('shop_categories')
            cache.delete('admin_categories')
            messages.success(request,'Hai aggiunto la nuova categoria con successo')
            return redirect('dashboard_shop_menu')
        
        messages.error(request, ' Qualche cosa è andato storto, riprova')
        return render(request,self.template_name, {'form':form})

#----------------------------------
# UPDATE Product section (admin)
class AddNewProductView(AdminRequiredMixin,View):
    template_name='dashboard/add_new_product.html'
    
    def get(self, request):
        
        form= AddOrUpdateNewProductAdmin()
        return render(request,self.template_name, {'form':form})

    def post(self, request):
        
        
        form= AddOrUpdateNewProductAdmin(request.POST)
        if form.is_valid():
            product= form.save(commit=False)
            product.save()
            cache.delete('shop_categories')
            cache.delete(f'category_{product.category.slug}')
            messages.success(request,'Hai aggiunto il nuovo prodotto con successo')
            return redirect('dashboard_shop_menu')
        
        messages.error(request, ' Qualche cosa è andato storto, riprova')
        return render(request,self.template_name, {'form':form})

#----------------------------------
# UPDATE Product section (admin)
class UpdateProductPage(AdminRequiredMixin, View):
    template_name = 'dashboard/update_product_page.html'

    def get(self, request, pk):
        
        product = get_object_or_404(Product, pk=pk)
        form = AddOrUpdateNewProductAdmin(instance=product)
        return render(request, self.template_name, {'form': form, 'product': product})
    
    def post(self, request, pk):
        
        product = get_object_or_404(Product, pk=pk)
        form = AddOrUpdateNewProductAdmin(request.POST, instance=product)
        if form.is_valid():
            form.save()
            cache.delete('shop_categories')
            cache.delete(f'category_{product.category.slug}')
            messages.success(request, f'Prodotto "{product.name}" aggiornato con successo.')
            return redirect('dashboard_shop_menu')
        else:
            messages.error(request, 'Errore durante l’aggiornamento del prodotto.')
            return render(request, self.template_name, {'form': form, 'product': product})


@admin_required
def update_product_category_section(request):
    categories = cache.get('admin_categories')
    if categories is None:
        categories = list(Category.objects.all())
        cache.set('admin_categories', categories, 60 * 60)  # 1 ora
    return render(request, 'dashboard/update_product_category_section.html', {'categories': categories})

@admin_required
def update_product_product_section(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'dashboard/update_product_product_section.html', {'category': category, 'products': products})




#*******************************************************************************************************************************
# INVOICE Section
#*******************************************************************************************************************************

@admin_required
def invoice_list(request):
    invoices = cache.get('invoice_list')
    if invoices is None:
        invoices = list(Invoice.objects.all().order_by('-date'))
        cache.set('invoice_list', invoices, 30 * 60)  # 30 min
    return render(request, 'dashboard/invoices/invoice_list.html', {'invoices': invoices})


@admin_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'dashboard/invoices/invoice_detail.html', {'invoice': invoice})


@admin_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceAdminForm(request.POST)
        if form.is_valid():
            form.save()
            cache.delete('invoice_list')
            return redirect('dashboard_invoice_list')
    else:
        form = InvoiceAdminForm()
    return render(request, 'dashboard/invoices/invoice_form.html', {'form': form})


@admin_required
def invoice_update(request, pk):
    
    
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceAdminForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            cache.delete('invoice_list')
            return redirect('dashboard_invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceAdminForm(instance=invoice)
    return render(request, 'dashboard/invoices/invoice_form.html', {'form': form})


@admin_required
def invoice_pdf_admin(request, pk):
    
    
    invoice = get_object_or_404(Invoice, pk=pk)
    
    return invoice.generate_pdf()

        



#*******************************************************************************************************************************
# STATISTICS Section
#*******************************************************************************************************************************


@admin_required
def analytics_view(request):
    #Creating some default data just to be sure
    start_date = timezone.now() - timedelta(days=30)
    end_date = timezone.now()

    form = DateRangeForm(request.GET or None)

    if form.is_valid():
        #Getting the real date
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

    # Cache key basata sulle date selezionate
    cache_key = f'analytics_{start_date.strftime("%Y%m%d")}_{end_date.strftime("%Y%m%d")}'
    cached = cache.get(cache_key)

    if cached:
        context = cached
        context['form'] = form
        return render(request, 'dashboard/analytics/dashboard_analytics.html', context)

    # We can use Django lookup,

    # __date is refferring to just 'date' with no time like 22-01-2025(exclute 08:00am)
    # so we're filtering just by date and not time

    # __range indicate to use a range between theese two date
    #orders became an ORM object that in our case needs to 'put order'

    # 'orders' became a queryset where we have every elements wich rappresents a row in a table
    orders = Order.objects.filter(
        status="PAID",
        created_at__date__range=(start_date, end_date)
    )


    #In daily sales we are aggregating the results that we have in 'orders'
    # taking the queryset 'orders' we are saying the we want a new field called day (annotate(day=...)
    # the queryset now become a series of a dict with 'day' as key.
    # the data that referrs to day  will be truncated with truncDAte (TruncDate('created_at')))
    # then order by the value of the key 'day'
    # the we create a new field called total with annotate(total=Sum('total'))
    # so the result will be a list of a dict with 2 keys 'day' and 'total'
    #
    # In this way we obtain every total order by date and now we can create the statistic form
    # to see every single date's data
    ######SQL translation
    #SELECT DATE(created_at) AS day, SUM(total) AS total (* Important: As day and AS total are one of the main concepts)
    #FROM orders
    #GROUP BY DATE(created_at)
    #ORDER BY DATE(created_at);

    daily_sales = (
        orders.annotate(day=TruncDate('created_at')).values('day').order_by('day').annotate(total=Sum('total'))
    )

    # Dividing days from totals
    days = [item['day'] for item in daily_sales]
    totals = [item['total'] for item in daily_sales]

    # Creating the statistic graph
    fig, ax = plt.subplots()
    ax.plot(days, totals, marker='o')
    ax.set_title('Daily sales')
    ax.set_xlabel('Data')
    ax.set_ylabel('Totale (€)')
    plt.tight_layout()

    # Converting in Base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    graphic = base64.b64encode(image_png).decode('utf-8')

    context = {
        'graphic': graphic,
        'total_orders': orders.count(),
        'total_sales': sum(order.total for order in orders),
    }

    # Cache per 1 ora (grafico + totali)
    cache.set(cache_key, context, 60 * 60)

    context['form'] = form
    return render(request, 'dashboard/analytics/dashboard_analytics.html', context)



