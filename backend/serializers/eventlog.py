from rest_framework import serializers

from backend.models import EventLogEntry
from backend.serializers import UserSerializer


class EventLogEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EventLogEntry
        fields = [
            'id',
            'action',
            'user',
            'timestamp',
            'data'
        ]
