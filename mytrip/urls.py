from django.conf.urls import url
from django.contrib.auth.views import logout, password_change as pwd_change, password_change_done as pwd_change_done, password_reset as reset, password_reset_done as reset_done, password_reset_confirm as reset_confirm, password_reset_complete as reset_complete
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import weather, starter, getzomato, hotels,flights,location
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'mytrip'


urlpatterns = [
    path('', views.home, name='home'),
    # url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    path('starter/', starter.as_view(), name='starter'),
    path('flights/', flights.as_view(), name='flights'),
    path('hotels/', hotels.as_view(), name='hotels'),
    path('weather/', weather.as_view(), name='weather'),
    path('location/', location.as_view(), name='location'),
    url(r'^getzomato/$', getzomato.as_view(), name='getzomato'),
    url('^password-change/done/$', pwd_change_done, name='password_change_done'),
    url('^password-change/$', pwd_change, {'post_change_redirect': '/password-change/done/'}, name='password_change'),
    url(r'^password-reset/complete/$', reset_complete, name='password_reset_complete'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', reset_confirm,
        {'post_reset_redirect': '/password-reset/complete/'}, name='password_reset_confirm'),
    url(r'^password-reset/done/$', reset_done, name='password_reset_done'),
    url(r'^password-reset/$', reset, {'post_reset_redirect': '/password-reset/done/',
                                      'email_template_name': 'registration/password_reset_email.html'},
        name='password_reset'),
    url(r'^userinterest_json/', views.UserInterestList.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)