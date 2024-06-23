# from django.shortcuts import render

# # Create your views here.
# from rest_framework import viewsets
# from drf_spectacular.utils import extend_schema, extend_schema_view
# from .models import Order
# from .serializers import OrderSerializer


# @extend_schema_view(
#     list=extend_schema(description='List all orders'),
#     retrieve=extend_schema(description='Retrieve an order'),
#     create=extend_schema(description='Create an order'),
#     update=extend_schema(description='Update an order'),
#     partial_update=extend_schema(description='Partially update an order'),
#     destroy=extend_schema(description='Delete an order'),
# )

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import viewsets
# from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
# from .models import Order
# from .serializers import OrderSerializer


# @extend_schema_view(
#     list=extend_schema(
#         description='List all orders',
#         responses={200: OpenApiResponse(OrderSerializer(many=True), description="A list of orders")},
#         examples=[
#             {
#                 'orders': [
#                     {
#                         'id': 1,
#                         'item': 'Example Item',
#                         'amount': '100.00',
#                         'description': 'Example description',
#                         'owner': 1,
#                         'created_at': '2024-06-23T12:00:00Z',
#                         'updated_at': '2024-06-23T12:00:00Z'
#                     }
#                 ]
#             }
#         ]
#     ),
#     retrieve=extend_schema(
#         description='Retrieve an order',
#         parameters=[OpenApiParameter(name='pk', description='Order ID', required=True, type=int)],
#         responses={200: OpenApiResponse(OrderSerializer, description="An order instance")},
#         examples=[
#             {
#                 'id': 1,
#                 'item': 'Example Item',
#                 'amount': '100.00',
#                 'description': 'Example description',
#                 'owner': 1,
#                 'created_at': '2024-06-23T12:00:00Z',
#                 'updated_at': '2024-06-23T12:00:00Z'
#             }
#         ]
#     ),
#     create=extend_schema(
#         description='Create an order',
#         request=OrderSerializer,
#         responses={201: OpenApiResponse({'msg': 'Order created Successfully'}, description="Order creation confirmation")},
#         examples=[
#             {
#                 'item': 'New Item',
#                 'amount': '150.00',
#                 'description': 'New description',
#                 'owner': 1
#             }
#         ]
#     ),
#     update=extend_schema(
#         description='Update an order',
#         request=OrderSerializer,
#         parameters=[OpenApiParameter(name='pk', description='Order ID', required=True, type=int)],
#         responses={200: OpenApiResponse({'msg': 'Order Updated Successfully'}, description="Order update confirmation")},
#         examples=[
#             {
#                 'item': 'Updated Item',
#                 'amount': '200.00',
#                 'description': 'Updated description',
#                 'owner': 1
#             }
#         ]
#     ),
#     partial_update=extend_schema(
#         description='Partially update an order',
#         request=OrderSerializer,
#         parameters=[OpenApiParameter(name='pk', description='Order ID', required=True, type=int)],
#         responses={200: OpenApiResponse({'msg': 'Order Partially Updated Successfully'}, description="Partial order update confirmation")},
#         examples=[
#             {
#                 'item': 'Partially Updated Item',
#                 'description': 'Partially updated description'
#             }
#         ]
#     ),
#     destroy=extend_schema(
#         description='Delete an order',
#         parameters=[OpenApiParameter(name='pk', description='Order ID', required=True, type=int)],
#         responses={200: OpenApiResponse({'msg': 'Order deleted'}, description="Order deletion confirmation")}
#     )
# )
# class OrderViewset(viewsets.ViewSet):
    # def list(self, request):
    #     orders = Order.objects.all()
    #     serializer = OrderSerializer(orders, many=True)
    #     return Response(serializer.data)
    
    # def retrieve(self, request, pk=None):
    #     id = pk
    #     if id is not None:
    #         order = Order.objects.get(id=id)
    #         serializer = OrderSerializer(order)
    #         return Response(serializer.data)
    
    # def create(self, request):
    #     serializer = OrderSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'msg': 'Order created Successfully'}, 
    #                         status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, 
    #                         status=status.HTTP_400_BAD_REQUEST)
    
    
    # def update(self, request, pk):
    #     id = pk
    #     order = Order.objects.get(id=id)
    #     serializer = OrderSerializer(order, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'msg': 'Order Updated Successfully'})
    #     return Response(serializer.errors, 
    #                         status=status.HTTP_400_BAD_REQUEST)
    
    
    # def partial_update(self, request, pk):
    #     id = pk
    #     order = Order.objects.get(id=id)
    #     serializer = OrderSerializer(order, data=request.data,
    #                                    partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'msg': 'Order Partially Updated Successfully'})
    #     return Response(serializer.errors, 
    #                         status=status.HTTP_400_BAD_REQUEST)
    
    
    # def destroy(self, request, pk):
    #     id = pk
    #     order = Order.objects.get(id=id)
    #     order.delete()
    #     return Response({'msg': 'Order deleted'})
    
# views.py
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, OpenApiExample
from .models import Order
from .serializers import OrderSerializer

@extend_schema_view(
    list=extend_schema(
        description='List all orders',
        responses={200: OpenApiResponse(OrderSerializer(many=True), description="A list of orders")},
        examples=[
            OpenApiExample(
                'Example List',
                value={
                    'orders': [
                        {
                            'id': 1,
                            'item': 'Example Item',
                            'amount': '100.00',
                            'description': 'Example description',
                            'owner': 1,
                            'created_at': '2024-06-23T12:00:00Z',
                            'updated_at': '2024-06-23T12:00:00Z'
                        }
                    ]
                }
            )
        ]
    ),
    retrieve=extend_schema(
        description='Retrieve an order',
        responses={200: OpenApiResponse(OrderSerializer, description="An order instance")},
        examples=[
            OpenApiExample(
                'Example Retrieve',
                value={
                    'id': 1,
                    'item': 'Example Item',
                    'amount': '100.00',
                    'description': 'Example description',
                    'owner': 1,
                    'created_at': '2024-06-23T12:00:00Z',
                    'updated_at': '2024-06-23T12:00:00Z'
                }
            )
        ]
    ),
    create=extend_schema(
        description='Create an order',
        request=OrderSerializer,
        responses={201: OpenApiResponse({'msg': 'Order created Successfully'}, description="Order creation confirmation")},
        examples=[
            OpenApiExample(
                'Example Create',
                value={
                    'item': 'New Item',
                    'amount': '150.00',
                    'description': 'New description',
                    'owner': 1
                }
            )
        ]
    ),
    update=extend_schema(
        description='Update an order',
        request=OrderSerializer,
        responses={200: OpenApiResponse({'msg': 'Order Updated Successfully'}, description="Order update confirmation")},
        examples=[
            OpenApiExample(
                'Example Update',
                value={
                    'item': 'Updated Item',
                    'amount': '200.00',
                    'description': 'Updated description',
                    'owner': 1
                }
            )
        ]
    ),
    partial_update=extend_schema(
        description='Partially update an order',
        request=OrderSerializer,
        responses={200: OpenApiResponse({'msg': 'Order Partially Updated Successfully'}, description="Partial order update confirmation")},
        examples=[
            OpenApiExample(
                'Example Partial Update',
                value={
                    'item': 'Partially Updated Item',
                    'description': 'Partially updated description'
                }
            )
        ]
    ),
    destroy=extend_schema(
        description='Delete an order',
        responses={200: OpenApiResponse({'msg': 'Order deleted'}, description="Order deletion confirmation")}
    )
)
class OrderViewset(viewsets.ViewSet):

    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Order created Successfully'}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Order Updated Successfully'})
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Order Partially Updated Successfully'})
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({'msg': 'Order deleted'})
