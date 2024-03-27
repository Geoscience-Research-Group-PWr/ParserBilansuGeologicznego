from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from Database import Database
import datetime

db=Database()
tasks=[]
class DataForm(forms.Form):
    name=forms.CharField(label="Mine name")
    start=forms.CharField(label="From",initial=str(datetime.date.today().year-10))
    end=forms.CharField(label="To",initial=str(datetime.date.today().year))


def index1(request):
    form = DataForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        name=form.cleaned_data["name"]
        start=form.cleaned_data["start"]
        end=form.cleaned_data["end"]
        tasks.clear()
        tasks.append(db.search(str(name)))
        return HttpResponseRedirect("results")
    else:
        return render(request,"MinesAPP/index1.html",{"form":form})
    return render(request,"MinesAPP/index1.html",{"form":DataForm()})

def results(request):
    data=[]
    sums=[]
    if tasks[0]:
        columns=[]
        headers1=list(tasks[0][0].keys())
        headers1=headers1[1:-1]
        headers2=list(tasks[0][0]["more"].keys())
        columns=headers1+headers2
        data=db.get_data(tasks,headers2)[0]
        sums=[db.get_data(tasks,headers2)[1],db.get_data(tasks,headers2)[2],db.get_data(tasks,headers2)[3]]
    else:
        columns=[]
        data=[[' ']]
        sums=[]
    return render(request,"MinesAPP/results.html",{"items":tasks,"columns":columns,"data":data,"suma":sums,"name":data[0][0]})