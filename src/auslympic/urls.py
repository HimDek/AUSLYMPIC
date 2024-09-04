from django.urls import path
from .views import Home, SportView, LeaderBoard

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('leaderboards/', LeaderBoard.as_view(), name='leaderboard'),
    path('<int:pk>/', SportView.as_view(), name='sport')
]
