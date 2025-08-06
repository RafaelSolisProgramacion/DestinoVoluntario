from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('registrar/voluntario/', views.registrar_voluntario, name='registrar_voluntario'),
    path('registrar/organizacion/', views.registrar_organizacion, name='registrar_organizacion'),
]