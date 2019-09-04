from datetime import datetime, timedelta

import requests_cache
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.modules.analytics.constants import NUMBER_OF_DAYS_FOR_ACTIVE_STATUS
from nomad.settings import TIME_ZONE_SUBCLASS

time_difference = timedelta(days=1)
requests_cache.install_cache(expire_after=time_difference)


@api_view(['GET'])
def user_analytics(request):
    """
    Returns number of users
    :param request:
    :return: 200 successful
    """
    number_of_users = User.objects.count()
    number_of_verified_users = User.objects.filter(profile__is_verified=True).count()
    end_date = datetime.now(tz=TIME_ZONE_SUBCLASS)
    start_date = end_date - timedelta(days=NUMBER_OF_DAYS_FOR_ACTIVE_STATUS)
    number_of_active_users = User.objects.filter(profile__last_active__range=[start_date, end_date]).count()
    number_of_active_verified_users = User.objects.filter(
        profile__last_active__range=[start_date, end_date], profile__is_verified=True).count()

    res = {
        'total': number_of_users,
        'active': number_of_active_users,
        'verified': number_of_verified_users,
        'active_verified': number_of_active_verified_users
    }
    return Response(res, status=status.HTTP_200_OK)
