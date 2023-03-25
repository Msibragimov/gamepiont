from django.urls import path
from .views import *



urlpatterns = [
    path('', homepage, name='homepage'),
    path('register', register, name='register'),
    path('login', login_request, name='login'),
    path('logout', log_user_out, name='logout'),
    path('activate/<int:uid>/<str:token>', activate_user, name='activate'),
]