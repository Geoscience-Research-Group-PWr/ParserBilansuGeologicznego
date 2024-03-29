from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from Database import Database
import datetime

db=Database()
output=[]


class NameForm(forms.Form):
    name=forms.CharField(label="Mine name :")
    start=forms.CharField(label="From :",initial=str(datetime.date.today().year-14))
    end=forms.CharField(label="To :",initial=str(datetime.date.today().year))


# zrobić year jako wybieralną listę
class TypeForm(forms.Form):
    types=forms.CharField(label="Mineral type")
    start1 = forms.CharField(label="From:", initial=str(datetime.date.today().year - 14))
    end1 = forms.CharField(label="To:", initial=str(datetime.date.today().year))


def menu(request):
    return render(request,"MinesAPP/menu.html")


def name_search(request):
    form = NameForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        name=form.cleaned_data["name"]
        start=form.cleaned_data["start"]
        end=form.cleaned_data["end"]
        output.clear()
        output.append(db.search_by_name(str(name), start, end))
        output.append(name)
        return HttpResponseRedirect("name_search/results")
    else:
        return render(request,"MinesAPP/index1.html",{"form":form})
    return render(request,"MinesAPP/index1.html", {"form":NameForm()})


def type_search(request):
    form = TypeForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        types=form.cleaned_data["types"]
        start1=form.cleaned_data["start1"]
        end1=form.cleaned_data["end1"]
        output.clear()
        output.append(db.search_by_type(str(types), start1, end1))
        output.append(types)
        return HttpResponseRedirect("type_search/results")
    else:
        return render(request,"MinesAPP/type_search.html",{"form":form})
    return render(request,"MinesAPP/type_search.html", {"form":TypeForm()})


def results(request):
    data=[]
    sums=[]
    if not output:
        return render(request, "MinesAPP/error.html")
    if output[0]:
        columns=[]
        headers1=list(output[0][0].keys())
        headers1=headers1[1:-1]
        headers2=list(output[0][0]["More"].keys())
        columns=headers1+headers2
        data=db.get_data(output, headers2)[0]
        sums=[db.get_data(output, headers2)[1], db.get_data(output, headers2)[2], db.get_data(output, headers2)[3]]
        return render(request, "MinesAPP/results.html",
                      {"items": output, "columns": columns, "data": data, "suma": sums, "name": output[1]})
    else:
        columns=[]
        data=[[' ']]
        sums=[]
        return render(request,"MinesAPP/error.html")