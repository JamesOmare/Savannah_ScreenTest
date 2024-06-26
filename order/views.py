from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse, OpenApiExample
from .models import Order
from loguru import logger
from customer.models import Customer
from .serializers import OrderSerializer
import africastalking


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
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    # def create(self, request):
    #     user = request.user
    #     customer = Customer.objects.filter(email=user.email).first()
        
    #     if not customer:
    #         return Response({'error': 'User Not Found, Invalid Credentials'}, 
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     if not customer.phone_number:
    #         return Response({'error': 'Phone number is required, Please update your phone number to proceed.'}, 
    #                         status=status.HTTP_400_BAD_REQUEST)
        
    #     serializer = OrderSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         # Send the SMS
    #         order = serializer.instance
    #         phone_number = order.owner.phone_number
    #         logger.info(f"Phone number: {phone_number}")
    #         message = f"Hello {order.owner.username}, your order for {order.item} has been placed successfully."

    #         africastalking.initialize(settings.AFRICAS_TALKING_USERNAME, settings.AFRICAS_TALKING_API_KEY)
    #         sms = africastalking.SMS

    #         try:
    #             response = sms.send(
    #                 message,
    #                 [phone_number],
    #                 settings.AFRICAS_TALKING_SENDER_ID
    #             )
    #             logger.info(f"SMS Response: {response}")
    #             sms_status = response['SMSMessageData']['status']
    #         except Exception as e:
    #             sms_response = f"Failed to send SMS: {str(e)}"
    #             return Response({
    #                 'msg': 'Order created Successfully',
    #                 'sms_response': sms_response
    #             }, status=status.HTTP_201_CREATED)
    #         return Response({
    #             'msg': 'Order created Successfully',
    #             'sms_response': f"The sms message has been sent to the user with a status of {sms_status}"
    #         }, status=status.HTTP_201_CREATED)
                
    #     return Response(serializer.errors, 
    #                     status=status.HTTP_400_BAD_REQUEST)
    
        
    def create(self, request):
        user = request.user
        customer = Customer.objects.filter(email=user.email).first()
        
        if not customer:
            return Response({'error': 'User Not Found, Invalid Credentials'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        if not customer.phone_number:
            return Response({'error': 'Phone number is required, Please update your phone number to proceed.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            # Send the SMS
            order = serializer.instance
            phone_number = order.owner.phone_number
            message = f"Hello {order.owner.username}, your order for {order.item} has been placed successfully."

            africastalking.initialize(settings.AFRICAS_TALKING_USERNAME, settings.AFRICAS_TALKING_API_KEY)
            sms = africastalking.SMS

            try:
                response = sms.send(
                    message,
                    [phone_number],
                    settings.AFRICAS_TALKING_SENDER_ID
                )
                sms_status = response['SMSMessageData']['Recipients'][0]['status']
            except Exception as e:
                sms_response = f"Failed to send SMS: {str(e)}"
                return Response({
                    'msg': 'Order created Successfully',
                    'sms_response': sms_response,
                    'africastalking_response': f'{response}',
                }, status=status.HTTP_201_CREATED)
            return Response({
                'msg': 'Order created Successfully',
                'sms_response': f"The sms message has been sent to the user with a status of {sms_status}",
                'africastalking_response': f'{response}',
            }, status=status.HTTP_201_CREATED)
            
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
