from rest_framework import serializers

from backend.models import PhoneTemplate, Phone
from backend.serializers import ItemOwnerSerializer


class PhoneTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = PhoneTemplate
        fields = ['id', 'name', 'description', 'owner']


class PhoneSerializer(serializers.ModelSerializer):
    template = PhoneTemplateSerializer()

    class Meta:
        model = Phone
        fields = [
            'id',
            'template',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at',
            'extension',
            'network',
            'dhcp',
            'ip_address',
            'mac_address',
            'location'
        ]