import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import User  # Import your custom User model

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # No token provided, no authentication performed

        token = auth_header.split(' ')[1]  # Extract the token after "Bearer "

        try:
            # Decode the JWT token to get the payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        try:
            # Retrieve the user based on the user_id in the payload
            user = User.objects.get(id=payload['user_id'])  # Make sure 'id' is the primary key
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        # Return the user and None (the second value is for authentication backend)
        return (user, None)
