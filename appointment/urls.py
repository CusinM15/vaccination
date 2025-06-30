from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('confirm/<str:token>/', views.confirm_email, name='confirm_email'),
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('resend-verification/', login_required(views.resend_verification), name='resend_verification'),
    path('submit-vaccination/', login_required(views.submit_vacation), name='submit_vacation'),
    path('book-appointment/', login_required(views.book_appointment), name='book_appointment'),
]