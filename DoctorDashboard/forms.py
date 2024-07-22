from django import forms

class MyFileForm(forms.Form):
    pid = forms.CharField(widget=forms.TextInput(attrs={'class':'col m-2','id':"Pnum" ,"hidden":True }))
    Did = forms.CharField(widget=forms.TextInput(attrs={'class':'col m-2',"id":"Dnm" ,"hidden":True }))
    Pname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',"id":"Pnames",'placeholder':"Enter name","hidden":True }))
    file_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter file name" }))
    file = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))