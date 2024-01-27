from rest_framework import serializers

from backend.models import User, ItemOwner


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'ef_reg_id', 'ef_security_collar_id', 'last_seen']


class ItemOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOwner
        fields = ['id', 'name', 'shortname']
