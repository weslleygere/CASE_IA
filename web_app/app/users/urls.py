from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    UserEditView,
    UserDeleteView,
    UserListView,
    UserDetailView,
    UserSearchView,
    PasswordRequestView,
    PasswordChangeView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<int:pk>/edit/', UserEditView.as_view(), name='user_edit'),
    path('<int:pk>/delete-account/', UserDeleteView.as_view(), name='delete_account'),
    path('user-list/', UserListView.as_view(), name='user_list'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('search/', UserSearchView.as_view(), name='user_search'),
    path('reset-password/request/', PasswordRequestView.as_view(), name='reset_password_request'),
    path('reset-password/change/<uidb64>/<token>/', PasswordChangeView.as_view(), name='reset_password_change'),
]