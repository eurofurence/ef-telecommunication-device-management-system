from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from backend.models import ItemBinding, RadioDevice, RadioAccessory, Pager, Phone, Callbox
from backend.serializers import UserSerializer
from backend.serializers.callbox import CallboxSerializer
from backend.serializers.phone import PhoneSerializer
from backend.serializers.radio import PagerSerializer, RadioAccessorySerializer, RadioDeviceSerializer


class PolymorphicItemSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        RadioDevice: RadioDeviceSerializer,
        RadioAccessory: RadioAccessorySerializer,
        Pager: PagerSerializer,
        Phone: PhoneSerializer,
        Callbox: CallboxSerializer,
    }


class ItemBindingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    bound_by = UserSerializer()
    item = PolymorphicItemSerializer()

    class Meta:
        model = ItemBinding
        fields = ['id', 'item', 'user', 'bound_at', 'bound_by']
