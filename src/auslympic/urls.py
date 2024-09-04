from django.urls import path
from .views import Home, SportView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('<int:pk>/', SportView.as_view(), name='sport')
]
