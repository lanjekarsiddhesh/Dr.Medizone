from DMZ.Decorators.Patient_login import is_patient_login
from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime
from math import *

Users = ''
user_name = ''
Model = ''

class user:
    @is_patient_login
    def patient_home(request,patient_id):
        id = Patient.objects.get(patient_id=patient_id)
        param = {'id':id}
        return render(request,'patientHomescreen.html',param)

    def patientRegistration(request):
        Doctor_status = request.session.get('Doctor_status')
        login = request.session.get('patient_status')
        Id = request.session.get('patient_id')
        patient_user = Patient.objects.all()
        try:
            if  request.method == 'POST':
                patient_fname = request.POST['patient_Name']
                patient_mname = request.POST['Mpatient_Name']
                patient_lname = request.POST['Lpatient_Name']
                Pname=patient_fname+" "+patient_mname+" "+patient_lname
                patient_name = Pname
                email = request.POST['patient_email']
                patient_sex = request.POST['patient_sex']
                patient_DOB = request.POST['patient_dob']
                mobile = request.POST['patient_mob']
                patient_profile = request.FILES['patient_prof']
                patient_address = request.POST['patient_add']
                patient_area = request.POST['patient_area']
                patient_city = request.POST['patient_ct']
                patient_state= request.POST['patient_st']
                patient_country = request.POST['patient_country']
                patient_zip = request.POST['patient_pin']
                patient_userName = request.POST['patient_user']
                password =  request.POST['patient_pass']
                passwordC =  request.POST['patient_cpass']
                patient_Blood =  request.POST['patient_blood']
                Qna = request.POST['patient_qna']
                Ans = request.POST['patient_ans']

                USERNAME = ''
                EMAIL = ''
                MOBILE = ''

                for i in patient_user:
                    if i.patient_userName == patient_userName:
                        USERNAME = i.patient_userName
                    if i.email == email:
                        EMAIL = i.email
                    if i.mobile == mobile:
                        MOBILE = i.mobile


                if USERNAME == patient_userName :
                    messages.warning(request,f"This USERNAME is already exist; Please enter unique USERNAME")
                elif EMAIL == email:
                    messages.warning(request,f"This Email is already exist; Please enter unique Email")
                elif MOBILE == mobile:
                    messages.warning(request,f"This Mobile is already exist; Please enter unique Mobile")

                else:
                    if password == passwordC:
                        hash_password = make_password(password)

                        new_patient = Patient(patient_Blood=patient_Blood,patient_name=patient_name,email=email,patient_DOB=patient_DOB,
                            patient_sex=patient_sex,mobile=mobile,patient_profile=patient_profile,Security_Answer=Qna,Security_Question=Ans,
                            patient_address=patient_address,patient_city=patient_city,patient_state=patient_state,patient_zip=patient_zip,
                            patient_userName=patient_userName,password=hash_password,patient_area=patient_area,patient_country=patient_country)
                                
                        new_patient.save()
                        messages.success(request, f"{patient_name} your information is save sucessfully")

                    else:
                        messages.error(request, "Password doesn't match")
        except:
            messages.error(request, "Something Wrong!!! Fill the form again")

        param = {"Doctor_status":Doctor_status,"Id":Id,"login":login, }
        return render(request,'PatientRegistrationForm.html',param)


    def update_Patient_loginDetails(patient):
        login = Patient_login.get_patient_by_id(patient.patient_id)
        if login:
            login.total_login += 1
            Patient_login.objects.filter(Patient_id=patient.patient_id).update(total_login=login.total_login,Last_login=datetime.now())
        else:
            logindetails = Patient_login(Patient_id_id=patient.patient_id,Last_login=datetime.now())
            logindetails.save()


    def PatientSave(request):
        request.session.get('otp')

        new_patient = Patient(patient_Blood=user.Blood,patient_name=user.name,email=user.email,patient_DOB=user.DOB,
                patient_sex=user.sex,mobile=int(user.mobile),patient_profile=user.profile,
                patient_address=user.address,patient_city=user.city,patient_state=user.state,patient_zip=user.zip,
                patient_userName=user.userName,password=user.hash_password,patient_area=user.area,patient_country= user.country)

        if request.method == "POST":
            one = request.POST['Oneotp']
            two = request.POST['Twootp']
            three = request.POST['Threeotp']
            four = request.POST['Fourotp']
            # otp = request.POST['otp']
            otp = one+two+three+four
            
            if request.session.get('otp') == otp:
                print("Match")
                
                new_patient.save()
                return redirect('/Login/')
                
        return render(request,"otp2.html",{"check":request.session.get('otp')})