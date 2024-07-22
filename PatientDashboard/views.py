from django.shortcuts import render, redirect
from DMZ.models import *
from django.http import HttpResponse, HttpResponseRedirect
from medicine.models.order import Orders
from medicine.models.cart import CartItem, cart
from medicine.models.favouriteProduct import wishlist, wishlistItem
from medicine.models.Review import Reviews
from django.contrib import messages

# Create your views here.
ProfileId = 0
def index(request):
    id = request.session.get('patient_id')
    Id = Patient.objects.get(patient_id=id)
    param = {'id':id,'Id':Id,}
    return render(request,'comman.html',param)

def order(request):
    id = request.session.get('patient_id')
    Id = Patient.objects.get(patient_id=id)
    Cart = cart.objects.get(patient=id)
    Order = Orders.objects.filter(Cart=Cart.id)
    OrderReceived = Orders.objects.filter(Cart=Cart.id,status='Order Received')
    Orderdelivered = Orders.objects.filter(Cart=Cart.id,status='Order delivered')
    param = {'id':id,'Id':Id,'Order':Order,'OrderReceived':OrderReceived,'Orderdelivered':Orderdelivered}
    return render(request,'orders.html',param)

def DrAppointment(request):
    id = request.session.get('patient_id')
    Id = Patient.objects.get(patient_id=id)
    appointment = Appointments.objects.filter(patient=id)
    appointmentClinic = Appointments.objects.filter(patient=id,Appointments_type='Personal meeting')
    appointmentHome = Appointments.objects.filter(patient=id,Appointments_type='Home visit')
    appointmentCancle = Appointments.objects.filter(patient=id,Cancelled=1)
    appointmentVideo = Appointments.objects.filter(patient=id,Appointments_type='Videocall meeting')
    if request.method == "POST":
        num = request.POST['num']
        cancleAP(request,num)
        messages.success(request, "your appointment is cancelled if you pay for this appointment then your payment will be return in seven days")
    param = {'id':id,'Id':Id,'appointmentCancle':appointmentCancle,'appointmentHome':appointmentHome,'appointment':appointment,'appointmentClinic':appointmentClinic,'appointmentVideo':appointmentVideo}
    return render(request,'Appointment.html',param)

def LabAppointment(request):
    id = request.session.get('patient_id')
    Id = Patient.objects.get(patient_id=id)
    appointment = diagnostic_appointment.objects.filter(patient=id)
    appointmentLab = diagnostic_appointment.objects.filter(patient=id,Appointments_type='Lab Visit')
    appointmentHome = diagnostic_appointment.objects.filter(patient=id,Appointments_type='Home visit')
    appointmentCancle = diagnostic_appointment.objects.filter(patient=id,Cancelled=1)

    if request.method == "POST":
        num = request.POST['num']
        LabcancleAP(request,num)
        messages.success(request, "your appointment is cancelled if you pay for this appointment then your payment will be return in seven days")

    param = {'id':id,'Id':Id,'appointmentCancle':appointmentCancle,'appointmentHome':appointmentHome,'appointment':appointment,'appointmentLab':appointmentLab}
    return render(request,'LabAppointment.html',param)

def FavouriteProduct(request):
    id = request.session.get('patient_id')
    Id = Patient.objects.get(patient_id=id)
    wishlists = wishlist.objects.get(patient=id) 
    WishId = wishlists.id
    item = wishlistItem.objects.filter(WishlistProduct=WishId)
    param = {'id':id,'Id':Id,"item":item}
    return render(request,'WishListProduct.html',param)

def LabCart(request):
     id = request.session.get('patient_id')
     Id = Patient.objects.get(patient_id=id)
     Digno_Cart = dignostic_test_cart.objects.get(patient = id)
     Digno_CartItem = dignostic_test_cartItems.objects.filter(carts=Digno_Cart.id,is_paid=False)
     total = []
     for i in Digno_CartItem:
            total.append(i.Tests.price)
     param = {'id':id,'Id':Id,"length":len(Digno_CartItem) ,'total':sum(total),'cart':Digno_CartItem}
     return render(request, 'LabCart.html',param )

def MedicineCart(request):
     id = request.session.get('patient_id')
     Id = Patient.objects.get(patient_id=id)
     Medi_Cart = cart.objects.get(patient = id)
     Medi_CartItem = CartItem.objects.filter(carts=Medi_Cart.id,is_paid=False)
     total = []
     for i in Medi_CartItem:
            total.append(i.Product.price)
     param = {'id':id,'Id':Id,"length":len(Medi_CartItem) ,'total':sum(total),'cart':Medi_CartItem}
     return render(request, 'MedicineCart.html',param )

def DrReview(request):
     id = request.session.get('patient_id')
     Id = Patient.objects.get(patient_id=id)
     rating = ReviewsRatings.objects.filter(patient = id)

     param = {'id':id,'Id':Id,'rating':rating}
     return render(request,'DoctorRating.html',param)

def MediReview(request):
     id = request.session.get('patient_id')
     Id = Patient.objects.get(patient_id=id)
     rating = Reviews.objects.filter(patient = id)

     param = {'id':id,'Id':Id,'rating':rating}
     return render(request,'MediReview.html',param)

def Profile(request):
    id = request.session.get('patient_id')
    Id = Patient.objects.get(patient_id=id)
    if request.method == "POST":
        name = request.POST['name']
        sex = request.POST['sex']
        blood = request.POST['blood']
        email = request.POST['email']
        mob = request.POST['mob']
        add = request.POST['add']
        cty = request.POST['cty']
        zip = request.POST['zip']
        area = request.POST['area']
        CN = request.POST['CN']
        State = request.POST['State']

        Patient.objects.filter(patient_id=id).update(patient_Blood=blood,patient_name=name,email=email,
                                patient_sex=sex,mobile=mob ,
                                patient_address=add,patient_city=cty,patient_state=State,patient_zip=zip,
                                patient_area=area,patient_country=CN)
        
        messages.success(request,"Updated Successfully !!!")
    param = {'id':id,'Id':Id}
    return render(request,'account.html',param)

def cancleAP(request,id):
    Appointments.objects.filter(Appointments_id=id).update(Cancelled=True)


def report(request):
     id = request.session.get('patient_id')
     Id = Patient.objects.get(patient_id=id)
     report = PatientReport.objects.filter(patient = id)
     param = {'id':id,'Id':Id,"file":report}
     return render(request,'Report.html',param)
    

def LabcancleAP(request,id):
    diagnostic_appointment.objects.filter(id=id).update(Cancelled=True)

def CancleWishListItem(request):
    iD = request.session.get('patient_id')
    id = request.GET.get('Wid')
    wish = wishlist.objects.get(patient=iD)
    wishlistItem.objects.filter(WishlistProduct=wish,Product=id).delete()
    return redirect(f'/PDashboard/FavouriteProduct/?id={iD}')


