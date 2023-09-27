from rest_framework import serializers

from backend.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'ef_reg_id', 'ef_security_collar_id', 'last_seen']
