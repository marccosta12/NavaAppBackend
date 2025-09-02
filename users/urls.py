from django.urls import path
from .views import (RequestPhoneVerificationView, VerifyPhoneCodeView, SetEmailView, VerifyEmailCodeView, SetUsernameView, SetPasswordView, 
                    LoginView, GetUsersView, UpdateUsersView, KycUploadDocumentView, KycUploadSelfieView)

urlpatterns = [
    path("auth/request-phone-verification", RequestPhoneVerificationView.as_view()),
    path("auth/verify-phone-code", VerifyPhoneCodeView.as_view()),
    path('auth/set-email', SetEmailView.as_view()),
    path('auth/verify-email-code', VerifyEmailCodeView.as_view()),
    path("auth/set-username", SetUsernameView.as_view(), name="set-username"),
    path("auth/set-password", SetPasswordView.as_view(), name="set-password"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("users/me", GetUsersView.as_view(), name="me"),
    path("users/update", UpdateUsersView.as_view(), name="me-update"),
    path("kyc/upload-document", KycUploadDocumentView.as_view(), name="kyc-upload-document"),
    path("kyc/upload-selfie", KycUploadSelfieView.as_view(), name="kyc-upload-selfie"),
]
