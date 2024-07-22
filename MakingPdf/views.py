# pip install xhtml2pdf
from django.shortcuts import render
from DMZ.models import Appointments, Bill
from medicine.models.order import Orders
from medicine.models.cart import cart, CartItem
from django.http import HttpResponse
from django.template.loader import get_template
from DMZ.models import *
from xhtml2pdf import pisa



# Create your views here.
def AppointmnetPdf(request):
    appointmnet = Appointments.objects.get(Appointments_id=39)
    bill = Bill.objects.get(appointments_id=63)
    print(bill.appointments.Appointments_date)
    param = {"Bill":bill,"Appointments":appointmnet}
    return render(request, "AppointmnetPdf.html",param)

def MedicinePdf(request,id):
    order = Orders.objects.get(Orders_id=id)
    order_d = request.GET.get('id')
    print(order)
   #  Cart = cart.objects.get(id=id)
    Cartitems = CartItem.objects.filter(order=id)
    param = {"order":order,"Cartitem":Cartitems}
    return render(request, "MedicinePdf.html",param)

def render_pdf(request,id):
    appointmnet = Appointments.objects.get(Appointments_id=id)
    bill = Bill.objects.get(appointments_id=id)
    template_path = 'AppointmnetPdf.html'
    context = {"Bill":bill,"Appointments":appointmnet}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def Lab_render_pdf(request,id):
    appointmnet = diagnostic_appointment.objects.get(id=id)
    bill = DignoBill.objects.get(Test=id)
    cart = dignostic_test_cartItems.objects.filter(carts=bill.Test.CartTest)
    template_path = 'Lab_AppointmnetPdf.html'
    context = {"Bill":bill,"Appointments":appointmnet, "cart" : cart}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def Medicine_render_pdf(request):
    id = request.GET.get('id')
    order = Orders.objects.get(Orders_id=id)
    Cartitems = CartItem.objects.filter(order=id)
    template_path = 'MedicinePdf.html'
    total = []
    for i in Cartitems:
        total.append(i.Product.price)
    context = {"total":sum(total),"order":order,"Cartitem":Cartitems }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Medicinereport.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
