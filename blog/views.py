from django.shortcuts import render
from .models import *
from django.views.generic import ListView
import requests
import json


def home(request):
    params = {
        'access_token': '6366847119.8b2861e.30e82030fbe64951bb8a13ab13afe6cf'
    }

    response = requests.get('https://api.instagram.com/v1/users/self/media/recent/', params=params)        
    datas = response.json()

    # for item in datas['data'][:6] :

    comments = [{ "commnt" : requests.get('https://api.instagram.com/v1/media/{postid}/comments'.format(postid= item['id']), params=params).json() , "data" : item }  for item in datas['data'][:6]]

    with open('siteinfo.json', 'r') as f:
        siteinfo = json.load(f)
    content = {
            'siteinfo': siteinfo,
            'insta': comments ,
            'events': Events.objects.order_by('date_event').reverse()[0:3],
    }
    return render(request,'index.html', content)
 

class PostLstView(ListView):
    model = Events
    template_name = 'blog/blog-home.html'
    ordering = ['-date_event']
    paginate_by = 5
