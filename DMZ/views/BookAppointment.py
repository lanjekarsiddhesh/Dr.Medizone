from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from ..models import *
from ..forms import *
from django.contrib import messages
from math import *
import razorpay
from .mobile import send_otp
from .api import ApiKey


Users = ''
user_name = ''
Model = ''

Api = ApiKey()

def BookAppointment(request,doctor_id):
    # retrive information from db
    Doctor_status = request.session.get('Doctor_status')
    doctor = Doctor.objects.filter(doctor_id=doctor_id)
    doctors = Doctor.objects.get(doctor_id=doctor_id)
    Appointment = Appointments.objects.filter(Doctor_id_id=doctor_id)
    Appointment1 = Appointments.objects.filter(Doctor_id_id=doctor_id,Appointments_date='2023-01-08')
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')

    # Appointment_times = []
    Appointment_times = ''
    Appointment_dates = ''
    for i in Appointment:
        date = str(i.Appointments_date)
        time = i.Appointments_time
        Appointment_times += time + " " 
        Appointment_dates += date + " " 
    
    # collect info from appointment form
    
    if request.method == 'POST':
        client = razorpay.Client(auth=(Api.get("RKey"), Api.get("RSecretKey")))
        DATA = {
            "amount": doctors.doctor_fee*100,
            "currency": "INR",
            "receipt": "receipt#1",
            "payment_capture":1
        }
        
        payment = client.order.create(data=DATA)
        payment_id = payment['id']


        Appointments_date = request.POST['date']
        Appointments_time = request.POST['time']
        Appointments_type = request.POST['type']
        patient_name = request.POST['ptfname'] +" "+ request.POST['ptlaname']
        patient_fname = patient_name
        mobile = request.POST['mob']
        Doctor_name = doctors.doctor_name
        Doctor_speciality = doctors.doctor_category
        Fees = doctors.doctor_fee
        Hospital_address = doctors.hosptial_name
        Hospital_number = doctors.hosptial_telephone
        Hospital_pincode = doctors.hosptial_pincode
        paymenyt = request.POST['flexRadioDefault']
        patient_id = request.session.get('patient_id')

        # Save appointment info into db
        Appointment = Appointments(order_id=payment_id,Appointments_date=Appointments_date,Appointments_time=Appointments_time,Appointments_type=Appointments_type,
        patient_name=patient_fname,patient_mobile=mobile,Doctor_id_id=doctor_id,patient_id = patient_id)

        # save form's msg in variable

        msg1 = "name:- "+patient_fname
        msg2 = "time:- "+Appointments_time+", date:- "+Appointments_date
        msg3 = "type:- "+Appointments_type
        msg4 = "Doctor name:- "+Doctor_name
        msg5 = " Doctor speciality:- "+ Doctor_speciality
        msg6 = "fee:- "+ str(Fees)
        msg7 = "address:- "+Hospital_address+", pincode:- "+Hospital_pincode
        msg8 = "Hospital number:- "+str(Hospital_number)
        msg9 = "payment status:- "+str(paymenyt)
        



        if Appointments_type == 'Videocall meeting' or paymenyt == 'paid':
            msg10 = "videocall link: "
            appointment_detail = f"{msg1}\n{msg2}\n{msg3}\n{msg4}\n{msg5}\n{msg6}\n{msg7}\n{msg8}\n{msg9}\n{msg10}"
            Bill.objects.create(Payment= Fees, order_id=payment_id).save()
            Appointment.save()
            messages.success(request, "your appointment is booked others details send on entered mobile number")
            # send msg on mobile number
            send_otp(my_number=mobile,msg=appointment_detail)
            return render(request,'Razorpay.html',{'payment':payment,'payment_id':payment_id,'api_key':Api.get("RKey")})
            
        else:
            appointment_detail = f"{msg1}\n{msg2}\n{msg3}\n{msg4}\n{msg5}\n{msg6}\n{msg7}\n{msg8}\n{msg9}"
            Appointment.save()
            Bill.objects.create(Payment= Fees, order_id=payment_id, appointments=Appointment).save()
            # views.render_pdf(request)
            messages.success(request, "your appointment is booked others details send on entered mobile number")
            # send msg on mobile number
            send_otp(my_number=mobile,msg=appointment_detail)
            return redirect(f'/MakingPdf/create/{Appointment.Appointments_id}')

            # show success msg
            
    param = {"Doctor_status":Doctor_status,"Id":Id,"login":login,'RAZORPAY_API_KEY':Api.get("RKey"),'Appointment_dates':Appointment_dates,'Appointment_times':Appointment_times,"patient":patient,'doctor':doctor[0],}

    return render(request,'BookAppointment.html',param)
