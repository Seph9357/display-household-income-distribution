from django.conf.urls import url

from . import views

urlpatterns = [


    url(r'service/fieldvaluedisplay/?$', views.DisplaySa4StateinfoView.as_view()),



]