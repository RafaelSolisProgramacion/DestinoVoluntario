from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('registrar/voluntario/', views.registrar_voluntario, name='registrar_voluntario'),
    path('registrar/organizacion/', views.registrar_organizacion, name='registrar_organizacion'),
    path('dashboard/', views.dashboard, name='dashboard'),
]