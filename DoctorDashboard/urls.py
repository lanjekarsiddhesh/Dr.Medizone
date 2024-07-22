from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeDash, name="HomeDash"),
    path("AppointmentDash/", views.AppointmentDash, name="HomeDash"),
    path("AppointmentBillDash/", views.AppointmentBill, name="AppointmentBill"),
    path("Review/", views.Review, name="Review"),
    path("ViewReport/", views.ViewReport, name="ViewReport"),
    path("updatePending/<int:id>", views.updatePending, name="updatePending"),
    path("profile/", views.Profile, name="Profile"),
]