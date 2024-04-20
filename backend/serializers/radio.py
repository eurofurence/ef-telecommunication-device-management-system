from rest_framework import serializers

from backend.models import RadioDeviceTemplate, RadioDevice, RadioAccessoryTemplate, RadioAccessory, Pager, RadioCoding, \
    PagerTemplate
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
    owner = ItemOwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ItemOwnerSerializer.Meta.model.objects.all(), source='owner')
    coding = RadioCodingSerializerReduced(read_only=True)
    coding_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=RadioCoding.objects.all(), source='coding')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioDeviceTemplate
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'owner_id',
            'coding',
            'coding_id',
            'pretty_name'
        ]


class RadioDeviceSerializer(serializers.ModelSerializer):
    template = RadioDeviceTemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=RadioDeviceTemplate.objects.all(), source='template')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioDevice
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
            'callsign',
        ]


class RadioAccessoryTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioAccessoryTemplate
        fields = ['id', 'name', 'description', 'owner', 'allow_quickadd', 'pretty_name']


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
    template_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=RadioAccessoryTemplate.objects.all(), source='template')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioAccessory
        fields = [
            'id',
            'pretty_name',
            'template',
            'template_id',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at'
        ]


class PagerTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = PagerTemplate
        fields = ['id', 'name', 'description', 'owner', 'pretty_name']


class PagerSerializer(serializers.ModelSerializer):
    template = PagerTemplateSerializer()
    template_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PagerTemplate.objects.all(), source='template')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = Pager
        fields = [
            'id',
            'pretty_name',
            'template',
            'template_id',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at'
        ]
