from django.http import HttpResponseRedirect
from DMZ.Decorators.Patient_login import is_patient_login
from django.shortcuts import render 
from ..models import *
from ..forms import *
from math import *
import razorpay
from .api import ApiKey

Users = ''
user_name = ''
Model = ''

Api = ApiKey()

def Diagnostic(request):
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    test = diagnostic_test_list.objects.all()
    combo = combo_diagnostic_test_list.objects.all()
    combo_length = len(combo)
    slides = combo_length//4 + ceil((combo_length/4)-(combo_length//4))
    Doctor_status = request.session.get('Doctor_status')
    TestLength = DignoCartLength(request)
    # Digno_Cart = DignoFetchItems(request)
    # Digno_CartItem = dignostic_test_cartItems.objects.filter(carts=Digno_Cart.id)
    length = len(test)
    print(Api.get("RKey"))
    param = {"TestLength":TestLength,"login":login,"Doctor_status":Doctor_status,'test':test,'length':length,"patient_id":Id,"login":login,"combo":combo,"no_of_slides":slides, "slide_range": range(1,slides),'Dr_length':combo_length,'Range':range(combo_length),'range': range(length),}

    if request.method == 'POST':
        tests = request.POST['test']
        Appointments_date = request.POST['Appointments_date']
        Patient_name = request.POST['Patient_name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        Patient_gender = request.POST['Patient_gender']
        Patient_DOB = request.POST['Patient_DOB']
        Patient_pincode = request.POST['Patient_pincode']
        Patient_adress = request.POST['Patient_adress']

        digonstic = diagnostic_appointment(test=tests,Appointments_date=Appointments_date,Patient_name=Patient_name,mobile=mobile
        ,email=email,Patient_gender=Patient_gender,Patient_DOB=Patient_DOB,Patient_pincode=Patient_pincode,Patient_adress=Patient_adress)
        digonstic.save()

    return render(request,'diagnostic.html',param)

def ComboDignostic(request):
    DiagnoTest = diagnostic_test_list.objects.all()
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        img = request.FILES["img"]
        DignoCombo = request.POST["DignoCombo"]
        count = request.POST['num']
        whoBook = request.POST['whoBook']
        preparation = request.POST['preparation']
        Gender = request.POST['Gender']
        age = request.POST['age']

        combo = combo_diagnostic_test_list(name=name,price=price,image=img,details=DignoCombo,Test_count=count,
                                            Who_should_book_this_checkup=whoBook,What_preparation_is_needed_for_this_Checkup=preparation,
                                            Gender=Gender,Age_Group=age)
        combo.save()
    return render(request, "DignoCombo.html",{"DiagnoTest":DiagnoTest})

def ComboDiagnosticDetails(request,id):
    print(id)
    Test = combo_diagnostic_test_list.objects.get(Id=id)
    param = {"test":Test}
    return render(request ,"DignoComboDetails.html",param)

def DiagnosticDetails(request,id):
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    Test = diagnostic_test_list.objects.get(id=id)
    Id = request.session.get('patient_id')
    # patient = Patient.objects.get(patient_id=Id)
    Digno_Cart , _ = dignostic_test_cart.objects.get_or_create(patient_id = Id)
    Digno_CartItem = ""
    Cartid = ''
    Digno_Cart = DignoFetchItems(request)
    Digno_CartItem = dignostic_test_cartItems.objects.filter(carts=Digno_Cart.id,is_paid=False)
        
    for i in Digno_CartItem:
        Cartid = i.carts.id


    TestLength = DignoCartLength(request)

    total = []

    extra = 0

    DisabledAddToCart = None

    for i in Digno_CartItem:
        total.append(i.Tests.price)
        if i.Tests.id == id:
            DisabledAddToCart = "True"
        if i.Tests.Home_visit == True:
            extra = 100

    total.append(extra)

    param = {"patient_id":Id,"login":login,"Cartid":Cartid,"extra":extra,"DisabledAddToCart":DisabledAddToCart,"Carttotal":sum(total),"TestLength":TestLength,"test":Test,"CartItem":Digno_CartItem}
    return render(request ,"DignoDetails.html",param)

def DignosticForm(request):
    test = 0
    testCart = ''
    totalPrice = 0
    Id = 0
    Idd = request.GET.get('id')
    login = request.session.get('patient_status')
    ComboDiagnoTestID = request.GET.get('ComboID')
    DiagnoTestID = request.GET.get('DignoID')
    CartDiagnoTestID = request.GET.get('CartID')
    Digno_Cart = DignoFetchItems(request)
    

    if ComboDiagnoTestID:
        test = combo_diagnostic_test_list.objects.get(Id=ComboDiagnoTestID)
        Id=ComboDiagnoTestID
        totalPrice = test.price

    elif DiagnoTestID:
        Id=ComboDiagnoTestID
        test = diagnostic_test_list.objects.get(id=DiagnoTestID)
        totalPrice = test.price

    elif CartDiagnoTestID:
        testCart = dignostic_test_cartItems.objects.filter(carts=CartDiagnoTestID,is_paid=False)
        total = []
        for i in testCart:
            i.carts.id
            total.append(i.Tests.price)
            totalPrice = sum(total)


    if request.method == "POST":
        client = razorpay.Client(auth=(Api.get("RKey"), Api.get("RSecretKey")))

        DATA = {
            "amount": totalPrice*100,
            "currency": "INR",
            "receipt": "receipt#1",
            "payment_capture":1
            }
    
        payment = client.order.create(data=DATA)
        payment_id = payment['id']
        DignoBill.objects.create(price=totalPrice,Orders_id=payment_id)


        patient = request.session.get('patient_id')
        Test = Id
        Test_prices = request.POST["Test_price"]
        dates = request.POST["Appointments_date"]
        Appointment_type = request.POST["Appointment_type"]
        Patient_names = request.POST["Patient_name"]
        Patient_mobiles = request.POST["Patient_mobile"]
        Patient_emails = request.POST["Patient_email"]
        Patient_genders = request.POST["Patient_gender"]
        Patient_pincodes = request.POST["Patient_pincode"]
        Patient_adress = request.POST["Patient_adress"]

    
        if ComboDiagnoTestID:
            ComboTestData = diagnostic_appointment(ComboTest_id=ComboDiagnoTestID,patient_id=patient,Price=Test_prices,Appointments_date=dates,Appointments_type=Appointment_type,
                                            Patient_name=Patient_names,Patient_mobile=Patient_mobiles,Patient_email=Patient_emails,
                                            Patient_gender=Patient_genders,Patient_pincode=Patient_pincodes,Patient_adress=Patient_adress,order_id=payment_id)
            ComboTestData.save()
        elif DiagnoTestID:
            SingleTestData = diagnostic_appointment(SingleTest_id=DiagnoTestID,patient_id=patient,Price=Test_prices,Appointments_date=dates,Appointments_type=Appointment_type,
                                            Patient_name=Patient_names,Patient_mobile=Patient_mobiles,Patient_email=Patient_emails,
                                            Patient_gender=Patient_genders,Patient_pincode=Patient_pincodes,Patient_adress=Patient_adress,order_id=payment_id)
            SingleTestData.save()

        elif CartDiagnoTestID:
            SingleTestData = diagnostic_appointment(CartTest_id=CartDiagnoTestID,patient_id=patient,Price=Test_prices,Appointments_date=dates,Appointments_type=Appointment_type,
                                            Patient_name=Patient_names,Patient_mobile=Patient_mobiles,Patient_email=Patient_emails,
                                            Patient_gender=Patient_genders,Patient_pincode=Patient_pincodes,Patient_adress=Patient_adress,order_id=payment_id)
            
            
            SingleTestData.save()
        return render(request,'Razorpay.html',{"login":login,"payment_id":payment_id, 'Id':Idd,'payment':payment,'api_key':Api.get("RKey"),"payment_id":payment_id})
        
    
    return render(request, "diagnosticForm.html" ,{"test":test,"total":totalPrice,"testCart":testCart})

def DignoCart(request):
    Patient = request.session.get('patient_id')
    Digno_Cart , _ = dignostic_test_cart.objects.get_or_create(patient_id = Patient)
    Digno_CartItem = dignostic_test_cartItems.objects.filter(id=Digno_Cart.id)
    login = request.session.get('patient_status')

    totalPrice = []

    for i in Digno_CartItem:
        totalPrice.append(i.Tests.price)

    Total_price = sum(totalPrice)

@is_patient_login
def DignoAddToCart(request,id):
    Test = diagnostic_test_list.objects.get(id=id)
    patient = request.session.get('patient_id')

    Digno_Cart , _ = dignostic_test_cart.objects.get_or_create(patient_id = patient)

    Digno_CartItem = dignostic_test_cartItems(carts=Digno_Cart,Tests=Test)
    Digno_CartItem.save()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DignoCartLength(request):
    length = None
    try:
        id = request.session.get('patient_id')
        patient = Patient.objects.get(patient_id=id)
        Digno_Cart , _ = dignostic_test_cart.objects.get_or_create(patient_id = patient)
        Digno_CartItem = dignostic_test_cartItems.objects.filter(carts=Digno_Cart.id,is_paid=False)
        length = len(Digno_CartItem)
    except:
        length = 0
    return length

def DeleteCartItem(request,id):
    Digno_Cart = DignoFetchItems(request)
    dignostic_test_cartItems.objects.get(carts=Digno_Cart.id,Tests=id,is_paid=False).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DignoFetchItems(request):
    try:
        Id = request.session.get('patient_id')
        # patient = Patient.objects.filter(patient_id=Id)
        Digno_Cart , _ = dignostic_test_cart.objects.get_or_create(patient = Id)
        
    except:
        Digno_Cart , _ = dignostic_test_cart.objects.get_or_create(patient = Id)

    return Digno_Cart