from django.urls import path,re_path,include
from django.http import HttpResponseRedirect

from . import views

app_name = 'candela'
urlpatterns = [
    re_path(r'^$', lambda r: HttpResponseRedirect('victims/')),
    path('beacon/', views.receive_beacon, name='receive_beacon'),
    path('victims/', include([
            path('', views.victims_index, name='victims_index'),
            path('list/', views.list_victims, name='list_victims'),
            path('<int:id>/', include([
                    path('', views.victim_details, name='victim_details'),
                    path('sent/', views.list_sent, name='victim_sent'),
                    path('stack/', views.list_stack, name='victim_stack'),
                ])),
        ])),
]
