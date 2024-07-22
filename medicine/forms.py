from django import forms
from .models.category import Category

category = Category.objects.all()

class UploadForm(forms.Form):
    medicine_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'validationCustom01' ,'placeholder':"Enter medicines name" }))
    # company_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'validationCustom02' ,'placeholder':"Enter company name"}))
    medicine_quantity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'validationCustom03' ,'placeholder':"Enter medicine quantity "}))
    Total_medicines = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','id':'validationCustom04' ,'placeholder':"Enter Total medicines"}))
    price = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'validationCustom05' ,'placeholder':"Enter medicine price"}))
    price_off = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'validationCustom06' ,'placeholder':"Enter off price"}))
    discription = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'validationCustom07' ,'placeholder':"Enter medicines discription" }))
    uses = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','id':'validationCustom08' ,'placeholder':"Enter medicines uses" }))
    Image1 = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control' ,'id':'validationCustom09'}))
    Image2 = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control' ,'id':'validationCustom10'}))
    Image3 = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control' ,'id':'validationCustom11'}))
    Image4 = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control' ,'id':'validationCustom12'}))


class IdForm(forms.Form):
    medicine_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','id':'medicineID' ,'placeholder':"Enter medicines id" }))
    # medicine_search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'medicineSearch' ,'placeholder':"Enter medicines search" }))

class NameForm(forms.Form):
    medicine_search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'medicineSearch' ,'placeholder':"Enter medicines search" }))

class UpdateForm(forms.Form):
    medicine_quantity = forms.IntegerField(error_messages={'required':'quantity'} ,widget=forms.NumberInput(attrs={'class':'form-control','id':'medicineQuantity' ,'placeholder':"Enter medicines quantity" }))
    medicine_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'medicineQuantity','placeholder':"Enter medicines name" }))
    medicine_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','id':'medicineQuantity' ,'placeholder':"Enter medicines price" }))

class BrandForm(forms.Form):
    Brand_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'medicineQuantity','placeholder':"Enter medicines name" }))