from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import AdminPasswordResetForm

app_name = 'backoffice'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # URLs de recuperación de contraseña
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='backoffice/password_reset.html',
             form_class=AdminPasswordResetForm,
             email_template_name='backoffice/password_reset_email.html',
             subject_template_name='backoffice/password_reset_subject.txt',
             success_url='/admin/password-reset/done/'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='backoffice/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='backoffice/password_reset_confirm.html',
             success_url='/admin/reset/done/'
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='backoffice/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]