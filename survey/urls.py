from django.conf.urls import patterns, url

from .views import IndexView
from .views import SurveyDetail
from .views import ConfirmView
from .views import SurveyCompleted

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='survey-list'),
    url(
        r'^survey/(?P<id>\d+)/$',
        SurveyDetail.as_view(),
        name='survey-detail'
    ),
    url(
        r'^survey/(?P<id>\d+)/completed/$',
        SurveyCompleted.as_view(),
        name='survey-completed'
    ),
    url(
        r'^survey/(?P<id>\d+)-(?P<step>\d+)/$',
        SurveyDetail.as_view(),
        name='survey-detail-step'
    ),
    url(
        r'^confirm/(?P<uuid>\w+)/$',
        ConfirmView.as_view(),
        name='survey-confirmation'
    ),
)
