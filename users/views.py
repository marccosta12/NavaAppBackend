from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequestPhoneVerificationSerializer, VerifyPhoneCodeSerializer, SetEmailSerializer, VerifyEmailCodeSerializer, SetUsernameSerializer, SetPasswordSerializer


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
    
class SetEmailView(APIView):
    def post(self, request):
        serializer = SetEmailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": {"emailSet": True}
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailCodeView(APIView):
    def post(self, request):
        serializer = VerifyEmailCodeSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "success": True,
                "data": {"emailVerified": True}
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetUsernameView(APIView):
    def post(self, request):
        serializer = SetUsernameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": {"usernameSet": True}
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetPasswordView(APIView):
    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "data": {"passwordSet": True}
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


