from django.urls import path
from . import views

urlpatterns = [
    path('about_us/', views.about_us, name='about_us'),
    path('sustainability_pledge/', views.sustainability_pledge, name='sustainability_pledge'),
    path('connect_with_us/', views.connect_with_us, name='connect_with_us'),
]