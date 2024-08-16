from django.shortcuts import render, redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
import time
import datetime
from django.utils import timezone
import pytz

from django.db.models import Avg, IntegerField, Count, Sum
from django.db.models.functions import Cast

import pandas as pd

global session_start
global session_end

def home(request):
    return render(request, 'home.html')

@login_required
def player(request, id):
    # email = 'abc@gmail.com'
    # email = request.user.email
    return render(request, 'player.html', {'video': Video.objects.filter(id=id).first(), 'videos':Video.objects.all()} )

def loggedin(request):
    session_start=datetime.datetime.now() #time.time()
    # request.session['session_start'] = session_start
    print(session_start)
    
    response = redirect('/player/1')
    response.set_cookie('session_start', session_start)
    response.set_cookie('user_id', request.user.id)
    return response

def loggedout(request):
    session_end=datetime.datetime.now()
    past = request.COOKIES.get('session_start')
    user = request.COOKIES.get('user_id')
    session_start = datetime.datetime.strptime(past, "%Y-%m-%d %H:%M:%S.%f")
    diff = session_end - session_start
    seconds_in_day = 24 * 60 * 60
    session_length = diff.days * seconds_in_day + diff.seconds

    # Calculate the duration of videos watched during the session
    user_events = UserEvent.objects.filter(user=user,created_at__gt=timezone.make_aware(session_start,timezone.get_default_timezone()) )
    print(UserEvent.objects.all().order_by('-id').values())
    print('hiiiii')
    print(session_end)
    print(user_events)
    total_duration = user_events.aggregate(total_duration=Sum('duration'))['total_duration']

    tf_reg_serializer = UserSessionSerializer(data={'user':user, 'session':session_length, 'duration':total_duration})
    if tf_reg_serializer.is_valid():
        print('valid!!')
        tf_reg_serializer.save()

    # Log the session data
    print(f'Session for user {request.user.id} lasted {session_length} seconds and had a total video watch time of {total_duration} seconds.')
    return redirect('home')

@api_view(['GET','POST'])
# @parser_classes([JSONParser])
def track(request):
    if request.method == "POST":
        data = request.data
        video = int(data["video_id"])
        duration = int(data["duration"])
        ended = data["ended"]
        runtime = int(data["runtime"])
        playedFor = int(data["playedFor"])
        user = request.user.id
        
        print('here')
        
        if ended==True and duration>0.75*runtime:
            video = Video.objects.filter(id=video).first()
            video.watches += 1
            print(video.title)
            video.save()
        else:
            tf_reg_serializer = UserEventSerializer(data={'user':user, 'video':video, 'duration':playedFor})
            if tf_reg_serializer.is_valid():
                print('valid!!')
                tf_reg_serializer.save()

        return HttpResponse("Event tracked successfully.")


def analysis(request):
    avg_duration_video_watched_per_user = (UserEvent.objects
        .values('user')
        # .values('video')
        .annotate(avg_duration=Sum('duration'))
        .order_by()
    )

    data = UserEvent.objects.all().values()
    df = pd.DataFrame(data)

    grouped = df.groupby(['video', 'user']).sum()
    result = grouped.reset_index().groupby('video')['duration'].mean()

    # Most watched video
    data2 = Video.objects.all().order_by('-watches').values()

    # average user session vs duration of videos watched during that session etc.
    data = UserSession.objects.all().values()
    print(data)
    df = pd.DataFrame(data)
    grouped = df.groupby(['user'])['session','duration'].mean()
    result2 = grouped.reset_index()
    print('session: \n', result2)

    mydict = {
        "df": pd.DataFrame(result).reset_index().to_html(),
        "df2": pd.DataFrame(data2).to_html,
        "df3": pd.DataFrame(result2).reset_index().to_html(),
    }

    print(avg_duration_video_watched_per_user)
    print(grouped)
    print(result)
    return render(request, 'analysis.html', mydict)
