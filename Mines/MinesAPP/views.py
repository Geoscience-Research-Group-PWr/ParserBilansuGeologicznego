from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from Database import Database

db=Database()
tasks=[]
class DataForm(forms.Form):
    name=forms.CharField(initial="Name")


def index1(request):
    form = DataForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        name=form.cleaned_data["name"]
        tasks.clear()
        tasks.append(db.search(str(name)))
    else:
        return render(request,"MinesAPP/index1.html",{"form":form})
    return render(request,"MinesAPP/index1.html",{"form":DataForm()})

def results(request):
    return render(request,"MinesAPP/results.html",{"items":tasks})
