from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class OrganizationSignupView(APIView):

    def post(self, req):
        serialized_data = OrganiationSignupSerializer(data=req.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        serialized_data.save()

        return Response({'success': True}, status=status.HTTP_201_CREATED)
