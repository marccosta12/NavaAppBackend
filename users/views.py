from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequestPhoneVerificationSerializer, VerifyPhoneCodeSerializer


class RequestPhoneVerificationView(APIView):
    def post(self, request):
        serializer = RequestPhoneVerificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "data": {"message": "Verification code sent"}},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyPhoneCodeView(APIView):
    def post(self, request):
        serializer = VerifyPhoneCodeSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "success": True,
                "data": {"phoneVerified": True}
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)