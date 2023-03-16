from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:pk>/', views.ViewUser.as_view()),
]
