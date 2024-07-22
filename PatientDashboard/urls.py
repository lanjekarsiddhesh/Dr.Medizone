from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="PatientDash"),
    path("profile/", views.Profile, name="Profile"),
    path("DrAppointment/", views.DrAppointment, name="DrAppointment"),
    path("LabAppointment/", views.LabAppointment, name="LabAppointment"),
    path("FavouriteProduct/", views.FavouriteProduct, name="FavouriteProduct"),
    path("CancleWishListItem/", views.CancleWishListItem, name="CancleWishListItem"),
    path("LabCart/", views.LabCart, name="LabCart"),
    path("MedicineCart/", views.MedicineCart, name="MedicineCart"),
    path("DrReview/", views.DrReview, name="DrReview"),
    path("MediReview/", views.MediReview, name="MediReview"),
    path("report/", views.report, name="report"),
    path("order/", views.order, name="order"),
    path("cancleAP/<int:id>", views.cancleAP, name="cancleAP"),
]