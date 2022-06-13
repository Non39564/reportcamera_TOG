from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
def Dashboard(request):
    return render(request, 'dashboard.html')

def Chart(request):
    return render(request, 'chart.html')

def Table(request):
    return render(request, 'table.html')

def Edit(request):
    return render(request, 'edit.html')