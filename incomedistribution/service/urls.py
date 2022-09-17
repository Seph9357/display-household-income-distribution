from django.conf.urls import url

from . import views

urlpatterns = [


    url(r'service/fieldvaluedisplay/?$', views.DisplaySa4StateinfoView.as_view()),
    url(r'service/statelistdisplay/?$', views.DisplayStateListView.as_view()),
    url(r'service/householdcompositionlistdisplay/?$', views.DisplayHouseholdCompositionListView.as_view()),
    url(r'service/weeklyhouseholdincomelistdisplay/?$', views.WeeklyHouseholdIncomeListView.as_view()),
    url(r'service/filterview/?$', views.FilterView.as_view()),
    url(r'service/sa4listdisplay/?$', views.DisplaySA4ListView.as_view()),
    url(r'service/a4statecomparedisplay/?$', views.Sa4StateCompareView.as_view()),

]