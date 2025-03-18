from django.urls import path
from userapp import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('center/', views.CenterView.as_view(), name='center'),
]
