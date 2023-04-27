from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('signin/', views.UserSignInView.as_view(), name='signin'),
    path('images/', views.ImageView.as_view(), name='images'),
    path('history/', views.HistoryView.as_view(), name='history'),
]