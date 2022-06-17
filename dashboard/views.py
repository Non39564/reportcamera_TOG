from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from dashboard.models import DataCamera
from django.db import connections
from datetime import date
import base64, io, os
from PIL import Image, ImageFile
from django.conf import settings

ImageFile.LOAD_TRUNCATED_IMAGES = True
def binaeytopic():
    image = []
    pi = DataCamera.objects.raw('SELECT id,image FROM dashboard_datacamera ORDER BY id DESC LIMIT 0, 3')
    for p in pi:
        image.append(p.image)

    # Decode the string
    binary_data = base64.b64decode(image[0])
    binary_data1 = base64.b64decode(image[1])
    binary_data2 = base64.b64decode(image[2])
    # Convert the bytes into a PIL image
    image = Image.open(io.BytesIO(binary_data))
    image1 = Image.open(io.BytesIO(binary_data1))
    image2 = Image.open(io.BytesIO(binary_data2))

    # Save the image
    image.save('dashboard/static/dashboard/img/1.jpg')
    image1.save("dashboard/static/dashboard/img/2.jpg")
    image2.save("dashboard/static/dashboard/img/3.jpg")
    return "Load picture success!!"

def home(request):
    obj = DataCamera.objects.get(max(id))
    image_data = base64.b64encode(obj.image).decode()

    data = {
        'imgs' : image_data
    }
    return render(request, 'dashboard.html', data)

# Create your views here.
def Dashboard(request):
    a = binaeytopic()
    print(a)
    context={}
    data = []
    today = date.today()
    now = today.strftime("%Y-%m-%d")
    dt = DataCamera.objects.raw('SELECT * from dashboard_DataCamera where date = %s ORDER BY time_in desc',[now])
    for d in dt:
        data.append(d)
        
    su = DataCamera.objects.raw('SELECT id, date, count(name) ss from dashboard_DataCamera group by date order by date')
    datasum =[]
    for s in su:
        datasum.append(s)
    
    context['data'] = data
    context['datasum'] = datasum
    return render(request, 'dashboard.html',context)

def Chart(request):
    context ={}
    su = DataCamera.objects.raw('''
                        SELECT
                        id, date,  
                        SUM(CASE WHEN (name='Non') THEN stack ELSE 0 END) AS Non,
                        SUM(CASE WHEN (name='Tor') THEN stack ELSE 0 END) AS Tor,
                        SUM(CASE WHEN (name='GG') THEN stack ELSE 0 END) AS GG,
                        SUM(CASE WHEN (name='non') THEN stack ELSE 0 END) AS non
                        FROM 
                        dashboard_datacamera
                        GROUP BY 
                        date''')
    name = DataCamera.objects.raw('SELECT id, name from dashboard_DataCamera group by name order by name')
    pie = DataCamera.objects.raw('SELECT id, name,count(name) c from dashboard_DataCamera group by name')

    databar =[]
    namel = []
    datapie = []

    for s in su:
        databar.append(s)
    for n in name:
        namel.append(n)
    for p in pie:
        datapie.append(p)

    context['databar'] = databar
    context['name'] = name
    context['datapie'] = datapie
    print(databar)

    return render(request, 'chart.html', context)

def Table(request):
    context={}
    data = []
    dt = DataCamera.objects.raw('SELECT * from dashboard_DataCamera ORDER BY date desc')
    for d in dt:
        data.append(d)
    context['data'] = data
    return render(request, 'table.html',context)

def Edit(request):
    context ={}
    if request.POST:
        ids = request.POST.get('id')
        name = request.POST.get('name')
        edit = DataCamera.objects.raw(
                    'SELECT * from dashboard_DataCamera WHERE id = %s and name = %s', [ids,name])
        for e in edit:
            context['id'] = e.id
            context['Company'] = e.Company
            context['name'] = e.name
            context['time_in'] = e.time_in
            context['date'] = e.date
            context['time_out'] = e.time_out
        
        return render(request, 'edit.html', context)
    return redirect('Dashboard')

def saveEdit(request):
    if request.POST:
        ids = request.POST.get('id')
        name = request.POST.get('name')
        Company = request.POST.get('Company')
        date = request.POST.get('date')
        time_in = request.POST.get('time_in')
        time_out = request.POST.get('time_out')
        cursor = connections['default'].cursor()
        cursor.execute("UPDATE dashboard_DataCamera SET Company = %s , name = %s , date = %s ,time_in = %s,time_out = %s WHERE id = %s", [
                           Company,name,date,time_in,time_out, ids])
        return redirect('Dashboard')

def delete(request):
    if request.POST:
        name = request.POST.get('name')        
        ids = request.POST.get('id')       
        cursor = connections['default'].cursor()
        cursor.execute("DELETE from dashboard_DataCamera WHERE id = %s and name = %s", [
                           ids, name])
        return redirect('Dashboard')
    
def Unknown(request):
    context={}
    data = []
    image = []
    imageshow = []
    dt = DataCamera.objects.raw('''SELECT id, Company, name, date, time_in, time_out, image FROM dashboard_datacamera 
                                WHERE name = 'unknown' ORDER by date, time_in DESC''')
    imgdata = []
    for d in dt:
        binary_data = base64.b64decode(d.image)
        image = Image.open(io.BytesIO(binary_data))
        ids = d.id
        image.save(f'dashboard/static/dashboard/img/unknown/{ids}.jpg')
        imgdata.append(d)

    images = os.listdir('dashboard/static/dashboard/img/unknown/')
    context['images'] = images
    context['data'] = data
    context['imgdata'] = imgdata
    return render(request, 'unknown.html',context)

# def Unknown(request):
#     context={}
#     data = []
#     image = []
#     imageshow = []
#     dt = DataCamera.objects.raw('''SELECT id, Company, name, date, time_in, time_out, image FROM dashboard_datacamera 
#                                 WHERE name = 'unknown' ORDER by date, time_in DESC LIMIT 0, 1; ''')
#     imgdata = []
#     for d in dt:
#         binary_data = base64.b64decode(d.image)
#         image = Image.open(io.BytesIO(binary_data))
#         ids = d.id
#         image.save(f'dashboard/static/dashboard/img/unknown/{ids}.jpg')
#         imgdata.append(d)




#     context['data'] = data
#     context['imgdata'] = imgdata
#     return render(request, 'unknown.html',context)

def Statistics(request):
    context={}
    data = []
    dt = DataCamera.objects.raw('SELECT id, name, COUNT(name) as value FROM dashboard_datacamera GROUP By name ORDER BY value DESC')
    for d in dt:
        data.append(d)
    context['data'] = data
    return render(request, 'statistics.html',context)

def gallery_view(request):
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + "./static/dashboard/img/unknown/")
    context = {"images": img_list}
    return render (request, 'unknown.html', context)