from rest_framework import serializers

from backend.models import RadioDeviceTemplate, RadioDevice, RadioAccessoryTemplate, RadioAccessory, Pager, RadioCoding
from backend.serializers import ItemOwnerSerializer


class RadioCodingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioCoding
        fields = ['id', 'name', 'color', 'description']


class RadioCodingSerializerReduced(serializers.ModelSerializer):
    class Meta:
        model = RadioCoding
        fields = ['id', 'name', 'color']


class RadioDeviceTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()
    coding = RadioCodingSerializerReduced()

    class Meta:
        model = RadioDeviceTemplate
        fields = ['id', 'name', 'description', 'owner', 'coding']


class RadioDeviceSerializer(serializers.ModelSerializer):
    template = RadioDeviceTemplateSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioDevice
        fields = [
            'id',
            'pretty_name',
            'template',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at',
            'callsign',
        ]


class RadioAccessoryTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = RadioAccessoryTemplate
        fields = ['id', 'name', 'description', 'owner', 'allow_quickadd']


class RadioAccessoryTemplateQuickAddSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()
    statistics = serializers.SerializerMethodField()
    type = serializers.ReadOnlyField(default='RadioAccessoryTemplate')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioAccessoryTemplate
        fields = ['id', 'type', 'name', 'pretty_name', 'description', 'owner', 'allow_quickadd', 'statistics']

    def get_statistics(self, obj):
        total = RadioAccessory.objects.filter(template_id=obj.id).count()
        handed_out = RadioAccessory.objects.filter(template_id=obj.id, itembinding__isnull=False).count()
        return {
            'total': total,
            'handed_out': handed_out,
            'available': total - handed_out
        }


class RadioAccessorySerializer(serializers.ModelSerializer):
    template = RadioAccessoryTemplateSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioAccessory
        fields = [
            'id',
            'pretty_name',
            'template',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at'
        ]


class PagerTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = RadioAccessoryTemplate
        fields = ['id', 'name', 'description', 'owner']


class PagerSerializer(serializers.ModelSerializer):
    template = PagerTemplateSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = Pager
        fields = [
            'id',
            'pretty_name',
            'template',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at'
        ]
