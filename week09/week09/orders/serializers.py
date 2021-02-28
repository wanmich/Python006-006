# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from .models import Orders, Articles, Posts
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view


# class OrdersSerializers(serializers.HyperlinkedModelSerializer):
#     created_by = serializers.ReadOnlyField(source='created_by.username')

#     class Meta:
#         model = Orders
#         fields = ['id', 'order_id', 'remark', 'create_time', 'update_time', 'created_by']


class OrdersSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Orders
        fields = ['id', 'order_id', 'remark', 'create_time', 'update_time', 'created_by']

    @api_view(['GET'])
    def show_data(self, request):
        id = request.GET['id']
        datas = Orders.objects.filter(article_id=id)
        order_data = OrdersSerializer(datas, many=True)
        return Response({'order_data': OrdersSerializer.data})

    @api_view(['POST'])
    def create_data(self, request):
        id = request.GET['id']
        datas = Orders.objects.filter(article_id=id)
        order_data = OrdersSerializer(datas, many=True)
        return Response({'order_data': OrdersSerializer.data})