# project_register/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from .views import update_status


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='authenticate/login.html'), name='login'),
    path('register/', views.register_user, name='register'),
    path('home/', views.home, name='home'),
    path('', views.welcome, name='welcome'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('professor/', views.professor_page, name='professor_page'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('search_student/', views.search_student, name='search_student'),
    path('delete_pdf/<int:pdf_id>/', views.delete_pdf, name='delete_pdf'),
    path('search/', views.search_by_sujet, name='search_by_sujet'),
    path('update_status/<int:pdf_id>/', update_status, name='update_status'),
    path('student/', views.student, name='student'),


    



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

