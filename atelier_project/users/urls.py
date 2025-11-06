from django.urls import path
from .views import RegisterClientView, LoginClientView, logout_view, client_profile_dashboard_view, client_profile_mesuraments_table_view

urlpatterns = [
    path("register/", RegisterClientView.as_view(), name="register_client"),
    path("login_client/", LoginClientView.as_view(), name='login_client'),
    path("logout/", logout_view, name='logout'),

    path("client_profile_dashboard/", client_profile_dashboard_view, name='client_profile_dashboard'),
    path("client_profile_dashboard/client_mesuraments_table", client_profile_mesuraments_table_view, name='client_mesuraments_table'),

]