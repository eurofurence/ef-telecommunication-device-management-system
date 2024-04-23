from rest_framework import serializers

from backend.models import Order
from backend.serializers import UserSerializer
from backend.serializers.item import PolymorphicItemSerializer, PolymorphicItemTemplateSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserSerializer.Meta.model.objects.all(), source='user')
    item = PolymorphicItemSerializer(read_only=True)
    # TODO: Implement write support for item
    item_template = PolymorphicItemTemplateSerializer(read_only=True)
    # TODO: Implement write support for item_template

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_id',
            'type',
            'title',
            'item',
            'item_template',
        ]
