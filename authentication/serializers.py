from rest_framework import serializers
from django.contrib.auth.models import User
from durin.models import Client
import datetime

class OrganiationSignupSerializer(serializers.Serializer):
    f_name   = serializers.CharField()
    l_name   = serializers.CharField()
    username = serializers.CharField()
    email    = serializers.EmailField()
    password = serializers.CharField()
    orgname  = serializers.CharField()
    pnumber  = serializers.CharField()
    descrip  = serializers.CharField()

    def validate_username(self, val):
        if User.objects.filter(username=val).first():
            raise serializers.ValidationError("Username has already been taken")

        return val

    def validate_email(self, val):
        if User.objects.filter(email=val).first() and Client.objects.filter(name=):
            raise serializers.ValidationError("Email has already been taken")

        return val

    def validate(self, udata):
        cona = User.objects.filter(username=udata['username']).first()
        conb = Client.objects.filter(name=f"{data['username']}@org").first()
        if cona and conb:
            raise serializers.ValidationError("Username has already been choosen")

        cona = User.objects.filter(email=udata['email']).first()
        if cona and conb:
            raise serializers.ValidationError("Email has already been choosen")

        return udata

    def create(self, vdata):
        tosuper = True if not User.objects.all().first() else False
        tostaff = tosuper

        user = User.objects.filter(username=udata['username']).first()
        if not user:
            user = User.objects.create(
                        username=vdata['username'],
                        email=vdata['email'],
                        is_staff=tostaff,
                        is_superuser=tosuper
                    )

            user.set_password(vdata['password'])
            user.save()

        
