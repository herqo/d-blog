from django.urls import path
from .views import register, user_login, user_logout, edit_user_profile, user_change_password, user_profile, user_visible
from .views import user_upload_photo


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('edit-profile/', edit_user_profile, name='edit_profile'),
    path('password-change/', user_change_password, name='password_change'),
    path('upload-profile-photo/', user_upload_photo, name='user_upload_photo'),
    path('user-visible/', user_visible, name='user_visible'),
    path('<username>/', user_profile, name='user_profile'),
]