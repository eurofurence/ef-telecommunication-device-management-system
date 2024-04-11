from rest_framework import serializers
from rest_framework.fields import ListField, IntegerField

from backend.models import ItemBinding, User, Item, ItemTemplate
from backend.serializers import UserSerializer
from backend.serializers.item import PolymorphicItemSerializer
from backend.validators import ObjectWithIdExistsValidator


class ItemBindingSerializer(serializers.ModelSerializer):
    # Read-only
    user = UserSerializer(read_only=True)
    bound_by = UserSerializer(read_only=True)
    item = PolymorphicItemSerializer(read_only=True)

    # Write-only
    user_id = IntegerField(
        min_value=0,
        validators=[ObjectWithIdExistsValidator(User)]
    )
    item_ids = ListField(
        child=IntegerField(min_value=0, validators=[ObjectWithIdExistsValidator(Item)]),
        write_only=True,
        allow_empty=True,
    )
    item_template_ids = ListField(
        child=IntegerField(min_value=0, validators=[ObjectWithIdExistsValidator(ItemTemplate)]),
        write_only=True,
        allow_empty=True
    )

    class Meta:
        model = ItemBinding
        fields = [
            # Read-only
            'id',
            'item',
            'user',
            'bound_at',
            'bound_by',

            # Write-only
            'user_id',
            'item_ids',
            'item_template_ids',
        ]
