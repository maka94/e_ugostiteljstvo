from django.urls import path

from apps.users import views

urlpatterns = [
    path('test', views.TestView.as_view()),
    path('register', views.RegisterUserView.as_view()),
    path('login', views.LoginUserView.as_view()),
    path('logout', views.LogoutUserView.as_view()),
    path('change_password', views.ChangePasswordView.as_view()),
    path('profile', views.ProfileView.as_view()),
]