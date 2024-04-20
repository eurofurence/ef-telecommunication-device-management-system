from rest_framework import serializers

from backend.models import PhoneTemplate, Phone
from backend.serializers import ItemOwnerSerializer


class PhoneTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ItemOwnerSerializer.Meta.model.objects.all(), source='owner')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = PhoneTemplate
        fields = ['id', 'name', 'description', 'owner', 'owner_id', 'pretty_name']


class PhoneSerializer(serializers.ModelSerializer):
    template = PhoneTemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PhoneTemplate.objects.all(), source='template')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = Phone
        fields = [
            'id',
            'pretty_name',
            'template',
            'template_id',
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
