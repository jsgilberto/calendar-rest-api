from rest_framework import serializers
from .models import Calendar, Event
from django.http import Http404


class CalendarSerializer(serializers.ModelSerializer):

    owner = serializers.SerializerMethodField('get_owner')

    class Meta:
        model = Calendar
        fields = ['id', 'title', 'description', 'timezone', 'owner',
            'created_at', 'updated_at']


    def get_owner(self, obj):
        return obj.user.username
    

    def create(self, validated_data):
        validated_data.update({"user": self.context['request'].user})
        calendar = Calendar(**validated_data)
        calendar.save()
        return calendar



class EventSerializer(serializers.ModelSerializer):

    calendar = serializers.SerializerMethodField('get_calendar')

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'status', 'start', 'end',
            'calendar']
    

    def get_calendar(self, obj):
        return obj.calendar.id


    def create(self, validated_data):
        calendar_id = self.context.get("view").kwargs.get("calendar_id", None)

        # search for the calendar first
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Event.DoesNotExist:
            raise Http404("No Event matches the id.")
        
        validated_data.update({"calendar": calendar})
        event = Event(**validated_data)
        event.save()

        return event 