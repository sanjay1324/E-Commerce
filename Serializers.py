from rest_framework import serializers
from .models import UserLog,User,Product,OrderPurchased,Image
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['Username', 'password', 'EmailId', 'MobileNo', 'Age', 'Gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            Username=validated_data['Username'],
            EmailId=validated_data['EmailId'],
            MobileNo=validated_data['MobileNo'],
            Age=validated_data['Age'],
            Gender=validated_data['Gender'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    user_or_email = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        user_or_email = data['user_or_email']
        try:
            if '@' in user_or_email:
                user = User.objects.get(email=user_or_email)
            else:
                user = User.objects.get(username=user_or_email)
        except User.DoesNotExist:
            raise ValidationError("User with this username or email does not exist.")

        if not user.check_password(data['old_password']):
            raise ValidationError({"old_password": "Old password is incorrect."})

        if data['new_password'] != data['confirm_new_password']:
            raise ValidationError({"confirm_new_password": "New password fields didn't match."})

        data['user'] = user
        return data

# class LoginSerializer(serializers.Serializer):
#     Username = serializers.CharField(required=True)
#     Password = serializers.CharField(required=True)

#     def validate(self, data):
#         username = data.get('Username')
#         password = data.get('Password')

#         # Check if username exists in the database
#         try:
#             user = User.objects.get(Username=username)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User does not exist.")

#         # Check if password matches
#         if not user.check_password(password):
#             raise serializers.ValidationError("Invalid password.")
        
#         return data
    
#     def create(self, validated_data):
#         username = validated_data.get('Username')
#         user = User.objects.get(Username=username)
        
#         # Create log entry
#         user_log = UserLog.objects.create(
#             user=user,
#             Action="Logged In",
#             Timestamp=timezone.now()
#         )


#         return {
#             "user_id": user.UserId,
#             "log_id": user_log.LogId,
#             "action": user_log.Action,
#             "timestamp": user_log.Timestamp

#         }


# class LoginSerializer(serializers.Serializer):
#     Username = serializers.CharField(required=True)
#     Password = serializers.CharField(required=True)

#     def validate(self, data):
#         username = data.get('Username')
#         password = data.get('Password')

#         # Check if Username exists in the database
#         try:
#             user = User.objects.get(Username=username)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User does not exist.")

#         # Check if password matches
#         if not user.check_password(password):
#             raise serializers.ValidationError("Invalid password.")
        
#         return data
    
#     def create(self, validated_data):
#         username = validated_data.get('Username')
#         user = User.objects.get(Username=username)
        
#         # Create log entry with the user field correctly set
#         user_log = UserLog.objects.create(
#             user=user,
#             Action="Logged In",
#             Timestamp=timezone.now()
#         )

#         # Generate JWT token
#         refresh = RefreshToken.for_user(user)

       
    
#         return {
#             "UserId": user.UserId,  # Adjust to the correct primary key field
#             "LogId": user_log.LogId,
#             "Action": user_log.Action,
#             "Timestamp": user_log.Timestamp,
#             "RefreshToken": str(refresh),
#             "AccessToken": str(refresh.access_token),
#         }

class LoginSerializer(serializers.Serializer):
    Username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('Username')
        password = data.get('password')

        # Check if Username exists in the database
        try:
            user = User.objects.get(Username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        # Check if password matches
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")
        
        return data
    
    def create(self, validated_data):
        username = validated_data.get('Username')
        user = User.objects.get(Username=username)
        
        # Create log entry with the UserId field correctly set
        user_log = UserLog.objects.create(
            UserId=user,  # Correctly reference the UserId field
            Action="Logged In",
            Timestamp=timezone.now(),
            AccessToken="",  # Initialize the token fields
            RefreshToken=""
        )

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        # Update the log entry with the generated tokens
        user_log.AccessToken = str(refresh.access_token)
        user_log.RefreshToken = str(refresh)
        user_log.save()

        return {
            "UserId": user.UserId,  # Use the correct field for the user's primary key
            "LogId": user_log.LogId,
            "Action": user_log.Action,
            "Timestamp": user_log.Timestamp,
            "RefreshToken": user_log.RefreshToken,
            "AccessToken": user_log.AccessToken,
        }


class AddProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['ProductName', 'ProductDescription', 'ProductUnitPrice', 'ProductStatus', 'InitialLoadStock', 'StockLeft', 'ProductCategory']
    def create(self,validated_data):
        product=Product(
            ProductName=validated_data['ProductName'],
            ProductDescription=validated_data['ProductDescription'],
            ProductUnitPrice=validated_data['ProductUnitPrice'],
            ProductStatus=validated_data['ProductStatus'],
            InitialLoadStock=validated_data['InitialLoadStock'],
            StockLeft=validated_data['StockLeft'],
            ProductCategory=validated_data['ProductCategory']
        )
        product.save()
        return product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['ProductName', 'ProductDescription', 'ProductUnitPrice', 'ProductStatus', 'InitialLoadStock', 'StockLeft', 'ProductCategory']
    
class OrderPurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPurchased
        fields = ['user','Product','Quantity','TotalPrice']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
    



