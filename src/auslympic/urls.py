from django.urls import path
from .views import Home, SportView, LeaderBoard, NoticeView, MerchView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('leaderboard/', LeaderBoard.as_view(), name='leaderboard'),
    path('notices/', NoticeView.as_view(), name='notices'),
    path('merch/', MerchView.as_view(), name='merch'),
    path('<int:pk>/', SportView.as_view(), name='sport')
]
