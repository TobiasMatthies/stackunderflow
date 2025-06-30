from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationView, CustoLoginView

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustoLoginView.as_view(), name='api_token_auth'),
]
