from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from backend.models import RadioDevice, RadioAccessory, Pager, Phone, Callbox, RadioDeviceTemplate, \
    RadioAccessoryTemplate, PagerTemplate, PhoneTemplate, CallboxTemplate, ItemTemplate, ItemCoordinates, Item
from backend.serializers import ItemOwnerSerializer
from backend.serializers.callbox import CallboxSerializer, CallboxTemplateSerializer
from backend.serializers.phone import PhoneSerializer, PhoneTemplateSerializer
from backend.serializers.radio import RadioDeviceSerializer, RadioAccessorySerializer, PagerSerializer, \
    RadioDeviceTemplateSerializer, RadioAccessoryTemplateSerializer, PagerTemplateSerializer


class ItemTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = ItemTemplate
        fields = ['id', 'name', 'description', 'owner', 'private', 'pretty_name']


class PolymorphicItemTemplateSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        ItemTemplate: ItemTemplateSerializer,
        RadioDeviceTemplate: RadioDeviceTemplateSerializer,
        RadioAccessoryTemplate: RadioAccessoryTemplateSerializer,
        PagerTemplate: PagerTemplateSerializer,
        PhoneTemplate: PhoneTemplateSerializer,
        CallboxTemplate: CallboxTemplateSerializer,
    }


class PolymorphicItemSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        RadioDevice: RadioDeviceSerializer,
        RadioAccessory: RadioAccessorySerializer,
        Pager: PagerSerializer,
        Phone: PhoneSerializer,
        Callbox: CallboxSerializer,
    }


class ItemCoordinatesSerializer(serializers.ModelSerializer):
    item = PolymorphicItemSerializer(read_only=True)

    class Meta:
        model = ItemCoordinates
        fields = ['floor', 'latitude', 'longitude', 'item']


class ItemMetadataSerializer(PolymorphicSerializer):
    class ItemMetadataSerializer(serializers.ModelSerializer):
        pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)
        handed_out = serializers.BooleanField(read_only=True)

        class Meta:
            model = Item
            fields = ['id', 'pretty_name', 'handed_out']

    model_serializer_mapping = {
        RadioDevice: ItemMetadataSerializer,
        RadioAccessory: ItemMetadataSerializer,
        Pager: ItemMetadataSerializer,
        Phone: ItemMetadataSerializer,
        Callbox: ItemMetadataSerializer,
    }
