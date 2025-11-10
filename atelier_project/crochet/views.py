from django.shortcuts import render

# Create your views here.
def show_crochet_home(request):
    return render(request,'crochet/crochet_dashboard.html')