from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from backend.models import User
from backend.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['username', 'email', 'ef_reg_id', 'ef_security_collar_id']
