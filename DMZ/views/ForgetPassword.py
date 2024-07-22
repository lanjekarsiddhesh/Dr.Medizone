from .view import generate_otp
from django.shortcuts import render , redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from math import *
from .mail import send_mail

Users = ''
user_name = ''
Model = ''

def ForgetPassword(request):
    if request.method == 'POST':
        email = request.POST['mobile']
        userType = request.POST['usertype']
        Model += userType
        Users += email

        if userType == 'Patient':
            try:
                Patient2 = Patient.objects.get(email=email)
                if email == Patient2.email:
                    user_name += Patient2.patient_name
                    generate_otp(request)
                    send_mail(email="salonijagtap55@gmail.com",Text='Your OTP is:- ',subjectMSG="Verifying By OTP",user=Patient2.patient_name,MSG=request.session.get('otp'))
                    return redirect('/otp/')

            except:
                messages.warning(request, "This email is doesn't valid")

        elif userType == 'Doctor':
            try:
                doctor2 = Doctor.objects.get(email=email)
                if email == doctor2.email:
                    user_name += doctor2.doctor_name
                    generate_otp(request)
                    send_mail(Text='Your OTP is:- ',email="salonijagtap55@gmail.com",subjectMSG="Verifying By OTP",user=doctor2.doctor_name,MSG=request.session.get('otp'))
                    return redirect('/otp/')
            
            except:
                messages.warning(request, "This email is doesn't valid")
        # doctortDB = Doctor.objects.filter()
    return render(request,'forget.html')

def ForgetByMobile(request):

    if request.method == 'POST':
        mobile = request.POST['mobile']
        userType = request.POST['usertype']
        Model += userType

        if userType == 'Patient':
            try:
                Patient2 = Patient.objects.get(mobile=mobile)
                if mobile == str(Patient2.mobile):
                    user_name += Patient2.patient_name
                    Users += mobile
                    generate_otp(request)
                    print("Match")
                    send_mail(user=Patient2.patient_name,OtpVerify=request.session.get('otp'))
                    return redirect('/otp/')
                else:
                    print("doesn't math")

            except:
                messages.warning(request, "This number is doesn't valid")

        elif userType == 'Doctor':
            try:
                doctor2 = Doctor.objects.get(mobile=mobile)
                if mobile == str(doctor2.mobile):
                    user_name += doctor2.doctor_name
                    Users += mobile
                    generate_otp(request)
                    print("Match")
                    send_mail(user=doctor2.doctor_name,OtpVerify=request.session.get('otp'))
                    return redirect('/otp/')
            
            except:
                messages.warning(request, "This number is doesn't valid")
        else:
            print("error")

    return render(request, "forgetByNumber.html")

def ForgetByQuestion(request):

    if request.method == 'POST':
        userType = request.POST['usertype']
        question = request.POST['Question']
        answer = request.POST['answer']
        Model += userType
        question += question
        answer += answer
        

        if userType == 'Patient':
            try:
                Patient2 = Patient.objects.get(Security_Question=question,Security_Answer=answer)
                if Patient2:
                    print("Match ",Patient2.patient_name)
                    return redirect('/changePass/')
                else:
                    print("error")

            except:
                messages.warning(request, "This number is doesn't valid")
                print("Patient Not found")

        elif userType == 'Doctor':
            try:
                doctor2 = Doctor.objects.get(Security_Question=question,Security_Answer=answer)
                if doctor2:
                    # user_name += doctor2.doctor_name
                    # generate_otp(request)
                    # send_mail(user=doctor2.doctor_name,OtpVerify=request.session.get('otp'))
                    return redirect('/changePass/')
            
            except:
                messages.warning(request, "This number is doesn't valid")


    return render (request,"forgetByQuestion.html")