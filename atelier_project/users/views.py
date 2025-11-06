from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm,ClientForm


from .models import Client

class RegisterClientView(View):
    template_name='user/register.html'

    def get(self, request):
        user_form= CustomUserCreationForm()
        client_form= ClientForm()
        return render(request,self.template_name,
                      {
                        "user_form":user_form,
                        "client_form": client_form
                       })

    def post(self, request):
        user_form= CustomUserCreationForm(request.POST)
        client_form= ClientForm(request.POST)

        if user_form.is_valid() and client_form.is_valid():

            user= user_form.save(commit=False)
            user.username= user.username.lower()
            user.save()

            client= client_form.save(commit=False)
            client.user=user
            client.save()

            login(request, user)

            return redirect ('homepage')
        
        return render(request,self.template_name,
                      {
                        "user_form":user_form,
                        "client_form": client_form
                       })
    
class LoginClientView(View):
    template_name='user/login_client.html'

    def get(self,request):
        login_form= AuthenticationForm()

        return render(request,self.template_name,{'login_form':login_form})
    
    def post(self,request):
        login_form=AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user=login_form.get_user()
            login(request,user)
            return redirect('homepage')
        
        return render(request,self.template_name,{'login_form':login_form})

def logout_view(request):
    logout(request)
    return redirect('homepage')

@login_required
def client_profile_dashboard_view(request):
    template_name = 'user/client_profile_dashboard.html'
    return render(request,template_name)



@login_required
def client_profile_mesuraments_table_view(request):

    template_name = 'user/client_mesuraments_table.html'
    
    # Ottieni l'utente attualmente loggato
    user = request.user

    # Query: recupera il record Client associato a questo utente
    try:
        client = Client.objects.get(user=user)
        misure = {
            "Testa": client.measurements_head,
            "Petto": client.measurements_chest,
            "Vita": client.measurements_waist,
            "Fianchi": client.measurements_hips,
            "Manica": client.measurements_sleeve
        }
    except Client.DoesNotExist:
        misure = None

    context = {
        "user": user,
        "misure": misure
    }

    return render(request, template_name, context)













