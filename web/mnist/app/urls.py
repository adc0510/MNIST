from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'home'),
    path('test',views.MNIST, name = 'test'),
    path('test/save_drawing/', views.save_drawing, name='save_drawing'),
    path('test2', views.test2, name = 'test2'),
]