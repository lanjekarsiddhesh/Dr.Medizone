from django.http import HttpResponseRedirect

def is_patient_login(function):
    def wrapper(request, *args, **kw):
        if request.session.get('patient_status') != "Login":
            return HttpResponseRedirect("/Login/")
        else:
            return function(request, *args, **kw)
    return wrapper