from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ...serializers import KubecostDeploymentSerializer
from django.db import IntegrityError
from ...models.kubecost import get_kubecost_cluster

class KubecostDeploymentViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        data = {}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        data = {
            'cluster_name': request.data.get('cluster_name'), 
            'location': request.data.get('location'), 
            'gcp_project': request.data.get('gcp_project'),
            'company_project': request.data.get('company_project'),
            'environment': request.data.get('environment')
        }

        serializer = KubecostDeploymentSerializer(data=data)

        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle the IntegrityError
            error_response = {
                "error": f"Duplicate entry for {request.data.get('cluster_name')}"
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
