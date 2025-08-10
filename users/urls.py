from django.urls import path
from .views import (
    UserRegistrationView, login_view, logout_view, 
    UserProfileView, UserDetailView, current_user, admin_status, create_admin
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('me/', current_user, name='current-user'),
    
    # Admin management
    path('admin-status/', admin_status, name='admin-status'),
    path('create-admin/', create_admin, name='create-admin'),
    
    # Profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
