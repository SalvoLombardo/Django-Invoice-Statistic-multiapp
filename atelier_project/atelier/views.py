from django.shortcuts import render, redirect, get_object_or_404
from django.views import View 


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookAppointmentUserForm
from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import Appointment




@login_required
def appointment_dashboard(request):
    template_name = 'atelier/appointment_dashboard.html'
    return render(request,template_name)

#------------
# CREATE APPOINTMENT
# -----------        
class BookAppointmentUserView(LoginRequiredMixin, View):
    template_name = 'atelier/book_appointment_user.html'  # aggiungi .html alla fine!

    def get(self, request):
        form = BookAppointmentUserForm()
        return render(request, self.template_name, {'book_appointment_form': form})

    def post(self, request):
        form = BookAppointmentUserForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user.client_profile  # o come lo gestisci tu

            try:
                appointment.save()
                messages.success(request, "Appuntamento prenotato con successo!")
                return redirect("appointment_dashboard")

            except ValidationError as e:
                # Qui catturiamo l’errore e lo mostriamo nel form
                form.add_error(None, e.message_dict.get("__all__", e.messages))

        return render(request, self.template_name, {'book_appointment_form': form})
    
#------------
# SHOW APPOINTMENT
# -----------        
class AppointmentListUserView(LoginRequiredMixin,View):
    template_name='atelier/appointment_list_user.html'

    def get (self, request):
        appointments=Appointment.objects.filter(client=request.user.client_profile)
        return render(request, self.template_name,{'appointments':appointments})
    
#------------
# UPDATE APPOINTMENT
# -----------        
class AppointmentUpdateUserView(LoginRequiredMixin, View):
    template_name = 'atelier/appointment_update_user.html'

    def get(self, request, pk):
        
        appointment = get_object_or_404(Appointment, pk=pk, client=request.user.client_profile)
        form = BookAppointmentUserForm(instance=appointment)
        return render(request, self.template_name, {'form': form, 'appointment': appointment})
        

    def post(self, request, pk):
        #qui su appointment facciamo una query per ottenere un oggetto Appointment,
        #con pk (primary key) che si trova nella richiesta HTTP e passato tramite URL
        #associato al client che riguarda user.client profile (id del cliente)
        #Equivale a flask --> appointment = Appointment.query.filter_by(id=pk, client_id=current_user.id).first_or_404()
        appointment = get_object_or_404(Appointment, pk=pk, client=request.user.client_profile)

        # qui passiamo il form BookAppointmentUserForm e lo riutilizziamo poichè lasciamo tutto
        #invariato ma usando "instance=appointment" gli diciamo "le modifiche si fanno sull'oggetto
        # appointment quindi non sono inserimenti ma modifiche".
        #In questo modo non facciamo un inserimento ma un update.
        form = BookAppointmentUserForm(request.POST, instance=appointment)
        if form.is_valid():
            try:
                form.save()
                return redirect('appointment_list_user')
            

            except ValidationError as e:
                # Qui catturiamo l’errore e lo mostriamo nel form
                form.add_error(None, e.message_dict.get("__all__", e.messages))
                
        return render(request, self.template_name, {'form': form, 'appointment': appointment})

#------------
# DELETE APPOINTMENT
# -----------        
class AppointmentDeleteUserView(LoginRequiredMixin, View):
    template_name = 'atelier/appointment_delete_user.html'

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, client=request.user.client_profile)
        return render(request, self.template_name, {'appointment': appointment})

    def post(self, request, pk):

        appointment = get_object_or_404(Appointment, pk=pk, client=request.user.client_profile)
        appointment.delete()
        messages.success(request, "Appuntamento eliminato con successo.")
        return redirect('appointment_list_user')


