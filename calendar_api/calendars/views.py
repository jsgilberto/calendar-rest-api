from rest_framework import authentication, permissions, viewsets
from .models import Calendar, Event
from .serializers import CalendarSerializer, EventSerializer


class DefaultsMixin(object):
    """ Default settings for view authentication, permissions,
    filtering and pagination. """

    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 20
    paginate_by_param = 'pagination_size'
    max_paginate_by = 100


class CalendarViewSet(DefaultsMixin,
                    viewsets.ModelViewSet):
    """ API endpoint for listing and creating calendars. """

    # queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        This view should return a list of all the calendars
        for the currently authenticated user.
        """
        user = self.request.user
        return Calendar.objects.filter(user=user).order_by("updated_at")


class EventViewSet(DefaultsMixin,
                viewsets.ModelViewSet):
    """ API endpoints for listing and creating calendars. """
    serializer_class = EventSerializer
    lookup_field = 'id'


    def get_queryset(self):
        # make sure calendar is owned by user
        user = self.request.user
        calendar = Calendar.objects.get(id=self.kwargs["calendar_id"], user=user)
        return Event.objects.filter(calendar=calendar).order_by("start")