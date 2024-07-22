
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from ..models import *
from medicine.models.order import Orders
from medicine.models.cart import cart, CartItem
from medicine.models.products import Products
from ..forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from math import *
import os


Users = ''
user_name = ''
Model = ''

def Admin_dashboard1(request):
        return render(request,'Admin_dashboard_comman.html')

@login_required(login_url='login')
def Admin_dashboard(request):
    patient = Patient.objects.filter(status="Login")
    doctor = Doctor.objects.filter(status="Login")
    patient_ = Patient.objects.all()
    doctor_ = Doctor.objects.all()
    medicine = Products.objects.all()

    Total_medicines = []
    Expected_Total_medicines = []
    ids = []

    for i in medicine:
        Total_medicines.append(i.Total_medicines)
        ids.append(i.Id)
        Expected_Total_medicines.append(i.Expected_Total_medicines)

    Question = QNA.objects.all()
    Specilaity = specilaity.objects.all()
    appointment = Appointments.objects.all()
    product = Products.objects.all()
    home_care = homeCare.objects.all()
    Pending_appointments = Appointments.objects.filter(appointment_status="pending")
    Pending_Q = QNA.objects.filter(complete=False)
    complete_appointments = Appointments.objects.filter(appointment_status="complete")

    Lab_appointment = diagnostic_appointment.objects.all()
    Pending_Labappointments = diagnostic_appointment.objects.filter(visiting="pending")
    complete_Labappointments = diagnostic_appointment.objects.filter(visiting="visited")

    patient_length = len(patient_)
    doctor_length = len(doctor_)
    QNA_length = len(Question)
    appointment_length = len(appointment)
    length_Pending_appointments  = len(Pending_appointments)
    length_complete_appointments = len(complete_appointments)
    Labappointment_length = len(Lab_appointment)
    length_Pending_Labappointments  = len( Pending_Labappointments)
    length_complete_LAbappointments = len(complete_Labappointments)
    Lenghtproduct = len(product)
    Lenghthome_care = len(home_care)
    LenghtQ = len(Pending_Q)

    MedicineOrderPending = Orders.objects.filter(status="Order Received")
    MedicineOrder = Orders.objects.all()
    MedicineOrderLnt = len( MedicineOrder)
    MedicineOrderLength = len(MedicineOrderPending)

    page = request.GET.get('page',1)
    paginator = Paginator(patient,5)

    try:
        patient = paginator.page(page)
    except PageNotAnInteger:
        patient = paginator.page(1)
    except EmptyPage:
        patient = paginator.page(paginator.num_pages)
        

        
    param = {"MedicineOrderLnt":MedicineOrderLnt,"MedicineOrderLength":MedicineOrderLength,"MedicineOrderPending":MedicineOrderPending,"complete_Labappointments":complete_Labappointments,"Pending_Labappointments":Pending_Labappointments,"length_complete_LAbappointments":length_complete_LAbappointments,"length_Pending_Labappointments":length_Pending_Labappointments,"Labappointment_length":Labappointment_length,"Expected_Total_medicines":Expected_Total_medicines,"ids":ids,"medicine":Total_medicines,"LenghtQ ":LenghtQ ,"Lenghthome_care":Lenghthome_care,"Lenghtproduct":Lenghtproduct,"Specilaity":Specilaity,'complete_appointments':length_complete_appointments,'Pending_appointments':length_Pending_appointments,'QNA_length':QNA_length,'appointment_length':appointment_length,'appointment':appointment,'patient':patient,'doctor':doctor,'patient_length':patient_length,'doctor_lengths':doctor_length}
    return render(request,'Admin_dashboard.html',param)

@login_required(login_url='login')
def Admin_dashboard_doctorLogin(request):
    return render(request,'Admin_dashboard_doctorLogin.html')
    
@login_required(login_url='login')
def Admin_dashboard_doctor(request):
    doctor = None
    doctors = Doctor.objects.all()
    Specilaity = specilaity.objects.all()
    
    Specilaist = request.GET.get('SpecialisID')

    if Specilaist:
        doctor = Doctor.objects.filter(doctor_profession=Specilaist)
    else:
        doctor = Doctor.objects.all()
        

    page = request.GET.get('page',1)
    paginator = Paginator(doctor,10)

        

    Dr_length = len(doctor)

    try:
        doctor = paginator.page(page)
    except PageNotAnInteger:
        doctor = paginator.page(1)
    except EmptyPage:
        doctor = paginator.page(paginator.num_pages)


    if request.method == "POST":
        search = request.POST.get('search')
        drop = request.POST.get('drop')
        if search != None:
            doctor = Doctor.objects.filter(doctor_category__icontains=search) or Doctor.objects.filter(doctor_name__icontains=search)
        if drop != None:
            doctor = Doctor.objects.filter(doctor_category__icontains=drop) or Doctor.objects.filter(doctor_name__icontains=drop)
    param = {'Specilaity':Specilaity,'Dr_length':Dr_length,'Range':range(Dr_length),'doctor':doctor,'doctors':doctors}
    return render(request,'Admin_dashboard_doctor.html',param)

@login_required(login_url='login')
def Admin_dashboard_patient(request):
    blood = request.GET.get("Blood")
    patient = Patient.objects.all()
    patients = Patient.objects.all()
    login = Patient_login.objects.all()
    pt_length = len(patient)+1

    details = Patient_login.objects.all()
    if blood:
        if blood == 'A':
            patient = Patient.objects.filter(patient_Blood="A+")
        elif blood == 'B':
            patient = Patient.objects.filter(patient_Blood="B+")
        elif blood == 'AB':
            patient = Patient.objects.filter(patient_Blood="AB+")
        elif blood == 'O':
            patient = Patient.objects.filter(patient_Blood="O+")
        else:
            patient = Patient.objects.filter(patient_Blood=blood)

    page = request.GET.get('page',1)
    paginator = Paginator(patient,5)

    try:
        patient = paginator.page(page)
    except PageNotAnInteger:
        patient = paginator.page(1)
    except EmptyPage:
        patient = paginator.page(paginator.num_pages)

    if request.method == "POST":
        search = request.POST.get('search')
        drop = request.POST.get('drop')
        if search != None:
            patient = Patient.objects.filter(patient_name__icontains=search) or Patient.objects.filter(patient_sex=search)
        elif drop != None:
            patient = Patient.objects.filter(patient_Blood=drop) 
    param = {'details':details,'login':login,'pt_length':pt_length,'Range':range(pt_length),'patient':patient}
    return render(request,'Admin_dashboard_patient.html',param)

@login_required(login_url='login')
def patient_details(request):
    id = request.GET.get("id")
    patient = Patient.objects.get(patient_id=id)
    return render(request, 'Admin_patient_details.html',{"patient":patient})

@login_required(login_url='login')   
def doctor_details(request):
    id = request.GET.get("id")
    doctor = Doctor.objects.get(doctor_id=id)
    return render(request, 'Admin_doctor_details.html',{"doctor":doctor})

@login_required(login_url='login')
def admin_edit_doctor(request,doctor_id):
    doctor = Doctor.objects.filter(doctor_id=doctor_id)
    doctors = Doctor.objects.get(doctor_id=doctor_id)
    length = len(doctor)

    if request.method == 'POST':
        fullName = request.POST['fullName']
        gender = request.POST['gender']
        Address = request.POST['Address']
        Area = request.POST['Area']
        ciTy = request.POST['ciTy']
        sTate = request.POST['sTate']
        country = request.POST['country']
        zip = request.POST['zip']
        Cname = request.POST['Cname']
        Caddress = request.POST['Caddress']
        Carea = request.POST['Carea']
        Ccity = request.POST['Ccity']
        Cstate = request.POST['Cstate']
        Ccountry = request.POST['Ccountry']
        Czip = request.POST['Czip']
        Ctele = request.POST['Ctele']

        Doctor.objects.filter(doctor_id=doctor_id).update(doctor_name=fullName,doctor_sex=gender,doctor_address=Address,doctor_city=ciTy,
                                                            doctor_state=sTate,doctor_zip=zip,doctor_country=country,doctor_area=Area,
                                                            hosptial_name=Cname,hospital_address=Caddress,hosptial_area=Carea,hosptial_city=Ccity,hosptial_state=Cstate,
                                                            hosptial_country=Ccountry,hosptial_pincode=Czip,hosptial_telephone=Ctele)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    param = {'doctor':doctor[0], 'length':length}
    return render(request, 'admin_edit_doctor.html',param)

@login_required(login_url='login')
def admin_edit_Patient(request,patient_id):
    # patients = Patient.objects.filter(patient_id=patient_id)
    patients = Patient.objects.get(patient_id=patient_id)
    Data = None
    if request.method == "POST":
        name = request.POST['name']
        # Dob = request.POST['dob']
        Gender = request.POST['Gender']
        # phone = request.POST['phone']
        patient_blood = request.POST['patient_blood']
        Add = request.POST['Add']
        Area = request.POST['Area']
        City = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zip = request.POST['zip']

        Data = Patient.objects.filter(patient_id=patient_id)
        Data.update(patient_name=name, patient_sex=Gender,
        patient_Blood=patient_blood, patient_address=Add,patient_city=City,patient_state=state,patient_zip=zip,patient_country=country,patient_area=Area)
        if Data:
            messages.success(request,"Update profile sucessfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        


    param = {'patient':patients,"Data":Data}
    return render(request, 'admin_edit_patient.html',param)

def Admin_specialist(request):
    Specilaity = specilaity.objects.all()
    return render(request,'Admin_specialist.html',{"Specialist":Specilaity,"Length":len(Specilaity)})

@login_required(login_url='login')
def admin_dashboard_appointmnet(request):
    TYPE = request.GET.get("TYPE")
    status = request.GET.get("status")
    Qlength = None
    Appointment = Appointments.objects.all()
    Pending_appointments = Appointments.objects.filter(appointment_status="pending")
    complete_appointments = Appointments.objects.filter(appointment_status="complete")
    length_Pending_appointments  = len(Pending_appointments)
    length_complete_appointments = len(complete_appointments)
    length = len(Appointment)

    if TYPE:
        Appointment = Appointments.objects.filter(Appointments_type=TYPE)
        Qlength = len(Appointment)

    if status:
        Appointment = Appointments.objects.filter(appointment_status=status)
        Qlength = len(Appointment)

    if request.method == 'POST':
        id = request.POST['Id']
        # check = request.POST["check"]
        Appointments.objects.filter(Appointments_id=id).update(appointment_status="complete")
    param = {"Qlength":Qlength,'appointment':Appointment,'complete_appointments':length_complete_appointments,'Pending_appointments':length_Pending_appointments,'length':length}
    return render(request,"Admin_dashboard_appointment.html",param)
    
@login_required(login_url='login')
def Admin_dash_test_appointment(request):
    TYPE = request.GET.get("TYPE")
    status = request.GET.get("status")
    Qlength = None
    Appointment = diagnostic_appointment.objects.all()
    Pending_appointments = diagnostic_appointment.objects.filter(visiting="pending")
    complete_appointments = diagnostic_appointment.objects.filter(visiting="Visited")
    length_Pending_appointments  = len(Pending_appointments)
    length_complete_appointments = len(complete_appointments)
    length = len(Appointment)

    statusRequest = request.GET.get('status')
    id = request.GET.get('id')
    if statusRequest:
        diagnostic_appointment.objects.filter(id=id).update(visiting=statusRequest)

    if TYPE:
        Appointment = diagnostic_appointment.objects.filter(Appointments_type=TYPE)
        Qlength = len(Appointment)

    if status:
        Appointment = diagnostic_appointment.objects.filter(visiting=status)
        Qlength = len(Appointment)

    if request.method == 'POST':
        id = request.POST['Id']
        # check = request.POST["check"]
        Appointments.objects.filter(Appointments_id=id).update(appointment_status="complete")
    param = {"Qlength":Qlength,'appointment':Appointment,'complete_appointments':length_complete_appointments,'Pending_appointments':length_Pending_appointments,'length':length}
    return render(request,"Admin_dash_test_appointment.html",param)
    
def Admin_LabTest_Upload(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        Gender = request.POST['Gender']
        age = request.POST['age']
        Visit = request.POST['Visit']
        file = request.FILES['file']
        preparation = request.POST['preparation']
        Who_should_book_this_checkup = request.POST['Who_should_book_this_checkup']

        diagnostic_test_list(name=name,price=price,Who_should_book_this_checkup=Who_should_book_this_checkup,What_preparation_is_needed_for_this_Checkup=preparation,
                                Age_Group=age,Gender=Gender,image=file,Home_visit=Visit).save()
        messages.success(request,f'{name} Test is Submited')
    return render(request, 'Admin_labtest_upload.html')

def Admin_Update_test(request,id):
    Test = diagnostic_test_list.objects.get(id=id)
    if request.method == 'POST':
        selection = request.POST["selection"]
        update = request.POST['update']
        if selection == 'Test Name':
            diagnostic_test_list.objects.filter(id=id).update(name=update)
        elif selection == 'price':
            diagnostic_test_list.objects.filter(id=id).update(price=update)
        elif selection == 'Gender':
            diagnostic_test_list.objects.filter(id=id).update(Gender=update)
        elif selection == 'Age group':
            diagnostic_test_list.objects.filter(id=id).update(Age_Group=update)
        elif selection == 'visit':
            diagnostic_test_list.objects.filter(id=id).update(Home_visit=update)
        elif selection == 'Medicine Description':
            diagnostic_test_list.objects.filter(id=id).update(What_preparation_is_needed_for_this_Checkup=update)
        elif selection == 'Medicine Uses':
            diagnostic_test_list.objects.filter(id=id).update(Who_should_book_this_checkup=update)

        messages.success(request,f'Update {selection} = {update} successfully')

        return redirect(f'/Admin_Update_test/{id}')
    
    param = {"Test":Test}
    return render(request,'Test_update.html',param)

def Admin_combo_test(request):
    test = None
    gender = request.GET.get('gender')
    if gender:
        test = combo_diagnostic_test_list.objects.filter(Gender=gender)
    else:
        test = combo_diagnostic_test_list.objects.all()
    length = len(test)
    param = {'test':test,'length':length}
    return render(request, 'Admin_combo_test.html',param)

def Admin_combo_Edit(request,id):
    test = combo_diagnostic_test_list.objects.get(Id=id)
    DiagnoTest = diagnostic_test_list.objects.all()
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        DignoCombo = request.POST["DignoCombo"]
        count = request.POST['num']
        whoBook = request.POST['whoBook']
        preparation = request.POST['preparation']
        Gender = request.POST['Gender']
        age = request.POST['age']

        combo_diagnostic_test_list.objects.filter(Id=id).update(name=name,price=price,details=DignoCombo,Test_count=count,
                                            Who_should_book_this_checkup=whoBook,What_preparation_is_needed_for_this_Checkup=preparation,
                                            Gender=Gender,Age_Group=age)
        
        messages.success(request, f"{name} Test updated successfully")
        return redirect(f'/Admin_combo_Edit/{id}')
        
    param = {'test':test,'DiagnoTest':DiagnoTest}
    return render(request,'Edit_combo_test.html',param)

def Admin_dash_test(request):
    test = diagnostic_test_list.objects.all()
    return render(request, "Admin_dash_test.html" , {"test":test})

@login_required(login_url='login')
def admin_bill(request):
    bill = Bill.objects.all()
    order = Orders.objects.all()
    MedicineCart = cart.objects.all()
    param = {"order":order,"Bill":bill,"MedicineCart":MedicineCart}
    return render(request,"admin_bill.html",param)

    # delete operation

@login_required(login_url='login')
def admin_dashboard_homeCare(request):
    Homecare = homeCare.objects.all()
    id = request.GET.get('id')
    status = request.GET.get('status')
    homeCare.objects.filter(id=id).update(status=status)
    param = {"Homecare":Homecare}
    return render(request,"Admin_dashboard_homeCare.html",param)

@login_required(login_url='login')
def admin_dashboard_QNA(request):
    answer = request.GET.get('answer')
    Qna = QNA.objects.all()
    questionForm = question()
    answerForm = QNA_Answer()

    if answer:
        Qna = QNA.objects.filter(complete=answer)
    
    questions = None
    id = None
    if request.method == "POST":
        Q_Form = question(request.POST)
        A_Form = QNA_Answer(request.POST)
        if Q_Form.is_valid():
            id = request.POST['id']
            try:
                questions = QNA.objects.get(id=id)
            except:
                messages.error(request, 'Question id is not valid')

        if A_Form.is_valid():
            answer = request.POST['Answer']
            id = request.POST['id']
            questions = QNA.objects.filter(id=id)
            questions.update(Answer=answer,complete=True)
            messages.success(request, f'Question {id} Updated successfully.')
    


    param = {"Qna":Qna,"Question":questions,"questionForm":questionForm,"answerForm":answerForm}
    return render(request,'Admin_dashboard_QNA.html',param)

@login_required(login_url='login')
def UpdateMedicine(request,id):
    medicine = Products.objects.get(Id=id)
    if request.method == "POST":
        selection = request.POST["selection"]
        update = request.POST["medicineValue"]
        if selection == 'Medicine Name':
            Products.objects.filter(Id=id).update(medicine_name=update)
        elif selection == 'Medicine Qunatity':
            Products.objects.filter(Id=id).update(medicine_quantity=update)
        elif selection == 'Product Qunatity':
            Products.objects.filter(Id=id).update(Total_medicines=update)
        elif selection == 'Price':
            Products.objects.filter(Id=id).update(price=update)
        elif selection == 'Price off':
            Products.objects.filter(Id=id).update(price_off=update)
        elif selection == 'Medicine Description':
            Products.objects.filter(Id=id).update(discription=update)
        elif selection == 'Medicine Uses':
            Products.objects.filter(Id=id).update(uses=update)

    param = {"medicine":medicine}
    return render(request, 'MedicineUpdate.html' ,param)

@login_required(login_url='login')
def deletePt(request,Id):
    delete_data = Patient.objects.get(patient_id=Id)
    delete_data.delete()
    messages.success(request,"File delete successfully...!!!")
    os.remove(delete_data.patient_profile.path)
    return redirect("/Admin_dash_patient")

@login_required(login_url='login')
def deleteDr(request,Id):
    delete_data = Doctor.objects.get(doctor_id=Id)
    delete_data.delete()
    messages.success(request,"File delete successfully...!!!")
    os.remove(delete_data.doctor_profile.path)
    return redirect("/Admin_dash_doctor")

def deleteHome(request):
    id = request.GET.get('id')
    homeCare.objects.get(id=id).delete()
    messages.success(request,'HomeCare Delete Succesfully')
    return redirect('/Admin_dash_homerCare')

def deleteSingleTest(request,id):
    diagnostic_test_list.objects.get(id=id).delete()
    messages.success(request,"Test deleted Successfully")
    return redirect('/Admin_dash_test/')

def deleteComboTest(request,id):
    diagnostic_test_list.objects.get(id=id).delete()
    messages.success(request,"Test deleted Successfully")
    return redirect('/deleteComboTest/')

def deleteAppointmentBill(request,id):
    Bill.objects.get(Bill_number=id).delete()
    messages.success(request,"Appointment Bill Deleted Successfully")
    return redirect('/admin_bill/')

def deleteMedicineBill(request,id):
    Orders.objects.get(Orders_id=id).delete()
    messages.success(request,"Medicine Order Bill Deleted Successfully")
    return redirect('/admin_bill/')

def deleteAppointment(request,id):
    Appointments.objects.get(Appointments_id=id).delete()
    messages.success(request,"Appointment Deleted Successfully")
    return redirect('/Admin_dash_appointment/')

def admin_logout(request):
    logout(request)
    messages.success(request,"Admin Logout Successfully")
    return redirect('/Login/')