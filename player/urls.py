from django.urls import path
from player import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loggedin', views.loggedin),
    path('loggedout', views.loggedout),
    path('player/<int:id>', views.player, name='player-home'),
    path('player/track', views.track, name='track-watch-time'),
    path('player/analysis', views.analysis, name='player-analysis'),
]


