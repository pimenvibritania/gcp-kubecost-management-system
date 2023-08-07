from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ...serializers import KubecostNamespaceSerializer
from django.db import IntegrityError
from ...models.kubecost import Kubecost

class KubecostInsertDataViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        date = request.data.get('date')

        Kubecost.insert_data(date)

        message = f"Kubecost data '{date}' successfully inserted."
        print(message)

        data = {
            "status": "success",
            "message": message
        }
        return Response(data, status=status.HTTP_200_OK)
