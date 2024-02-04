from rest_framework import serializers

from backend.models import CallboxTemplate, Callbox
from backend.serializers import ItemOwnerSerializer


class CallboxTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = CallboxTemplate
        fields = ['id', 'name', 'description', 'owner']


class CallboxSerializer(serializers.ModelSerializer):
    template = CallboxTemplateSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = Callbox
        fields = [
            'id',
            'pretty_name',
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
            'location',
            'has_camera',
            'camera_ip_address',
            'camera_mac_address'
        ]
