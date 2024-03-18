from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,"MinesAPP/index.html")
def output(request):
    name='jogn'
    return render(request,"MinesAPP/output.html",{"name":name})