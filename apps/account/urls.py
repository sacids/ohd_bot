from django.urls import path
from django.urls.resolvers import URLPattern
from .views import LogoutView, LoginView,  ChangePasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", LoginView.as_view() , name="login"),  
    path("login", LoginView.as_view() , name="login"),  
    path("logout", LogoutView.as_view(), name="logout"),
    path("change-password", ChangePasswordView.as_view(), name="change-password"),

    #reset password
    # path("reset-password/", auth_views.PasswordResetView.as_view( template_name="accounts/password_reset.html"), name="password_reset"),
    # path("reset-password/done/", auth_views.PasswordResetDoneView.as_view( template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    # path("reset-password-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    # path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view( template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    
]