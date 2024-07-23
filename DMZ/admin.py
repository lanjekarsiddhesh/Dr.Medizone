from django.contrib import admin
from .models import *
# Register your models here for show db in admin pannel. 
class adminReview(admin.ModelAdmin):
    list_display = ['id', 'rating', 'health_concern','appointment_type','recommend_doctor','patient','doctorId','review','created_at','Updated_at']

class adminAppointment(admin.ModelAdmin):
    list_display = ['Appointments_date','Appointments_time','Appointments_type','Doctor_id']

class adminBill(admin.ModelAdmin):
    list_display = ['Bill_number','order_id','appointments','payment_status','Bill_date']


admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(specilaity)
admin.site.register(Appointments,adminAppointment)
admin.site.register(Doctor_login)
admin.site.register(Patient_login)
admin.site.register(Bill,adminBill)
admin.site.register(homeCare_page)
admin.site.register(homeCare)
admin.site.register(Tele)
admin.site.register(QNA)
admin.site.register(diagnostic_test_list)
admin.site.register(combo_diagnostic_test_list)
admin.site.register(dignostic_test_cart)
admin.site.register(dignostic_test_cartItems)
admin.site.register(diagnostic_appointment)
admin.site.register(Lab)
admin.site.register(Contact_us)
admin.site.register(PatientReport)
admin.site.register(ReviewsRatings,adminReview)