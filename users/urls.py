from django.urls import path
from .views import RequestPhoneVerificationView, VerifyPhoneCodeView, SetEmailView, VerifyEmailCodeView, SetUsernameView, SetPasswordView

urlpatterns = [
    path("auth/request-phone-verification", RequestPhoneVerificationView.as_view()),
    path("auth/verify-phone-code", VerifyPhoneCodeView.as_view()),
    path('auth/set-email', SetEmailView.as_view()),
    path('auth/verify-email-code', VerifyEmailCodeView.as_view()),
    path("auth/set-username", SetUsernameView.as_view(), name="set-username"),
    path("auth/set-password", SetPasswordView.as_view(), name="set-password"),
]
