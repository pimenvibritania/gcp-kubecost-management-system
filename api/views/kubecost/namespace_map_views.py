from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ...serializers import KubecostNamespaceMapSerializer
from django.db import IntegrityError
from ...models.kubecost import get_namespace_map

class KubecostNamespaceMapViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        data = get_namespace_map()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        data = {
            'namespace': request.data.get('namespace'), 
            'service': request.data.get('service_id'), 
            'project': request.data.get('project')
        }

        serializer = KubecostNamespaceMapSerializer(data=data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle the IntegrityError
            error_response = {
                "error": f"Duplicate entry for {request.data.get('namespace')}"
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
