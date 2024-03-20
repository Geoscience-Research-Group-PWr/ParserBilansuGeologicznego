from django.shortcuts import render
from django import forms
from django.http import HttpResponse

tasks=['x','y','z']
class DataForm(forms.Form):
    name=forms.CharField(initial="Name")
def add(request):
    if request.method=="post":
        form=DataForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            tasks.append("xd")
        return render(request,"MinesAPP/output.html",{"form":DataForm(),"name":"xxx"})
def index(request):
    return render(request,"MinesAPP/index.html",{"form":DataForm()})
def output(request):
    name='jogn'
    return render(request,"MinesAPP/output.html",{"name":name})
def list(request):
    return render(request,"MinesAPP/list.html",{"items":tasks})