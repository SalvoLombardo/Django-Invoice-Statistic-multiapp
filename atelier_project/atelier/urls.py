from django.urls import path
from .views import BookAppointmentUserView, appointment_dashboard, AppointmentListUserView, AppointmentUpdateUserView, AppointmentDeleteUserView

urlpatterns = [
    path("appointment_dashboard/", appointment_dashboard, name="appointment_dashboard"),
    path("appointment_dashboard/book_appointment/", BookAppointmentUserView.as_view(), name="book_appointment_user"),
    path("appointment_dashboard/appointment_list_user/", AppointmentListUserView.as_view(), name="appointment_list_user"),
    path("appointment_dashboard/appointment_list_user/<int:pk>/update/", AppointmentUpdateUserView.as_view(), name="appointment_update_user"),
    path("appointment_dashboard/appointment_list_user/delete/<int:pk>/", AppointmentDeleteUserView.as_view(), name="appointment_delete_user"),

]