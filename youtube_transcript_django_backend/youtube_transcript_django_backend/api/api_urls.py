from . api_views import *
from django.urls import path

urlpatterns = [
    #  ***************** API Routes ******************

    #  ***************** "api/" Prefix is already defined in MainApp of Django Project ******************
    path('get-summary', GetYoutubeTranscriptSummary.as_view(), name= GetYoutubeTranscriptSummary.api_name),
]