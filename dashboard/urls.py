from django.urls import path
from . import views
urlpatterns = [
    path('',views.Dashboard, name="Dashboard"),
    path('Chart',views.Chart, name="Chart"),
    path('Table',views.Table, name="Table"),
    path('Edit',views.Edit, name="Edit"),
    path('saveEdit',views.saveEdit, name="saveEdit"),
    path('delete',views.delete, name="delete"),
]

