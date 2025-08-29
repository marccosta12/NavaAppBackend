from django.urls import path
from .views import RequestPhoneVerificationView, VerifyPhoneCodeView

urlpatterns = [
    path("auth/request-phone-verification", RequestPhoneVerificationView.as_view()),
    path("auth/verify-phone-code", VerifyPhoneCodeView.as_view()),
]
