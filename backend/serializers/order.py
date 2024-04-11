from rest_framework import serializers

from backend.models import Order
from backend.serializers import UserSerializer
from backend.serializers.item import PolymorphicItemSerializer, PolymorphicItemTemplateSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    item = PolymorphicItemSerializer(read_only=True)
    item_template = PolymorphicItemTemplateSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'title',
            'item',
            'item_template',
        ]
