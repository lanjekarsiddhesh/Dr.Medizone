from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from DMZ.Decorators.Patient_login import is_patient_login
from .forms import *
from .models.products import Products
from .models.Review import Reviews
from .models.cart import cart, CartItem
from .models.order import Orders
from .models.brand import Brand
from .models.favouriteProduct import wishlist, wishlistItem
from DMZ.models import Patient
from math import ceil
import razorpay
from DMZ.views.api import ApiKey

# Create your views here.

Api = ApiKey()

def lengthCart(request):
    length = None
    try:
        id = request.session.get('patient_id')
        user1 = Patient.objects.get(patient_id=id)
        carts , _ = cart.objects.get_or_create(patient_id = user1.patient_id, is_paid = False)
        cartItems = CartItem.objects.filter(carts_id=carts.id,is_paid = False)
        length = len(cartItems)
    except:
        length = 0
    return length
    
def lengthWishlists(request):
    length = None
    try:
        id = request.session.get('patient_id')
        user1 = Patient.objects.get(patient_id=id)
        wishlists , _ = wishlist.objects.get_or_create(patient_id = user1.patient_id)
        wishlistItems = wishlistItem.objects.filter(WishlistProduct_id=wishlists.id)
        length = len(wishlistItems)
    except:
        length = 0
    return length

def quantity():
    brand = Brand.objects.all()
    lent = len(brand)+1
    for i in range(1,lent):
        length = len(Products.objects.filter(company_id=i))
        Brand.objects.filter(Id=i).update(Quantity=length)

def index(request):
    Id = request.session.get('patient_id')
    medicine = Products.objects.all()
    category = Category.objects.all()
    login = request.session.get('patient_status')

    length_cart = lengthCart(request)

    length_wishlist = lengthWishlists(request)

    allMedicine = []
    categoryMedicine = Products.objects.values('category','Id')
    cats = {item['category'] for item in categoryMedicine}
    for cat in cats:
        medicineProd = Products.objects.filter(category=cat)
        allMedicine.append(medicineProd)

    length = len(medicine)
    nslide = length//4 + ceil((length/4)-(length//4))
    param = {"id":Id,"login":login,"wishlist_length":length_wishlist,"cart_length":length_cart,"allMedicine":allMedicine, "no_of_slides":nslide, "range":range(nslide), "medicine":medicine,"category":category}
    return render(request, 'medicineHome.html',param)

def Upload(request):
    Id = request.session.get('patient_id')
    myForm = UploadForm()
    idForm = IdForm()
    nameForm = NameForm()
    updateForm = UpdateForm()
    category = Category.objects.all()
    brand = Brand.objects.all()
    medicine = Products.objects.all()
    
    if request.method == "POST":
        MyForm = UploadForm(request.POST,request.FILES)
        Idform = IdForm(request.POST)
        NameForms = NameForm(request.POST)
        updateform = UpdateForm(request.POST)
        if MyForm.is_valid():
            name = request.POST['medicine_name']
            company_name = request.POST['company_name']
            medicine_quantity = request.POST['medicine_quantity']
            Total_medicines = request.POST['Total_medicines']
            price = request.POST['price']
            price_off = request.POST['price_off']
            discription = request.POST['discription']
            uses = request.POST['uses']
            categorys = request.POST['category']
            Image1 = request.FILES['Image1']
            Image2 = request.FILES['Image2']
            Image3 = request.FILES['Image3']   
            Image4 = request.FILES['Image4']

            product = Products(category_id=categorys, medicine_name=name,company_id=company_name,medicine_quantity=medicine_quantity,Total_medicines=Total_medicines,
            price=price,price_off=price_off,discription=discription,uses=uses,Image1=Image1,Image2=Image2,Image3=Image3,Image4=Image4)

            product.save()
            messages.success(request,"Medicine Upload Successfully")
            quantity()
            return redirect('/medicineshop/upload/')

        if Idform.is_valid():
            search = request.POST['medicine_id']
            # search_by = request.POST['medicine_search']
            if search != None:
                medicine = Products.objects.filter(Id=search) 
                print(medicine)
            # if search_by != None:
            #     medicine = Products.objects.filter(medicine_name__icontains=search) or Products.objects.filter(category__icontains=search) or Products.objects.filter(company__icontains=search)
        
        if NameForms.is_valid():
            search = request.POST['medicine_search']
            # search_by = request.POST['medicine_search']
            if search != None:
                medicine = Products.objects.filter(medicine_name__icontains=search) 
                print(medicine)
            # if search_by != None:
            #     medicine = Products.objects.filter(medicine_name__icontains=search) or Products.objects.filter(category__icontains=search) or Products.objects.filter(company__icontains=search)
        


            
    param = {"id":Id,'length': len(medicine),'medicine':medicine,'brand':brand,'updateForm':updateForm,'idForm':idForm,'nameForm':nameForm,'myForm':myForm,"category":category}
    return render(request,'upload.html',param)

def product_details(request,id):
    Id = request.session.get('patient_id')
    login = request.session.get('patient_status')
    medicine = Products.objects.get(Id=id)
    user = Patient.objects.filter(status='Login')
    reviews = Reviews.objects.filter(product_id=id)
    # user1 = Patient.objects.get(status='Login')
    user1 = request.session.get('patient_id')

    
    length = len(reviews)

    length_cart = lengthCart(request)

    length_wishlist = lengthWishlists(request)

    overall_star(id)
    
    if request.method == "POST":
        product = id
        patient = user1
        product_img = request.FILES['img']
        subject = request.POST['sub']
        review = request.POST['review']
        rating = request.POST['rating']

        review = Reviews(product_id=product,patient_id=patient,product_img=product_img,subject=subject,review=review,rating=rating)
        review.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    overall_star(id)
    category = Category.objects.all()
    param = {"id":Id,"login":login,"wishlist_length":length_wishlist,"cart_length":length_cart,"length_review":length,"reviews":reviews, "user":user,"medicine":medicine,"category":category}
    return render(request,'product-details.html',param)

@is_patient_login
def add_to_cart(request,id):
    product = Products.objects.get(Id=id)
    patient = request.session.get('patient_id')

    Cart , _ = cart.objects.get_or_create(patient_id = patient, is_paid = False)
    # Cart , _ = cart.objects.get_or_create(patient_id = patient.patient_id, is_paid = False)

    cart_item = CartItem(carts=Cart, Product=product)
    cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@is_patient_login
def add_to_wishlist(request,id):
    product = Products.objects.get(Id=id)
    patient = request.session.get('patient_id')

    Productwishlist , _ = wishlist.objects.get_or_create(patient_id = patient)

    wishlist_item = wishlistItem(WishlistProduct=Productwishlist, Product=product)
    wishlist_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@is_patient_login
def Mycart(request):
    Id = request.session.get('patient_id')
    # user1 = Patient.objects.get(status='Login')
    user1 = request.session.get('patient_id')
    carts , _ = cart.objects.get_or_create(patient_id = user1, is_paid = False)
    cartItems = CartItem.objects.filter(carts_id=carts.id,is_paid = False)
    login = request.session.get('patient_status')

    length_cart = lengthCart(request)

    length_wishlist = lengthWishlists(request)

    total = []
    
    if request.method == 'POST':
        NAME = request.GET.get('id')
        quantity = request.POST[NAME]
        id = request.POST["Id"]
        print(CartItem.objects.filter(Product_id=id))
        print(quantity)

    for i in cartItems:
        total.append(i.Product.price)

    Total_price = sum(total)
    
    cart.objects.filter(patient_id = user1, is_paid = False).update(total=Total_price)

    param = {"id":Id,"login":login,"Id":carts.id,"total":Total_price,"wishlist_length":length_wishlist,"cart_length":length_cart,'Mycart':cartItems}
    return render(request,'cart.html',param)

@is_patient_login
def MyWishlist(request):
    user1 = request.session.get('patient_id')
    wishlists , _ = wishlist.objects.get_or_create(patient_id = user1)
    wishlistItems = wishlistItem.objects.filter(WishlistProduct_id=wishlists.id)
    login = request.session.get('patient_status')

    length_cart = lengthCart(request)

    length_wishlist = lengthWishlists(request)

    total = []
    for i in wishlistItems:
        total.append(i.Product.price)
    Total_price = sum(total)
    wishlist.objects.filter(patient_id = user1).update(total=Total_price)

    param = {"login":login,"Id":wishlists.id,"total":Total_price,"wishlist_length":length_wishlist,"cart_length":length_cart,'MyWishlist':wishlistItems}
    return render(request,'wishlist.html',param)

@is_patient_login
def Checkout(request):
    Id = request.session.get('patient_id')
    # user1 = Patient.objects.get(status='Login')
    RAZORPAY_API_KEY = Api.get("RKey")
    RAZORPAY_API_SECRET_KEY = Api.get("RSecretKey")
    login = request.session.get('patient_status')
    Id = request.GET.get('id')
    cartItems = CartItem.objects.filter(carts_id=Id,is_paid = False)
    # length_cart = len(cartItems)
    Cart = cart.objects.get(id=Id)
    # wishlists , _ = wishlist.objects.get_or_create(patient_id = user1.patient_id)
    # wishlistItems = wishlistItem.objects.filter(WishlistProduct_id=wishlists.id)
    # length_wishlist = len(wishlistItems)
    # cartItems = CartItem.objects.filter(carts_id=Id)

    length_cart = lengthCart(request)

    length_wishlist = lengthWishlists(request)

    if request.method == "POST":
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        DATA = {
                "amount": Cart.total*100,
                "currency": "INR",
                "receipt": "receipt#1",
                "payment_capture":1
                }
                
        payment = client.order.create(data=DATA)
        payment_id = payment['id']
        Orders.objects.create(price=Cart.total,Orders_id=payment_id,Cart_id=Id)
        return render(request,'Mrazorpay.html',{"login":login,"wishlist_length":length_wishlist,"payment_id":payment_id,"cart_length":length_cart,'Id':Id,'payment':payment,'api_key':RAZORPAY_API_KEY})

    param = {"id":Id,'total':Cart.total,'cart':cartItems}
    return render(request, 'checkout.html',param)

@csrf_exempt
def success(request):
    payment = request.POST
    Id = request.GET.get('id')
    order_d = request.GET.get('order')
    for key, val in payment.items():
        order_id = ""
        if key == 'razorpay_order_id':
            order_id += val
            order = Orders.objects.filter(Orders_id= order_id).first()
            carItems = CartItem.objects.filter(carts_id=Id,is_paid=False)

            for i in carItems:
                carItem = CartItem.objects.filter(Product_id=i.Product.Id,carts_id=Id,is_paid=False)

                product = Products.objects.get(Id=i.Product.Id)
                quantity = product.Total_medicines
                value = quantity-len(carItem)
                product_of_quantity = Products.objects.filter(Id=i.Product.Id)
                product_of_quantity.update(Total_medicines=value)

                carItem.update(is_paid=True,order=order_d)

        if key == 'razorpay_signature':
            razorpay_signature = val

   
    order.signature =razorpay_signature
    order.is_paid = True
    order.save()
    print(order.signature)
    messages.success(request, "your order is confirmed !!!")
    # redirect(f'/MakingPdf/createMedicine/?id={order.Orders_id}')
    return render(request,'Msuccess.html',{"id":order.Orders_id,})

def MedicineproductPage(request):
    Id = request.session.get('patient_id')
    # user1 = Patient.objects.get(status='Login')
    medicine = None
    product = None
    category = Category.objects.all()
    brand = Brand.objects.all()
    login = request.session.get('patient_status')

    length_cart = lengthCart(request)

    length_wishlist = lengthWishlists(request)

    Cat = request.GET.get('cat')
    brandId = request.GET.get('brand')
    star = request.GET.get('star')

    if Cat:
        product = Products.objects.filter(category_id=Cat)
    elif brandId:
        product = Products.objects.filter(company_id=brandId)
    elif star:
        product = Products.objects.filter(overall_rating__gte=star)
    else:
        product = Products.objects.all()
    

    if request.method == "POST":
            search = request.POST.get('Searches')
            if search != None:
                product = Products.objects.filter(medicine_name__icontains=search) or Products.objects.filter(category__icontains=search)

    quantity()
    param = {"id":Id,"login":login,"length":len(brand),"brand":brand,"wishlist_length":length_wishlist,"cart_length":length_cart,"products":product,"category":category}
    return render(request, "MedicineShop.html",param)

def overall_star(Products_id):
    Product = Products.objects.filter(Id=Products_id)
    one = len(Reviews.objects.filter(product=Products_id,rating=1))
    one_half = len(Reviews.objects.filter(product=Products_id,rating=1.5))
    two = len(Reviews.objects.filter(product=Products_id,rating=2))
    two_half = len(Reviews.objects.filter(product=Products_id,rating=2.5))
    three = len(Reviews.objects.filter(product=Products_id,rating=3))
    three_half = len(Reviews.objects.filter(product=Products_id,rating=3.5))
    four = len(Reviews.objects.filter(product=Products_id,rating=4))
    four_half = len(Reviews.objects.filter(product=Products_id,rating=4.5))
    five = len(Reviews.objects.filter(product=Products_id,rating=5))

    if  one > one_half or one > two or one > two_half or one > three or one > three_half or one > four or one > four_half or one > five:
        Product.update(overall_rating=1.0)

    if two > one or two > one_half or two > two_half or two > three or two > three_half or two > four or two > four_half or two > five:
        Product.update(overall_rating=2.0)

    if three > one or three > one_half or three > two or three > two_half or three > three_half or three > four or three > four_half or three > five:
        Product.update(overall_rating=3.0)

    if four > one or four > one_half or four > two or four > two_half or four > three or four > three_half or four > four_half or four > five:
        Product.update(overall_rating=4.0)

    if five > one or five > one_half or five > two or five > two_half or five > three or five > three_half or five > four or five > four_half:
        Product.update(overall_rating=5.0)

        # half's

    if four_half > one or four_half > one_half or four_half > two or four_half > two_half or four_half > three or four_half > three_half or four_half > four or four_half > five:
         Product.update(overall_rating=4.5)

    if three_half > one or three_half > one_half or three_half > two or three_half > two_half or three_half > three or three_half > four or three_half > four_half or three_half > five:
        Product.update(overall_rating=3.5)

    if two_half > one or two_half > one_half or two_half > two or two_half > three or two_half > three_half or two_half > four or two_half > four_half or two_half > five:
        Product.update(overall_rating=2.5)

    if one_half > one or one_half > two or one_half > two_half or one_half > three or one_half > three_half or one_half > four or one_half > four_half or one_half > five:
        Product.update(overall_rating=1.5)

def RemoveCartitem(request,id):
    user1 = request.session.get('patient_id')
    print(user1)
    carts = cart.objects.get(patient_id = user1)
    print(carts)
    print(carts.id)
    CartItem.objects.get(carts_id=carts.id,Product_id=id,is_paid=0).delete()
    messages.success(request, 'Item remove From Cart')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deleteMedicine(request,id):
    Products.objects.filter(Id=id).delete()
    messages.success(request,"Medicine Deleted Successfully")
    return redirect('/medicineshop/upload/')
