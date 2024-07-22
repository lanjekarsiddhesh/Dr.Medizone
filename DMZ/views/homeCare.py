
from django.shortcuts import render 
from ..models import *
from ..forms import *
from math import *

Users = ''
user_name = ''
Model = ''

def HomeCare(request):
    login = request.session.get('patient_status')
    Id = request.session.get('patient_id')
    Doctor_status = request.session.get('Doctor_status')
    homeCares = homeCare_page.objects.all()
    homeCare_length = len(homeCares)
    param = {"Doctor_status":Doctor_status,"Id":Id,"login":login,'homeCare_length': homeCare_length, 'homeCare':homeCares}
    if request.method == 'POST':
        names = request.POST['name']
        services = request.POST['service']
        mobiles = request.POST['mobile']
        emails = request.POST['email']
        address1s = request.POST['address1']
        address2s = request.POST['address2']
        address = address1s+" "+address2s
        Reason = request.POST['Reason']
        pincodes = request.POST['pin']
        patient = request.session.get('patient_id')

        homeCaress = homeCare(patient=patient,name=names,service=services,mobile=mobiles,email=emails,address=address, pincode= pincodes,Reason=Reason)
        homeCaress.save()

    return render(request,'home_care.html',param)