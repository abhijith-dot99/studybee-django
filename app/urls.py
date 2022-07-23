from django.urls import path
from . import views

urlpatterns  = [
    path('login/',views.loginpage,name="login"),
    path('',views.home,name ='home'),
    path('room/<str:pk>/', views.room,name = 'room'),
    path('createroom/',views.createroom,name = 'createroom'),
    path('updateroom/<str:pk>/',views.updateroom,name = 'updateroom'),
    path('deleteroom/<str:pk>/',views.deleteroom,name= 'deleteroom')
    ]
 