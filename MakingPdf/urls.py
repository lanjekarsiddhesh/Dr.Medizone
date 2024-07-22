from django.contrib import admin
from django.urls import path
from . import views
# from django.conf import settings

#html file path here
urlpatterns = [
    path("", views.AppointmnetPdf, name="AppointmnetPdf"),
    path("Medicine/<str:id>", views.MedicinePdf, name="MedicinePdf"),
    path("create/<int:id>", views.render_pdf, name="render_pdf"),
    path("Lab_Appointment_pdf/<int:id>", views.Lab_render_pdf, name="Lab_render_pdfs"),
    path("createMedicine/", views.Medicine_render_pdf, name="Medicine_render_pdf"),
               ]