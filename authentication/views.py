from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from durin.views import LoginView
from durin.views import LogoutView
from authentication.models import *
from authentication.serializers import *
from django_email_verification import send_email
from django.contrib.auth.signals import user_logged_in

class SignupView(APIView):

    def post(self, req):
        serialized_data = SignupSerializer(data=req.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        serialized_data.save()

        send_email(serialized_data.instance, thread=False)

        return Response({
            'success': True,
            'detail': 'Please verify your account using the email we sent you'
        },  status=status.HTTP_201_CREATED)

class SigninView(LoginView):

    def post(self, req, dom):
        user = User.objects.filter(email=req.data["email"], is_active=True).first()
        req.data['username'] = user.username if user else "@.asd"
        req.data['client'] = f"{req.data.get('email')}@{dom}"
        req.user = self.validate_and_return_user(req)
        client = self.get_client_obj(req)
        token_obj = self.get_token_obj(req, client)
        user_logged_in.send(
            sender=req.user.__class__, request=req, user=req.user
        )
        data = self.get_post_response_data(req, token_obj)
        return Response(data)

class SignoutView(LogoutView):
    pass

class ResetView(APIView):

    def post(self, req):
        serialized_data = SignupSerializer(data=req.data, context={'req': req})
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        serialized_data.save()

        return Response(
            {
                'success': True,
                'detail': 'If your email exists in our system, you would receive an email'
            },
            status=status.HTTP_200_OK
        )
