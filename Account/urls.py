from django.urls import path
from .views import register_view,register_web_view

urlpatterns = [
    path('register',register_view),
    path('reg',register_web_view),
]