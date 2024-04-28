from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import Order
from backend.serializers.order import OrderSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that allow Orders to be viewed or edited.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'user__username',
        'user__ef_reg_id',
        'user__ef_security_collar_id',
        'title',
    ]

    @action(detail=False, methods=['get'], url_path="user/(?P<userid>\\d+)")
    def get_user_orders(self, request, userid):
        """
        Returns all orders for the given user ID.

        :param request:
        :param userid:
        :return:
        """
        orders = Order.objects.filter(user__id=userid)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
