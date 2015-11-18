import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from survey.views import IndexView, SurveyDetail, ConfirmView, SurveyCompleted

class PostUrlsTestCase(TestCase):
    def setUp(self):
        pass

    def test_x(self):
        self.assertEqual(True, True)
