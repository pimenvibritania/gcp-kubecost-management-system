from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..serializers import ServiceSerializer
from django.db import IntegrityError
from ..models.kubecost import get_service

class ServiceViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        data = get_service()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        data = {
            'name': request.data.get('name'), 
            'service_type': request.data.get('service_type'), 
            'project': request.data.get('project'),
            'tech_family': request.data.get('tech_family_id'),
        }

        serializer = ServiceSerializer(data=data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle the IntegrityError
            error_response = {
                "error": f"Duplicate entry for {request.data.get('name')}"
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
