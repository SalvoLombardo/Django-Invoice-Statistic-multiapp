from django.urls import path
from .views import show_crochet_home

urlpatterns = [
    path('', show_crochet_home, name='crochet_dashboard'),
]