from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from functools import wraps

def is_doctor_login(function):
    def abcd(request, *args, **kw):
        if (request.session.get('Doctor_status') != "Login"):
            return HttpResponseRedirect("/Login/")
        else:
            return function(request, *args, **kw)
    return abcd
