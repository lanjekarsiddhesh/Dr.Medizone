
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render , redirect
from random import randint
from ..forms import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from math import *
from ..models import *
from .Daignostic import DignoFetchItems
from .mail import send_mail
from .Doctor import update_Dr_loginDetails
from .patient import user


patient = Patient.objects.all()
patient_file_attr = user()
# OtpVerify = ''
Users = ''
user_name = ''
Model = ''

def get_all_db():
    patient = Patient.objects.all()
    doctor = Doctor.objects.all()
    appointment = Appointments.objects.all()
    specialist = specilaity.objects.all()
    Dr_length = len(doctor)
    length = len(specialist)
    appointment_length = len(appointment)

def generate_otp(request):
    otp_num = randint(1000,9999)
    otp = str(otp_num)
    request.session['otp'] = otp
    request.session.set_expiry(60)
    print("This is your otp: ", request.session.get('otp'))
    return otp
    
def index(request):
    login = request.session.get('patient_status')
    Doctor_status = request.session.get('Doctor_status')
    patient_id = request.session.get('patient_id')
    Doctor_id = request.session.get('Doctor_id')
    
    # aii = get_all_db()
    doctor = Doctor.objects.all()
    Dr_length = len(doctor)
    slides = Dr_length//4 + ceil((Dr_length/4)-(Dr_length//4))
    # Dr_param =  {'range':range(length),'doctor':doctor}
    patient = Patient.objects.all()
    specialist = specilaity.objects.all()
    length = len(specialist)
    #appointment
    appointment = Appointments.objects.all()
    appointment_length = len(appointment)
    #digno
    tests = diagnostic_test_list.objects.all()
    test_length = len(tests)
            
    param = {"Doctor_status":Doctor_status,"Doctor_id":Doctor_id,"patient_id":patient_id,"login":login,"patient":patient,"appointment_length":appointment_length,"test_length":test_length,"specialist_length":length,"no_of_slides":slides, "slide_range": range(1,slides) ,'Dr_length':Dr_length,'Range':range(Dr_length),'range': range(length), 'specialists':specialist,'doctor':doctor}
    return render(request,'index.html',param)

@csrf_exempt
def success(request):
    payment = request.POST
    order_d = request.GET.get('order')
    for key, val in payment.items():
        order_id = ""
        # payment_id = ""
        # razorpay_signature = ""
        if key == 'razorpay_order_id':
            order_id += val
            bill = Bill.objects.filter(order_id= order_id).first()
            Dignobill = DignoBill.objects.filter(Orders_id= order_id).first()
            Digno_Cart = DignoFetchItems(request)
            cartItem = dignostic_test_cartItems.objects.filter(carts=Digno_Cart.id,is_paid=False)
            for i in cartItem:
                dignostic_test_cartItems.objects.filter(Tests=i.Tests.id,carts=Digno_Cart.id,is_paid=False).update(is_paid=True,order=order_d)
            try:
                appointments = Appointments.objects.get(order_id=order_id)
            except:
                Digno = diagnostic_appointment.objects.get(order_id=order_id)

        if key == 'razorpay_payment_id':
            payment_id = val

        if key == 'razorpay_signature':
            razorpay_signature = val

    # bill.paid = True
    if bill:
        bill.Payment_id = payment_id
        bill.signature =razorpay_signature
        bill.appointments=appointments
        bill.payment_status = True
        bill.save()
        redirect(f'/MakingPdf/create/{bill.appointments.Appointments_id}')

    if Dignobill:
        Dignobill.Payment_id = payment_id
        Dignobill.signature = razorpay_signature
        Dignobill.Test = Digno
        Dignobill.save()
    messages.success(request, "your appointment is booked others details send on entered mobile number")
    return render(request,'success.html')

def otp_fun(request):
    
    if request.method == "POST":
        one = request.POST['Oneotp']
        two = request.POST['Twootp']
        three = request.POST['Threeotp']
        four = request.POST['Fourotp']
        # otp = request.POST['otp']
        otp = one+two+three+four
        
        if request.session.get('otp') == otp:
            print("Match")
            return redirect('/changePass/')
        else:
            print("dosen't match")
            return redirect('/otp/')
    return render(request,'otp2.html',{"check":request.session.get('otp')})

def resend_otp(request):
    generate_otp(request)
    send_mail(user=user_name,OtpVerify=request.session.get('otp'))
    return redirect('/otp/')

def review(request,doctor_id):
    # retrive information from db
    Doctor_status = request.session.get('Doctor_status')
    doctor = Doctor.objects.filter(doctor_id=doctor_id)
    patient_id = request.session.get('patient_id')
    login = request.session.get('patient_status')

    if request.method == "POST":
        Type = request.POST["Type"]
        Health_concern = request.POST["Health_concern"]
        subject = request.POST["subject"]
        experience = request.POST["experience"]
        YES_NO = request.POST["YES_NO"]
        rating = request.POST["rating"]

        data = ReviewsRatings(appointment_type=Type,health_concern=Health_concern,subject=subject,
        review=experience,rating=rating,recommend_doctor=YES_NO,doctorId_id=doctor_id,patient_id=patient_id)
        data.save()

    overall_star(doctor_id)

    return render(request, "Review.html",{"Doctor_status":Doctor_status,'doctor':doctor[0],"Id":patient_id,"login":login,})

def loginError(request, userName, password, flag ):
    if userName == '' and password == '':
        messages.error(request, "enter username and password first")
                
    elif userName == '' :
        messages.error(request, "enter username first")       

    elif password == '':
        messages.error(request, "enter password first")

    elif userName == False:
        messages.error(request, "wrong username ")
                
    elif flag == False:
        messages.error(request, "wrong password ")
                  
def Login(request):
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login, logout
            #collect password & username by user
        userName = request.POST['userD']
        password = request.POST['PassD']
        login_user = request.POST['sid']

        if login_user == "admin":
            user_obj = authenticate(username= userName, password = password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/Admin_dash/')
            else:
                messages.error(request, "Either Username or Password Wrong OR You are not login")
                return render(request,'login.html')

        elif login_user == "doctor":
            # fetch data from username through db
            Dr = Doctor.get_doctor_by_username(userName)
            
            if Dr:
                # check password from db
                flag = check_password(password,Dr.password)
                if flag:
                    update_Dr_loginDetails(Dr)
                    Doctor.objects.filter(doctor_id=Dr.doctor_id).update(status="Login")
                    request.session['Doctor_id'] = Dr.doctor_id
                    request.session['Doctor_username'] = Dr.doctor_userName
                    request.session['Doctor_status'] = "Login"
                    print(request.session.get('Doctor_status'))
                    return redirect(F"/DDashboard/?Doctor_id={Dr.doctor_id}")
                else:
                    loginError(request, userName, password,  flag )
                    return render(request,'login.html')
            else:
                loginError(request, userName, password, flag=False )

        elif login_user == "patient":
                # fetch data from username through db
            patient = Patient.get_patient_by_username(userName)
            
            if patient:
                # check password from db
                flag = check_password(password,patient.password)
                if flag:
                    # update and create Doctor_login table
                    patient_file_attr.update_Patient_loginDetails(patient)
                    Patient.objects.filter(patient_id=patient.patient_id).update(status="Login")
                    print(patient)
                    request.session['patient_id'] = patient.patient_id
                    request.session['patient_username'] = patient.patient_userName
                    request.session['patient_status'] = "Login"
                    
                    return redirect(F"/PDashboard/DrAppointment/?patient_id={patient.patient_id}")
                else:
                    loginError(request, userName, password, flag )
                    return render(request,'login.html')
            else:
                loginError(request, userName, password, flag=False )

    return render(request,'login.html',{"Id":Id,"login":login,})

# ------------------------------------------------------------pecialist----------------------------------------------------------------------------------

def specialist(request):
    Doctor_status = request.session.get('Doctor_status')
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    specialist = specilaity.objects.all()
    patient_id = request.session.get('patient_id')
    Doctor_id = request.session.get('Doctor_id')
    length = len(specialist)
    param = {"Doctor_status":Doctor_status,"Doctor_id":Doctor_id,"patient_id":patient_id,"Doctor_status":Doctor_status,"Id":Id,"login":login,"patient":patient,'range': range(length), 'specialists':specialist}
    return render(request,'specialist.html',param)

# --------------------------------------------contact--------------------------------------------------------------------------------

def contact_us(request):
    Doctor_status = request.session.get('Doctor_status')
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    if request.method == "POST":
        Name = request.POST['name']
        Email = request.POST['email']
        Subject = request.POST['subject']
        Messages = request.POST['message']

        data =  Contact_us(Name=Name,Email=Email,Subject=Subject,Message=Messages)
        data.save()
        messages.success(request,"Your suggestion send successfully")
    return render(request,'contact_us.html',{"Doctor_status":Doctor_status,"Id":Id,"patient_id":Id,"login":login,})

def FAQ(request):
    FAQ = QNA.objects.all()
    login = request.session.get('patient_status')
    patient_id = request.session.get('patient_id')
    Doctor_status = request.session.get('Doctor_status')
    Id = request.session.get('patient_id')
    if request.method == "POST":
        Email = request.POST['Email']
        Question = request.POST['Question']

        Data = QNA(Question=Question,Email=Email,patient_id=Id)

        Data.save()
        messages.success(request, f"Send answer of your question in 24 hours on your this {Email} email address")
    
    return render(request,'FAQ.html',{"Doctor_status":Doctor_status,"patient_id":patient_id,"Id":Id,"login":login,'FAQ':FAQ})

def About(request):
    login = request.session.get('patient_status')
    Doctor_status = request.session.get('Doctor_status')
    Id = request.session.get('patient_id')
    return render(request,'About_us.html',{"Doctor_status":Doctor_status,"Id":Id,"patient_id":Id,"login":login,})

def Service(request):
    login = request.session.get('patient_status')
    Doctor_status = request.session.get('Doctor_status')
    Id = request.session.get('patient_id')
    return render(request,'service.html',{"Doctor_status":Doctor_status,"Id":Id,"login":login,})

def Department(request):
    specialist = specilaity.objects.all()
    patient_id = request.session.get('patient_id')
    length = len(specialist)
    login = request.session.get('patient_status')
    Doctor_status = request.session.get('Doctor_status')
    Id = request.session.get('patient_id')
    param = {"Doctor_status":Doctor_status,'range': range(length),"patient_id":patient_id, 'specialists':specialist,"Id":Id,"login":login,}
    return render(request,'department.html',param)

# -----------------------------------------------------------------Tele--------------------------------------------------------------------------------------------

def Tele(request):

    return render(request,'Tele.html')

# -----------------------------------------------------------Admin------------------------------------------------------------------------------------

def Logout(request):
    id = request.GET.get('id')
    try:
        Patient.objects.filter(patient_id=id).update(status="Logout")
        Doctor.objects.filter(doctor_id=id).update(status="Logout")
    except:
        messages.success(request,"Logout Successfully")
        return redirect('/Login/')
    request.session.clear()
    messages.success(request,"Logout Successfully")
    
    return redirect('/Login/')
    
