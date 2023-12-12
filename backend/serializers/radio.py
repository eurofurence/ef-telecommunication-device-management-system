from rest_framework import serializers

from backend.models import RadioDeviceTemplate, RadioDevice, RadioAccessoryTemplate, RadioAccessory


class RadioDeviceTemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RadioDeviceTemplate
        fields = ['id', 'name', 'description', 'owner']


class RadioDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RadioDevice
        fields = ['id', 'template', 'notes', 'serialnumber', 'handed_out', 'created_at', 'updated_at', 'callsign']


class RadioAccessoryTemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RadioAccessoryTemplate
        fields = ['id', 'name', 'description', 'owner', 'allow_quickadd']


class RadioAccessorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RadioAccessory
        fields = ['id', 'template', 'notes', 'serialnumber', 'handed_out', 'created_at', 'updated_at']
