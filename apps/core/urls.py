from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('registrar/voluntario/', views.registrar_voluntario, name='registrar_voluntario'),
    path('registrar/organizacion/', views.registrar_organizacion, name='registrar_organizacion'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Página de términos y condiciones
    path('terminos-condiciones/', TemplateView.as_view(template_name='core/terminos_condiciones.html'), name='terminos_condiciones'),

    # Password reset URLs
    path('password_reset/', PasswordResetView.as_view(template_name='core/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
]