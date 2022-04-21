from django.urls import path
from . import views

app_name = 'studies'
urlpatterns = [
    path('studies/', views.index, name='studies')
]