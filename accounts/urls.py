from django.urls import path, include

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('', views.UserProfileView.as_view(), name='profile'),
        path('edit/', views.UserProfileUpdateView.as_view(), name='edit_profile')
    ]))
]
