from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session  
from DMZ.models import *
from datetime import datetime
from datetime import date
from DMZ.views.mail import send_mail
from django.contrib import messages
import time
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
# Create your views here.



def HomeDash(request):
    id = request.GET.get('Doctor_id')
    Id = Doctor.objects.get(doctor_id=id)
    print(date.today())

    now = datetime.now()
    hour = now.hour
    greet = None

    print(hour)

    if hour < 12:
        greet = "Good Morning"
    elif hour < 16:
        greet = "Good Afternoon"
    else:
        greet = "Good Evening"

    next_appointment = Appointments.objects.filter(Doctor_id=id,appointment_status="pending",Appointments_date="2023-01-13")
    print(next_appointment)



    appointment = Appointments.objects.filter(Doctor_id=id)
    Clinic = Appointments.objects.filter(Doctor_id=id, Appointments_type="Personal meeting")
    Video = Appointments.objects.filter(Doctor_id=id, Appointments_type="Videocall meeting")
    Home = Appointments.objects.filter(Doctor_id=id, Appointments_type="Home visit")

    # Pendingappointment = Appointments.objects.filter(Doctor_id=id,appointment_status="pending",Appointments_date=date.today())
    Pendingappointment = Appointments.objects.filter(Doctor_id=id,appointment_status="pending")
    PendingClinic = Appointments.objects.filter(Doctor_id=id, Appointments_type="Personal meeting", appointment_status="pending")
    PendingVideo = Appointments.objects.filter(Doctor_id=id, Appointments_type="Videocall meeting", appointment_status="pending")
    PendingHome = Appointments.objects.filter(Doctor_id=id, Appointments_type="Home visit", appointment_status="pending")

    Fulllength = len(appointment)
    Clinicength = len(Clinic)
    Videolength = len(Video)
    Homelength = len(Home)

    PendingFulllength = len(Pendingappointment)
    PendingClinicength = len(PendingClinic)
    PendingVideolength = len(PendingVideo)
    PendingHomelength = len(PendingHome)

    
    param = {"greet":greet,"Id":id,'id':Id,"appointment":appointment,"time":datetime.today().strftime("%I:%M %p"),"Fulllength":Fulllength,
             "Home":Homelength,"Video":Videolength,"Clinic":Clinicength,"PendingFulllength":PendingFulllength,"PendingClinicength":PendingClinicength,"PendingVideolength":PendingVideolength,
             "PendingHomelength":PendingHomelength,"Pendingappointment":Pendingappointment}
    return render(request,'DoctorHome.html',param)

def ViewReport(request):
    id = request.GET.get('Doctor_id')
    Id = Doctor.objects.get(doctor_id=id)
    myFile = PatientReport.objects.all()
    return render(request,'report.html',{'myFile':myFile,"Id":id,'id':Id,})

def AppointmentDash(request):
    id = request.GET.get('Doctor_id')
    Id = Doctor.objects.get(doctor_id=id)
    print(request.session.get('Doctor_status'))

    myform = MyFileForm()

    appointment = None
    Clinic = None
    Video = None
    Home = None
    Canclled = Appointments.objects.filter(Doctor_id=id, Cancelled=True)

    status = request.GET.get('status')
    if status:
        appointment = Appointments.objects.filter(Doctor_id=id,appointment_status=status)
        Clinic = Appointments.objects.filter(Doctor_id=id, Appointments_type="Personal meeting",appointment_status=status)
        Video = Appointments.objects.filter(Doctor_id=id, Appointments_type="Videocall meeting",appointment_status=status)
        Home = Appointments.objects.filter(Doctor_id=id, Appointments_type="Home visit",appointment_status=status)
    else:
        appointment = Appointments.objects.filter(Doctor_id=id)
        Clinic = Appointments.objects.filter(Doctor_id=id, Appointments_type="Personal meeting")
        Video = Appointments.objects.filter(Doctor_id=id, Appointments_type="Videocall meeting")
        Home = Appointments.objects.filter(Doctor_id=id, Appointments_type="Home visit")

    Pendingappointment = Appointments.objects.filter(Doctor_id=id,appointment_status="pending")
    PendingClinic = Appointments.objects.filter(Doctor_id=id, Appointments_type="Personal meeting", appointment_status="pending")
    PendingVideo = Appointments.objects.filter(Doctor_id=id, Appointments_type="Videocall meeting", appointment_status="pending")
    PendingHome = Appointments.objects.filter(Doctor_id=id, Appointments_type="Home visit", appointment_status="pending")

    

    Fulllength = len(appointment)
    Clinicength = len(Clinic)
    Videolength = len(Video)
    Homelength = len(Home)

    PendingFulllength = len(Pendingappointment)
    PendingClinicength = len(PendingClinic)
    PendingVideolength = len(PendingVideo)
    PendingHomelength = len(PendingHome)

    if request.method == "POST":
        MyForms = MyFileForm(request.POST,request.FILES)

        try:
            patient_name = request.POST['name']
            patient_time = request.POST['time']
            patient_email = request.POST['Pemail']
            doctor_email = request.POST['Demail']
            text = f'''
            I am writing to inform you that I need to reschedule our appointment that was scheduled for {patient_time} due to unforeseen circumstances that have arisen.

            I apologize for any inconvenience this may cause you, and I hope that you can understand the situation. I would appreciate it if we could reschedule the appointment for a later date that is convenient for both of us.

            Please let me know if there are any dates or times that work best for you, and I will do my best to accommodate your schedule. I understand that your time is valuable, and I will make every effort to ensure that the rescheduled appointment is as convenient as possible for you.

            Thank you for your understanding, and I look forward to hearing back from you soon.
            '''
            send_mail(MSG=f'I am suggest this time {patient_time} if you comfirtable so accept this time and replay me on this email',user=patient_name,subjectMSG='Reshedule your appointment',Text=text,email=patient_email)

        except:

            if MyForms.is_valid():
                    pid = request.POST.get('pid')
                    Did = request.POST.get('Did')
                    name = request.POST.get('file_name')
                    Pname = request.POST.get('Pname')
                    File = request.FILES.get('file')

                    exist = PatientReport.objects.filter(name=name ,upload=File).exists()
                    exist2 = PatientReport.objects.filter(upload=File).exists()
                    if exist:
                        messages.error(request, "The name file %s is already exists...!!!" %File)
                    elif exist2:
                        messages.error(request, "The file %s is already exists...!!!" %File)
                    else:
                        PatientReport.objects.create(name=name,patientName=Pname, upload=File,doctor_id=Did,patient_id=pid).save()
                        messages.success(request,'File Upload Successfully')

    

    
    param = {'Form':myform,"Id":id,'id':Id,"appointment":appointment, "Clinics":Clinic, "Homes":Home, "Videos":Video, "Canclled":Canclled, "time":datetime.today().strftime("%I:%M %p"),"Fulllength":Fulllength,
             "Home":Homelength,"Video":Videolength,"Clinic":Clinicength,"PendingFulllength":PendingFulllength,"PendingClinicength":PendingClinicength,"PendingVideolength":PendingVideolength,
             "PendingHomelength":PendingHomelength,"Pendingappointment":Pendingappointment}
    
    return render(request,'DAppointment.html',param)


def AppointmentBill(request):
    id = request.GET.get('Doctor_id')
    print(id)
    Id = Doctor.objects.get(doctor_id=id)

    appointment = Appointments.objects.filter(Doctor_id=id)
    print(appointment)
    # appointment_bill = []

    param = None

    for i in appointment:
        # appointment_bill = Bill.objects.filter(appointments_id=i.Appointments_id)
        print(i.Appointments_id)
        appointment_bill = Bill.objects.filter(appointments_id=i.Appointments_id)
        print(appointment_bill)

        # param = {'id':Id,"appointment_bill":appointment_bill}
        
    param = {"Id":id,'id':Id,"appointment_bill":appointment_bill}
    return render(request,'bill.html',param)

def Review(request):
    id = request.GET.get('Doctor_id')
    Id = Doctor.objects.get(doctor_id=request.GET.get('Doctor_id'))
    rating = ReviewsRatings.objects.filter(doctorId=id)
    param = {"Id":id,'id':Id,'rating':rating}
    return render(request,"rating.html",param)

def Profile(request):
    id = request.GET.get('Doctor_id')
    Id = Doctor.objects.get(doctor_id=request.GET.get('Doctor_id'))
    sp = specilaity.objects.all()
    if request.method == "POST":
        doctor_name = request.POST['name']
        doctor_sex = request.POST['sex']
        doctor_professions = request.POST['category']
        email = request.POST['email']
        mobile = request.POST['mob']
        doctor_address = request.POST['Add']
        doctor_city = request.POST['City']
        doctor_state = request.POST['state']
        doctor_zip = request.POST['Zip']
        doctor_area = request.POST['area']
        doctor_country = request.POST['country']
        hosptial_name = request.POST['Hname']
        hospital_address = request.POST['Haddress']
        hosptial_area = request.POST['Harea']
        hosptial_city = request.POST['Hcity']
        hosptial_state = request.POST['Hstate']
        hosptial_country = request.POST['Hcountry']
        hosptial_pincode = request.POST['Hzip']
        hosptial_telephone = request.POST['tel']
        doctor_appointment = request.POST['advance']
        doctor_fee = request.POST['fee']
        one = request.POST['slot']
        doctor_college = request.POST['Clg']
        year_of_compilation = request.POST['year']
        doctor_experince = request.POST['Experience']
        doctor_Awards = request.POST['award']
        doctor_Year = request.POST['awardYear']
        doctor_qualifcations = request.POST['doctor_qualifcation']
        doctor_self = request.POST['doctor_self']

        Doctor.objects.filter(doctor_id=id).update(doctor_qualifcation=doctor_qualifcations,doctor_name=doctor_name,email=email,
                                    doctor_sex=doctor_sex,mobile=mobile,doctor_profession_id=doctor_professions,doctor_address=doctor_address,doctor_city=doctor_city,doctor_state=doctor_state,
                                    doctor_zip=doctor_zip,doctor_self=doctor_self,doctor_country=doctor_country,doctor_college=doctor_college,year_of_compilation=year_of_compilation,
                                    doctor_area=doctor_area,hosptial_name=hosptial_name,hospital_address=hospital_address,hosptial_area=hosptial_area,hosptial_city=hosptial_city
                                    ,hosptial_state=hosptial_state,hosptial_country=hosptial_country,hosptial_pincode=hosptial_pincode,hosptial_telephone=hosptial_telephone,
                                    doctor_Awards=doctor_Awards ,doctor_Awards_year=doctor_Year,Experience=doctor_experince,time_Slots=one,doctor_fee=doctor_fee,advance_appointment=doctor_appointment,
                                    
                                )
        messages.success(request,'Update Successfully')
    param = {"Id":id,'id':Id,"sp":sp}
    return render(request,'profile.html',param)

def updatePending(request,id):
    Appointments.objects.filter(Appointments_id=id).update(appointment_status="complete")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))