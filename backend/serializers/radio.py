from rest_framework import serializers

from backend.models import RadioDeviceTemplate, RadioDevice, RadioAccessoryTemplate, RadioAccessory
from backend.serializers import ItemOwnerSerializer


class RadioDeviceTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = RadioDeviceTemplate
        fields = ['id', 'name', 'description', 'owner']


class RadioDeviceSerializer(serializers.ModelSerializer):
    template = RadioDeviceTemplateSerializer()

    class Meta:
        model = RadioDevice
        fields = [
            'id',
            'template',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at',
            'callsign'
        ]


class RadioAccessoryTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = RadioAccessoryTemplate
        fields = ['id', 'name', 'description', 'owner', 'allow_quickadd']


class RadioAccessorySerializer(serializers.ModelSerializer):
    template = RadioAccessoryTemplateSerializer()

    class Meta:
        model = RadioAccessory
        fields = ['id', 'template', 'notes', 'serialnumber', 'handed_out', 'created_at', 'updated_at']
