from django.urls import path
from .views import Home, SportView, LeaderBoard, NoticeView, MerchandiseView, TeamsView, Winners, Rules, DumpedData

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('leaderboard/', LeaderBoard.as_view(), name='leaderboard'),
    path('notices/', NoticeView.as_view(), name='notices'),
    path('merchandise/', MerchandiseView.as_view(), name='merchandise'),
    path('teams/', TeamsView.as_view(), name='teams'),
    path('winners/', Winners.as_view(), name='winners'),
    path('rules/', Rules.as_view(), name='rules'),
    path('data/', DumpedData.as_view(), name='data'),
    path('<int:pk>/', SportView.as_view(), name='sport')
]
