from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from .Serializers import UserSerializers
from .Serializers import ChangePasswordSerializer
from .Serializers import LoginSerializer
from .Serializers import AddProductSerializers
from .models import User
from .models import Image
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product,OrderPurchased
from .Serializers import ProductSerializer
from .Serializers import OrderPurchasedSerializer
from .Serializers import ImageSerializer
from DjangoWebsite.settings import create_access_token
# from rest_framework.parsers import MultiPartParser, FormParser

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializers = UserSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    


# @api_view(['POST'])
# def LoginLog(request):
#     serializer = LoginSerializer(data=request.data)
    
#     if serializer.is_valid():
#         user_data = serializer.save()  # Save will trigger the creation of the log entry
        
#         return Response({
#             "UserId": user_data['UserId'],
#             "LogId": user_data['LogId'],
#             "Action": user_data['Action'],
#             "Timestamp": user_data['Timestamp'],
#             "RefreshToken": user_data['RefreshToken'],
#             "AccessToken": user_data['AccessToken'],
#         }, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def LoginLog(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user_data = serializer.save()  # Save will trigger the creation of the log entry
        
        return Response({
            "UserId": user_data['UserId'],
            "LogId": user_data['LogId'],
            "Action": user_data['Action'],
            "Timestamp": user_data['Timestamp'],
            "RefreshToken": user_data['RefreshToken'],
            "AccessToken": user_data['AccessToken'],
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    if request.method == 'POST':
        serializers = AddProductSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Retrieve a product by its ID
@permission_classes([IsAuthenticated])
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

@permission_classes([IsAuthenticated])
class AllProductDetailsView(generics.ListAPIView):
    queryset = Product.objects.all()



    serializer_class = ProductSerializer
# Update a product by its ID
class UpdateProductView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# class DeleteProductView(generics.DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# Delete a product by its ID
@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class AddOrderPurchased(generics.CreateAPIView):
    queryset = OrderPurchased.objects.all()
    serializer_class = OrderPurchasedSerializer

class RetrieveAllOrderPurchased(generics.ListAPIView):
    queryset = OrderPurchased.objects.all()
    serializer_class = OrderPurchasedSerializer

@api_view(['DELETE'])
def delete_orderPurchased(request, pk):
    try:
        orderPurchased = OrderPurchased.objects.get(pk=pk)
    except OrderPurchased.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    orderPurchased.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class ImageListCreate(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageRetrieve(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageUpdate(generics.UpdateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageDestroy(generics.RetrieveDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

