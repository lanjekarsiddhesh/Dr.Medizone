from distutils.command.upload import upload
from email.policy import default
from ftplib import MAXLINE
from statistics import mode
# from unittest.util import max_length
from django.db import models
from datetime import datetime
from datetime import time

# Create your models here.

class specilaity(models.Model):
    specilaity_category = models.CharField(max_length=200)
    index = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="dmz_imgs/speciality_icon/", default="")

    def __str__(self):
        return self.specilaity_category


#--------------------------------------------------------------Doctor & Patient Registration's table--------------------------------------------------------------------------

#patient module
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)
    patient_DOB = models.DateField(null=True)
    patient_sex = models.CharField(max_length=10)
    mobile = models.BigIntegerField(unique=True)
    patient_Blood = models.CharField(max_length=50,default="A+")
    patient_profile = models.ImageField(upload_to='dmz_imgs/patient/images/profile', default="")
    patient_address = models.CharField(max_length=200)
    patient_city = models.CharField(max_length=50)
    patient_state = models.CharField(max_length=50)
    patient_zip = models.IntegerField()
    patient_userName = models.CharField(max_length=50, unique=True,default="")
    password = models.CharField(max_length=100,default="")
    patient_area = models.CharField(max_length=50,default="")
    patient_country = models.CharField(max_length=50,default="")
    status = models.CharField(max_length=30,default="Logout")
    Security_Question = models.CharField(max_length=500,default="What is your name ?")
    Security_Answer = models.CharField(max_length=500, default="Drmedizone")

    # joining_date = models.DateTimeField(default=datetime.today())#not add in doc
    # total_login = models.IntegerField(default=0)#not add in doc
    #following def fun for show the name in front on admin pannel

    @staticmethod
    def get_patient_by_username(username):
        try:
            return Patient.objects.get(patient_userName=username)
        except:
            return False

    def isExists(self):
        if Patient.objects.filter(patient_userName=self.username):
            return True
        else:
            return False


    def __str__(self):
        return self.patient_name
 
#doctor module
class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)
    doctor_DOB = models.DateField()
    doctor_sex = models.CharField(max_length=10)
    mobile = models.BigIntegerField(unique=True)
    doctor_address = models.CharField(max_length=200)
    doctor_city = models.CharField(max_length=50)
    doctor_state = models.CharField(max_length=50)
    doctor_zip = models.BigIntegerField()
    doctor_userName = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100 ,unique=True,default="")
    doctor_country = models.CharField(max_length=100,default="")
    doctor_area = models.CharField(max_length=100,default="")
    doctor_self = models.TextField(max_length=100, default='')
    #awards
    doctor_Awards = models.CharField(max_length=500,default='')
    doctor_Awards_year = models.CharField(max_length=500,default='')
    #clinic
    hosptial_name=models.CharField(max_length=100,default="")#not add in doc-
    hospital_address=models.CharField(max_length=100,default="")
    hosptial_area=models.CharField(max_length=100,default="")
    hosptial_city=models.CharField(max_length=100,default="")
    hosptial_state=models.CharField(max_length=100,default="")#not add in doc-
    hosptial_country=models.CharField(max_length=100,default="")
    hosptial_pincode=models.CharField(max_length=100,default="")
    hosptial_telephone=models.BigIntegerField()
    #Qualification
    doctor_profession = models.ForeignKey(specilaity,on_delete=models.SET_NULL, blank=True, null=True)
    doctor_category = models.CharField(max_length=50, default="doctor")
    # doctor_category = models.CharField(max_length=50, default="doctor")
    doctor_profile = models.ImageField(upload_to='dmz_imgs/doctor/images/profile', default="null")
    doctor_certificate = models.ImageField(upload_to='dmz_imgs/doctor/images/certificates' ,default="null")
    doctor_qualifcation = models.CharField(max_length=100,default="doctor")
    doctor_college = models.CharField(max_length=200,default="Mumbai AIMS college")
    year_of_compilation = models.CharField(max_length=200,default="1995")
    #appointmnet
    doctor_fee = models.BigIntegerField(default="100")
    advance_appointment = models.IntegerField(default="1")
    time_Slots = models.CharField(max_length=1000,default='')
    # Appointments_day = models.BooleanField(default=False)
    # payment_satus = models.CharField(max_length=50, default="unpaid")
    #experince
    Experience = models.IntegerField(default=5)
    Security_Question = models.CharField(max_length=500,default="What is your name ?")
    Security_Answer = models.CharField(max_length=500, default="Drmedizone")
    #advance
    joining_date = models.DateTimeField(auto_now_add=True)#not add in doc
    status = models.CharField(max_length=50,default="Logout")
    overall_rating = models.FloatField(default=0)
    # total_login = models.IntegerField(default=0)#not add in doc

    @staticmethod
    def get_doctor_by_username(username):
        try:
            return Doctor.objects.get(doctor_userName=username)
        except:
            return False

    def isExists(self):
        if Doctor.objects.filter(doctor_userName=self.username):
            return True
        else:
            return False

    def __str__(self):
        return self.doctor_name

#--------------------------------------------------------------Appointment's table--------------------------------------------------------------------------

class Appointments(models.Model):
    Appointments_id = models.AutoField(primary_key=True)
    Appointments_date = models.DateField(default="")
    Appointments_time = models.CharField(max_length=100,default='')
    Appointments_type = models.CharField(max_length=50,default="")
    order_id = models.CharField(max_length=100,default="")
    patient_name = models.CharField(max_length=100,default="Patient")
    patient_mobile = models.CharField(max_length=100,default="123456789")
    appointment_status = models.CharField(max_length=30,default="pending")
    Doctor_id = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
    Cancelled = models.BooleanField(default=False)
    
#--------------------------------------------------------------Login's table--------------------------------------------------------------------------

class Doctor_login(models.Model):
    id = models.AutoField(primary_key=True)
    Doctor_id = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    # Doctor_username = models.CharField(max_length=100)
    # Doctor_pass = models.CharField(max_length=100)
    # Doctor_email = models.CharField(max_length=100)
    # Sequrity_question = models.CharField(max_length=100)
    # Sequrity_answer = models.CharField(max_length=100)#not add in doc
    Last_login = models.DateTimeField(default='')
    total_login = models.IntegerField(default=1)#not add in doc

    def SaveData(self):
        self.save()

    @staticmethod
    def get_doctor_by_id(Doctor_id):
        try:
            return Doctor_login.objects.get(Doctor_id=Doctor_id)
        except:
            return False


class Patient_login(models.Model):
    id = models.AutoField(primary_key=True)
    Patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
    # Patient_username = models.CharField(max_length=100)
    # Patient_pass = models.CharField(max_length=100)
    # Patient_email = models.CharField(max_length=100)
    # Sequrity_question = models.CharField(max_length=100,default="hello",null=True)
    # Sequrity_answer = models.CharField(max_length=100,default="ans",null=True)#not add in doc
    Last_login = models.DateTimeField(default='')
    total_login = models.IntegerField(default=1,null=True)#not add in doc

    @staticmethod
    def get_patient_by_id(Id):
        try:
            return Patient_login.objects.get(Patient_id=Id)
        except:
            return False

#--------------------------------------------------------------Bill table--------------------------------------------------------------------------
class Bill(models.Model):
    Bill_number =models.BigAutoField(primary_key=True)
    Payment = models.IntegerField(default=1)
    order_id = models.CharField(max_length=100,default='')
    Payment_id = models.CharField(max_length=100,null=True)
    signature = models.CharField(max_length=200,null=True)
    Bill_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    appointments = models.ForeignKey(Appointments, on_delete=models.SET_NULL, blank=True, null=True)
    Cancelled = models.BooleanField(default=False)

class Appointmnet_Bill(models.Model):
    Bill_number =models.BigAutoField(primary_key=True)
    order_id = models.CharField(max_length=100,default='')
    Payment_id = models.CharField(max_length=100,null=True)
    signature = models.CharField(max_length=200,null=True)
    Payment = models.IntegerField(default=0)
    Bill_date = models.DateTimeField(default='')
    Doctor_id = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    Patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)

#--------------------------------------------------------------HomeCare table--------------------------------------------------------------------------
class homeCare_page(models.Model):
    id = models.AutoField(primary_key=True)
    Home_Care_Service = models.CharField(max_length=100,default='')
    price = models.BigIntegerField(default=500)
    Home_Care_Service_image = models.ImageField(upload_to='dmz_imgs/HomeCare/',default='')  

    def __str__(self):
        return self.Home_Care_Service                         

class homeCare(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100 ,default='')
    service = models.CharField(max_length=50 ,default='')
    mobile = models.CharField(max_length=50 ,default='')
    email = models.EmailField( default='')
    address = models.CharField(max_length=100 ,default='')
    pincode = models.CharField(max_length=50 ,default='')  
    Reason = models.CharField(max_length=100 ,default='')  
    status = models.CharField(max_length=30,default="pending") 
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.name   

#--------------------------------------------------------------Tele table--------------------------------------------------------------------------
class Tele(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100 ,default='')
    service = models.CharField(max_length=50 ,default='')
    mobile = models.CharField(max_length=50 ,default='')
    email = models.EmailField( default='')
    status = models.CharField(max_length=30,default="pending") 

    def __str__(self):
        return self.name 

#--------------------------------------------------------------FAQ table--------------------------------------------------------------------------
class QNA(models.Model):
    id = models.AutoField(primary_key=True)
    Question = models.CharField(max_length=500,default='')
    Answer = models.CharField(max_length=500,default="Pending")
    Email = models.EmailField(default='')
    complete = models.BooleanField(default=False)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.Question

#--------------------------------------------------------------Diagnostic table--------------------------------------------------------------------------
class diagnostic_test_list(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.BigIntegerField(default=200)
    Who_should_book_this_checkup = models.TextField(null=True)
    What_preparation_is_needed_for_this_Checkup = models.TextField(null=True)
    Age_Group = models.CharField(max_length=200, null=True)
    Gender = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='dmz_imgs/diagnostic_test_img/',default='')
    Home_visit = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class combo_diagnostic_test_list(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    price = models.IntegerField()
    details = models.TextField()
    Who_should_book_this_checkup = models.TextField(null=True)
    What_preparation_is_needed_for_this_Checkup = models.TextField(null=True)
    Age_Group = models.CharField(max_length=200, null=True)
    Gender = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='dmz_imgs/combo_diagnostic_test_img/')
    Test_count = models.IntegerField(default=2)

    def __str__(self):
        return self.name

class dignostic_test_cart(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='Lab_cart')

class dignostic_test_cartItems(models.Model):
    carts = models.ForeignKey(dignostic_test_cart,on_delete=models.CASCADE,related_name="Lab_carItems")
    Tests = models.ForeignKey(diagnostic_test_list,on_delete=models.CASCADE,related_name="Lab_tests")
    book = models.CharField(max_length=500,null=True)
    order = models.CharField(max_length=500,null=True)
    is_paid = models.BooleanField(default=False)

    def get_test_price(self):
        Price = [self.Tests.price]
        return {"total":sum(Price)}

class diagnostic_appointment(models.Model):
    id = models.AutoField(primary_key=True)
    Price = models.IntegerField(null=True)
    SingleTest = models.ForeignKey(diagnostic_test_list,on_delete=models.CASCADE,related_name="single_Lab_tests",null=True)
    ComboTest = models.ForeignKey(combo_diagnostic_test_list,on_delete=models.CASCADE,related_name="Como_Lab_tests",null=True)
    CartTest = models.ForeignKey(dignostic_test_cart,on_delete=models.CASCADE,related_name="Cart_Bill_Lab_tests",null=True)
    Appointments_date = models.DateField(default='')
    Appointments_type = models.CharField(max_length=200,null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    Patient_name = models.CharField(max_length=100,default='')
    Patient_mobile = models.BigIntegerField(default='')
    Patient_email = models.EmailField(default='')
    Patient_gender = models.CharField(max_length=50,default='')
    Patient_pincode = models.BigIntegerField(default='')
    Patient_adress = models.CharField(max_length=300, default='')
    order_id = models.CharField(max_length=100,default="")
    visiting = models.CharField(max_length=100,default="pending")
    Cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.Patient_name   

class DignoBill(models.Model):
    Orders_id = models.CharField(primary_key=True,max_length=500)
    Payment_id = models.CharField(max_length=100,null=True)
    signature = models.CharField(max_length=500,null=True)
    price = models.FloatField()
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)  
    Test = models.ForeignKey(diagnostic_appointment,on_delete=models.CASCADE,related_name="Bill_Lab_tests",null=True)


#--------------------------------------------------------------Lab table--------------------------------------------------------------------------

class Lab(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100,default='')
    Lab_Name = models.CharField(max_length=100,default='')
    Educations = models.CharField(max_length=100,default='')
    Id_Proof = models.ImageField(upload_to='dmz_imgs/Lab/id_proof/',default='')
    license = models.ImageField(upload_to='dmz_imgs/Lab/license/',default='')
    Lab_Iamge = models.ImageField(upload_to='dmz_imgs/Lab/Lab_iamge/',default='')
    UserName = models.CharField(max_length=100,default='')
    Password = models.CharField(max_length=150,default='')
    Address = models.CharField(max_length=500,default='')
    City = models.CharField(max_length=100,default='')
    State = models.CharField(max_length=100,default='')
    Zip = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.Lab_Name
#--------------------------------------------------------------Contact us table--------------------------------------------------------------------------

class Contact_us(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200,default='')
    Email =models.EmailField(default='')
    Subject = models.CharField(max_length=250,default='')
    Message = models.TextField(default="")

    def __str__(self) -> str:
        return self.Subject

#--------------------------------------------------------------Review and rating table--------------------------------------------------------------------------
class ReviewsRatings(models.Model):
    id = models.AutoField(primary_key=True)
    doctorId = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    patient = models.ForeignKey(Patient,on_delete=models.SET_NULL, blank=True, null=True)
    appointment_type = models.CharField(max_length=100,default="")
    health_concern = models.CharField(max_length=100,default="")
    subject = models.CharField(max_length=100,default="")
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    recommend_doctor = models.CharField(max_length=50,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject

class disease(models.Model):
    id = models.AutoField(primary_key=True)
    disease = models.CharField(max_length=200,null=True)
    medicine = models.CharField(max_length=500,null=True)
    appointments = models.ForeignKey(Appointments, on_delete=models.SET_NULL, blank=True, null=True)

class PageView(models.Model):
    page = models.CharField(max_length=50, blank=False)
    hits = models.IntegerField(default=0)


class PatientReport(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    patientName = models.CharField(max_length=300,null=True)
    upload = models.FileField(upload_to='dmz_imgs/doctor/Reports')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)


