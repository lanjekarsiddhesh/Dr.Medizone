from django import forms

class otp(forms.Form):
    mob_otp = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'validationDefaultdoctormobotp' ,'placeholder':"Enter Mobile otp here" }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'validationDefaultmobile' ,'placeholder':"Enter Mobile number here" }))
    email_otp = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control otp','id':'validationDefaultdoctorotp' ,'placeholder':"Enter email otp here" }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control ','id':'validationDefaultemail' ,'placeholder':"Enter email here" }))


# admin QNA
class question(forms.Form):
    id = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control me-2' ,'placeholder':"Enter Question Id here",'aria-label':"Search","style":"height: 30px;" }))

class QNA_Answer(forms.Form):
    Answer = forms.CharField(widget=forms.Textarea(attrs={'id':'textarea1' ,'placeholder':"Enter Your Text..."}))