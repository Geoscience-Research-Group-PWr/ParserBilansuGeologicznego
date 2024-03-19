from django.shortcuts import render
from django import forms
from django.http import HttpResponse

class DataForm(forms.Form):
    name=forms.CharField(initial="Name")
    date1=forms.DateTimeField()
    date2=forms.DateField()
def add(request):
    if request.method=="post":
        form=DataForm(request.POST)
        mine=form.name.clean()
        print(mine)
        return render(request,"MinesAPP/output.html",{"form":DataForm(),"mine":mine})
    return render(request,"MinesAPP/output.html",{"form":DataForm()})
def index(request):
    return render(request,"MinesAPP/index.html",{"form":DataForm()})
def output(request):
    name='jogn'
    return render(request,"MinesAPP/output.html",{"name":name})