from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ...models.kubecost import KubecostReport

class KubecostReportViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        data = KubecostReport.report(from_date, to_date)

        # data = {
        #     "from_date": from_date,
        #     "to_date": to_date
        # }

        return Response(data, status=status.HTTP_200_OK)
