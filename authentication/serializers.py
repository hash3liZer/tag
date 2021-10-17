from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.tokens import default_token_generator
from durin.models import Client
from django.conf import settings
from django.core.mail import send_mail
import datetime

class SignupSerializer(serializers.Serializer):
    f_name   = serializers.CharField()
    l_name   = serializers.CharField()
    username = serializers.CharField()
    email    = serializers.EmailField()
    password = serializers.CharField()
    orgname  = serializers.CharField(required=False, default="")
    pnumber  = serializers.CharField(required=False, default="")
    descrip  = serializers.CharField(required=False, default="")

    def validate_username(self, val):
        user = User.objects.filter(username=val).first()
        if user and user.is_active:
            raise serializers.ValidationError("Username has already been taken")

        return val

    def validate_email(self, val):
        user = User.objects.filter(email=val).first()
        if user and user.is_active:
            raise serializers.ValidationError("Email has already been taken")

        return val

    def create(self, vdata):
        tosuper = True if not User.objects.filter(is_active=True).first() else False
        tostaff = tosuper

        user = User.objects.filter(username=vdata['username']).first()
        clp  = True if user else False
        user = User.objects.create(username=vdata['username']) if not user else user

        user.email=vdata['email']
        user.is_staff=tostaff
        user.is_superuser=tosuper
        user.orgname=vdata['orgname']
        user.pnumber=vdata['pnumber']
        user.descrip=vdata['descrip']
        user.is_active=False

        user.set_password(vdata['password'])
        user.save()

        if not clp:
            client = Client.objects.create(
                name=f"{vdata['email']}@org"
            )
            client.save()
            client = Client.objects.create(
                name=f"{vdata['email']}@res"
            )
            client.save()

        return user

class ResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, vdata):
        user    = User.objects.filter(email=vdata['email'], is_active=True).first()
        if not user:
            return

        token, expiry = default_token_generator.make_token(user, settings.EMAIL_TOKEN_LIFE)
        subject = "Reset Password"
        email   = f"Reset link for your {user.username}: {token}"

        send_mail(
            subject,
            email,
            settings.EMAIL_FROM_ADDRESS,
            [user.email]
        )

        return user
