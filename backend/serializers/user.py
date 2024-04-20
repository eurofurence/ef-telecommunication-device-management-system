from rest_framework import serializers

from backend.models import User, ItemOwner


class UserSerializer(serializers.ModelSerializer):
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'pretty_name', 'email', 'ef_reg_id', 'ef_security_collar_id', 'last_seen']


class ItemOwnerSerializer(serializers.ModelSerializer):
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = ItemOwner
        fields = ['id', 'name', 'shortname', 'pretty_name']
