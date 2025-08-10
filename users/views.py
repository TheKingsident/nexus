from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, UserRegistrationSerializer, 
    UserProfileUpdateSerializer
)
from .tasks import send_welcome_email


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()

        send_welcome_email.delay(user.email,
                                 user.username)
        
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        })
    else:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        # Delete the user's token to logout
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout successful'
        })
    except:
        return Response({
            'error': 'Error logging out'
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(UserProfileSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveAPIView):
    """Get user details by ID"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current authenticated user"""
    return Response({
        'user': UserSerializer(request.user).data,
        'profile': UserProfileSerializer(request.user.profile).data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def admin_status(request):
    """Check if admin/superuser exists"""
    superuser_exists = User.objects.filter(is_superuser=True).exists()
    superuser_count = User.objects.filter(is_superuser=True).count()
    total_users = User.objects.count()
    
    return Response({
        'superuser_exists': superuser_exists,
        'superuser_count': superuser_count,
        'total_users': total_users,
        'message': 'Superuser exists' if superuser_exists else 'No superuser found'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def create_admin(request):
    """Create admin user via API (backup method)"""
    # Only allow if no superuser exists
    if User.objects.filter(is_superuser=True).exists():
        return Response({
            'error': 'Superuser already exists'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    username = request.data.get('username', 'admin')
    email = request.data.get('email', 'admin@example.com')
    password = request.data.get('password', 'admin123')
    
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        return Response({
            'message': f'Superuser "{username}" created successfully',
            'username': username,
            'email': email
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            'error': f'Failed to create superuser: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
