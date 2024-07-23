from DMZ.Decorators.Doctor_login import is_doctor_login
from django.shortcuts import render
from ..models import *
from ..forms import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime
from math import *

Users = ''
user_name = ''
Model = ''

def doctorRegistration(request):
    login = request.session.get('patient_status')
    Doctor_status = request.session.get('Doctor_status')
    Id = request.session.get('patient_id')
    special = specilaity.objects.all()
    name = []
    
    # time slot
    # 1 hrs
    One_hrs = [
        "1am - 2am",
        "2am - 3am",
        "3am - 4am",
        "4am - 5am",
        "5am - 6am",
        "6am - 7am",
        "7am - 8am",
        "8am - 9am",
        "9am - 10am",
        "10am - 11am",
        "11am - 12am",
        "12am - 1pm",
        "1pm - 2pm",
        "2pm - 3pm",
        "3pm - 4pm",
        "4pm - 5pm",
        "5pm - 6pm",
        "6pm - 7pm",
        "7pm - 8pm",
        "8pm - 9pm",
        "9pm - 10pm",
        "10pm - 11pm",
        "11pm - 12pm"
    ]

    # 30 min 
    Half_hrs = [
            "1am - 1:30am",
            "1:30am - 2am",
            "2am - 2:30am",
            "2:30am - 3am",
            "3am - 3:30am",
            "3:30am - 4am",
            "4am - 4:30am",
            "4:30am - 5am",
            "5am - 5:30am",
            "5:30am - 6am",
            "6am - 6:30am",
            "6:30am - 7am",
            "7am - 7:30am",
            "7:30am - 8am",
            "8am - 8:30am",
            "8:30am - 9am",
            "9am - 9:30am",
            "9:30am - 10am",
            "10am - 10:30am",
            "10:30am - 11am",
            "11am - 11:30am",
            "11:30am - 12am",
            "12am - 12:30pm",
            "12:30pm - 1pm",
            "1pm - 1:30pm",
            "1:30pm - 2pm",
            "2pm - 2:30pm",
            "2:30pm - 3am",
            "3pm - 3:30pm",
            "3:30pm - 4pm",
            "4pm - 4:30pm",
            "4:30pm - 5pm",
            "5pm - 5:30pm",
            "5:30pm - 6pm",
            "6pm - 6:30am",
            "6:30pm - 7pm",
            "7pm - 7:30pm",
            "7:30pm - 8pm",
            "8pm - 8:30pm",
            "8:30pm - 9pm",
            "9pm - 9:30pm",
            "9:30pm - 10pm",
            "10pm - 10:30pm",
            "10:30pm - 11pm",
            "11pm - 11:30pm",
            "11:30pm - 12pm"
    ]

    # 15min
    A_15mn = [
            "1am - 1:15am",
            "1:15am - 1:30am",
            "1:30am - 1:45am",
            "1:45am - 2am",

            "2am - 2:15am",
            "2:15am - 2:30am",
            "2:30am - 2:45am",
            "2:45am - 3am",

            "3am - 3:15am",
            "3:15am - 3:30am",
            "3:30am - 3:45am",
            "3:45am - 4am",

            "4am - 4:15am",
            "4:15am - 4:30am",
            "4:30am - 4:45am",
            "4:45am - 5am",

            "5am - 5:15am",
            "5:15am - 5:30am",
            "5:30am - 5:45am",
            "5:45am - 6am",

            "6am - 6:15am",
            "6:15am - 6:30am",
            "6:30am - 6:45am",
            "6:45am - 7am",

            "7am - 7:15am",
            "7:15am - 7:30am",
            "7:30am - 7:45am",
            "7:45am - 8am",

            "8am - 8:15am",
            "8:15am - 8:30am",
            "8:30am - 8:45am",
            "8:45am - 9am",

            "9am - 9:15am",
            "9:15am - 9:30am",
            "9:30am - 9:45am",
            "9:45am - 10am",

            "10am - 10:15am",
            "10:15am - 10:30am",
            "10:30am - 10:45am",
            "10:45am - 11am",

            "11am - 11:15am",
            "11:15am - 11:30am",
            "11:30am - 11:45am",
            "11:45am - 12am",

            "1pm - 1:15pm",
            "1:15pm - 1:30ap",
            "1:30pm - 1:45pm",
            "1:45pm - 2pm",

            "2pm - 2:15pm",
            "2:15pm - 2:30pm",
            "2:30pm - 2:45pm",
            "2:45pm - 3pm",

            "3pm - 3:15pm",
            "3:15pm - 3:30pm",
            "3:30pm - 3:45pm",
            "3:45pm - 4pm",

            "4pm - 4:15pm",
            "4:15pm - 4:30pm",
            "4:30pm - 4:45pm",
            "4:45pm - 5pm",

            "5pm - 5:15pm",
            "5:15pm - 5:30pm",
            "5:30pm - 5:45pm",
            "5:45pm - 6ap",

            "6pm - 6:15pm",
            "6:15pm - 6:30pm",
            "6:30pm - 6:45pm",
            "6:45pm - 7pm",

            "7pm - 7:15pm",
            "7:15pm - 7:30pm",
            "7:30pm - 7:45pm",
            "7:45pm - 8pm",

            "8pm - 8:15pm",
            "8:15pm - 8:30pm",
            "8:30am - 8:45pm",
            "8:45pm - 9pm",

            "9pm - 9:15pm",
            "9:15pm - 9:30pm",
            "9:30pm - 9:45pm",
            "9:45pm - 10pm",

            "10pm - 10:15pm",
            "10:15pm - 10:30pm",
            "10:30pm - 10:45pm",
            "10:45pm - 11pm",

            "11pm - 11:15pm",
            "11:15pm - 11:30pm",
            "11:30pm - 11:45pm",
            "11:45pm - 12pm",
        ]
    # time slot end

    para = {"special":special,"name": name,"Doctor_status":Doctor_status,"One_hrs":One_hrs,"Half_hrs":Half_hrs,"A_15mn":A_15mn,"Id":Id,"login":login}

    global new_doctor
    
    if request.method == 'POST':
        try:
            doctor_fname = request.POST['doctortName']
            doctor_mname = request.POST['MdoctortName']
            doctor_lname = request.POST['LdoctortName']
            name=doctor_fname+" "+doctor_mname+" "+doctor_lname
            # profile
            doctor_name = name
            doctor_DOB = request.POST['doctordob']  
            doctor_sex = request.POST['doctorsex']
            doctor_professions = request.POST['speciality']
            doctor_qualifcation = request.POST['qualification']
            doctor_profile = request.FILES['prof']
            doctor_certificate = request.FILES['cer']
            doctor_self = request.POST['self']
            doctor_experince = request.POST['Experience']
            doctor_Awards = request.POST['Awards']
            doctor_Year = request.POST['Year']
            doctor_fee = request.POST['fee']
            doctor_appointment = request.POST['appointment']
                # contact
            
            doctor_address = request.POST['doctoradd']
            doctor_area = request.POST['doctorarea']
            doctor_city = request.POST['doctorct']
            doctor_country = request.POST['doctorcountry']
            doctor_state = request.POST['doctorst']
            doctor_zip = request.POST['doctorpin']
                #userpass&name
            email = request.POST['doctoremail']
            # email_otp = request.POST['doctoremailotp']
            mobile = request.POST['doctormob']
            # mobile_otp = request.POST['doctormobotp']
            doctor_userName = request.POST['doctoruser']
            password = request.POST['doctorpass']
            doctor_C_pass = request.POST['cpass']
            #clinic
            hosptial_name = request.POST['C\H_name']
            hospital_address = request.POST['C\H_add']
            hosptial_area = request.POST['C\H_area']
            hosptial_city = request.POST['C\H_ct'] 
            hosptial_state = request.POST['C\H_st']
            hosptial_country = request.POST['C\H_country']
            hosptial_pincode = request.POST['C\H_pincode']
            hosptial_telephone = request.POST['C\H_tel']
            one = request.POST['onehrs']
            question = request.POST['sequrityQ']
            answer = request.POST['sequrityA']

            sp = specilaity.objects.get(index=doctor_professions)
            
            USERNAME = ''
            EMAIL = ''
            MOBILE = ''
            for i in Doctor.objects.all():
                if i.doctor_userName == doctor_userName:
                    USERNAME = i.doctor_userName
                if i.email == email:
                    EMAIL = i.email
                if i.mobile == mobile:
                    MOBILE = i.mobile


            if USERNAME == doctor_userName :
                messages.warning(request,f"This USERNAME is already exist; Please enter unique USERNAME")
            elif EMAIL == email:
                messages.warning(request,f"This Email is already exist; Please enter unique Email")
            elif MOBILE == mobile:
                messages.warning(request,f"This Mobile is already exist; Please enter unique Mobile")
            else:
                #password confirmation 
                if password==doctor_C_pass:
                    password = make_password(password)

                    new_doctor = Doctor(doctor_category=sp.specilaity_category,doctor_qualifcation=doctor_qualifcation,doctor_name=doctor_name,email=email,doctor_DOB=doctor_DOB,
                            doctor_sex=doctor_sex,mobile=mobile,doctor_profession_id=doctor_professions,doctor_profile=doctor_profile,
                            doctor_certificate=doctor_certificate,doctor_address=doctor_address,doctor_city=doctor_city,doctor_state=doctor_state,
                            doctor_zip=doctor_zip,doctor_userName=doctor_userName,password=password,doctor_self=doctor_self,doctor_country=doctor_country,
                            doctor_area=doctor_area,hosptial_name=hosptial_name,hospital_address=hospital_address,hosptial_area=hosptial_area,hosptial_city=hosptial_city
                            ,hosptial_state=hosptial_state,hosptial_country=hosptial_country,hosptial_pincode=hosptial_pincode,hosptial_telephone=hosptial_telephone,
                            doctor_Awards=doctor_Awards ,doctor_Awards_year=doctor_Year,Experience=doctor_experince,time_Slots=one,doctor_fee=doctor_fee,advance_appointment=doctor_appointment,
                            Security_Answer=answer,Security_Question=question
                            )  
                    new_doctor.save()
                    messages.success(request, f" dr. {doctor_name} your information is save sucessfully")

                else:
                    messages.warning(request, 'password is not match.')
        except:
            messages.error(request, 'Something Wrong!!! Fill the form again')
        
    return render(request,'DoctorRegistrationForm.html',para)



def update_Dr_loginDetails(Dr):
    login = Doctor_login.get_doctor_by_id(Dr.doctor_id)
    if login:
        login.total_login += 1
        Doctor_login.objects.filter(Doctor_id=Dr.doctor_id).update(total_login=login.total_login,Last_login=datetime.now())
    else:
        logindetails = Doctor_login(Doctor_id_id=Dr.doctor_id,Last_login=datetime.now())
        logindetails.save()

def doctors(request):
    doctor = None
    Doctor_status = request.session.get('Doctor_status')
    patient = Patient.objects.all()
    specialist = specilaity.objects.all()
    rating = ReviewsRatings.objects.all()
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    patient_id = request.session.get('patient_id')
    Doctor_id = request.session.get('Doctor_id')
    lengths = len(specialist)
    Greater = request.GET.get('G')
    Lesser = request.GET.get('L')
    
    a = []
    for i in rating:
        id = i.doctorId_id
        if id == id:
            a.append(id)
        print(len(a))
    
    # print(request.GET)
    Category = request.GET.get('doctor_category')
    star = request.GET.get('star')

    if Category:
        doctor = Doctor.objects.filter(doctor_profession=Category)

    elif star:
        doctor = Doctor.objects.filter(overall_rating__gte=star)
    elif Greater and Lesser:
        doctor = Doctor.objects.filter(doctor_fee__lte=Greater)
    elif Greater:
        doctor = Doctor.objects.filter(doctor_fee__gte=Greater)
    else:
        doctor = Doctor.objects.all()

    if request.method == "POST":
        search = request.POST.get('Searches')
        if search != None:
            doctor = Doctor.objects.filter(doctor_category__icontains=search) or Doctor.objects.filter(doctor_name__icontains=search) or Doctor.objects.filter(doctor_fee__icontains=search)
    
    length = len(doctor)
    param =  {"Doctor_status":Doctor_status,"Doctor_id":Doctor_id,"patient_id":patient_id,"Doctor_status":Doctor_status,"Id":Id,"login":login,"patient":patient,'rating':rating,'range':range(length),'doctor':doctor,'range': range(lengths), 'specialists':specialist}
    return render(request,'doctors.html',param)        

@is_doctor_login
def doctor_home(request,doctor_id):
    Id = Doctor.objects.get(doctor_id=doctor_id)
    return render(request,'doctorHomescreen.html',{'id':Id})


def doctor_profile(request,doctor_id,doctor_category):

    doctor = Doctor.objects.filter(doctor_id=doctor_id)
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    category = Doctor.objects.filter(doctor_category=doctor_category)
    # patient = Patient.objects.all()
    review = ReviewsRatings.objects.filter(doctorId_id = doctor_id)
    patient_id = request.session.get('patient_id')
    length = len(review)
    Dr_length = len(category)
    slides = Dr_length//4 + ceil((Dr_length/4)-(Dr_length//4))
    # doctor = Doctor.objects.get(doctor_id=doctor_id)

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

    return render(request,'doctor_profile.html',{"Id":Id,"no_of_slides":slides, "slide_range": range(1,slides) ,"patient_id":patient_id,"login":login,'length':length,"category":category,"review":review,'doctor':doctor[0]})

def doctor_specilaity(request,index):
    Doctor_status = request.session.get('Doctor_status')
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    Specilaitys = specilaity.objects.get(index=index)
    Specilaity = specilaity.objects.filter(index=index) 
    patient_id = request.session.get('patient_id')
    Doctor_id = request.session.get('Doctor_id')
    # Specilaity.specilaity_category
    # doctors = Doctor.objects.all()
    if Specilaitys.specilaity_category:
        doctors = Doctor.objects.filter(doctor_profession=Specilaitys)
    
    param = {"Doctor_status":Doctor_status,"Doctor_id":Doctor_id,"patient_id":patient_id,"Doctor_status":Doctor_status,"Id":Id,"login":login,'Specilaity':Specilaity[0],'doctor':doctors}
    return render(request,'filter.html',param)


def overall_star(doctor_id):
    doctor = Doctor.objects.filter(doctor_id=doctor_id)
    one = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=1))
    one_half = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=1.5))
    two = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=2))
    two_half = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=2.5))
    three = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=3))
    three_half = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=3.5))
    four = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=4))
    four_half = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=4.5))
    five = len(ReviewsRatings.objects.filter(doctorId=doctor_id,rating=5))

    if  one > one_half or one > two or one > two_half or one > three or one > three_half or one > four or one > four_half or one > five:
        doctor.update(overall_rating=1.0)

    if two > one or two > one_half or two > two_half or two > three or two > three_half or two > four or two > four_half or two > five:
        doctor.update(overall_rating=2.0)

    if three > one or three > one_half or three > two or three > two_half or three > three_half or three > four or three > four_half or three > five:
        doctor.update(overall_rating=3.0)

    if four > one or four > one_half or four > two or four > two_half or four > three or four > three_half or four > four_half or four > five:
        doctor.update(overall_rating=4.0)

    if five > one or five > one_half or five > two or five > two_half or five > three or five > three_half or five > four or five > four_half:
        doctor.update(overall_rating=5.0)

    # half's

    if four_half > one or four_half > one_half or four_half > two or four_half > two_half or four_half > three or four_half > three_half or four_half > four or four_half > five:
        doctor.update(overall_rating=4.5)

    if three_half > one or three_half > one_half or three_half > two or three_half > two_half or three_half > three or three_half > four or three_half > four_half or three_half > five:
        doctor.update(overall_rating=3.5)

    if two_half > one or two_half > one_half or two_half > two or two_half > three or two_half > three_half or two_half > four or two_half > four_half or two_half > five:
        doctor.update(overall_rating=2.5)

    if one_half > one or one_half > two or one_half > two_half or one_half > three or one_half > three_half or one_half > four or one_half > four_half or one_half > five:
        doctor.update(overall_rating=1.5)
