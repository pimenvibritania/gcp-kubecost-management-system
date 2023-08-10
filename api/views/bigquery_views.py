from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from rest_framework.decorators import api_view, permission_classes as view_permission_classes
from rest_framework.permissions import IsAuthenticated
from dateutil.parser import parse
from django.http import HttpResponse 
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta
from ..models.bigquery import BigQuery
from ..serializers import TFSerializer, IndexWeightSerializer, BQQueryParamSerializer
from home.models.tech_family import TechFamily
from home.models.index_weight import IndexWeight
from itertools import chain
from django.utils import timezone

import asyncio

def validateFormat(value):
    try:
        parsed_date = parse(value)
        if parsed_date.strftime('%Y-%m-%d') != value:
            raise ValueError("Date format must be 'Y-m-d' (e.g., '2023-08-07')")
        
    except ValueError:
        raise ValidationError("Invalid date format. Must be 'Y-m-d' (e.g., '2023-08-07')")

def create_model_entry(data, date):
    data["created_at"] = date
    serializer = IndexWeightSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    print(f"Entry for {data} created")


def sync_index_weight(request, *args, **kwargs):

    start_date = datetime(2023, 1, 1).date()
    current_date = timezone.now().date()
    delta = timedelta(days=1)
    
    data = [
        {
            'value': 14.81, 
            'environment': "production", 
            'tech_family': 5
        },
        {
            'value':14.81, 
            'environment': "staging", 
            'tech_family': 5
        },
        {
            'value':14.81 , 
            'environment': "development", 
            'tech_family': 5
        },
        {
            'value': 0.67, 
            'environment': "production", 
            'tech_family': 9
        },
        {
            'value': 0.67, 
            'environment': "staging", 
            'tech_family': 9
        },
        {
            'value': 0.67, 
            'environment': "development", 
            'tech_family': 9
        },
        {
            'value': 84.51, 
            'environment': "production", 
            'tech_family': 6
        },
        {
            'value': 84.51, 
            'environment': "staging", 
            'tech_family': 6
        },
        {
            'value': 84.51, 
            'environment': "development", 
            'tech_family': 6
        },
        
        {
            'value': 63.83, 
            'environment': "production", 
            'tech_family': 1
        },
        {
            'value': 56.99, 
            'environment': "staging", 
            'tech_family': 1
        },
        {
            'value': 56.99, 
            'environment': "development", 
            'tech_family': 1
        },
        
        {
            'value': 25.53, 
            'environment': "production", 
            'tech_family': 2
        },
        {
            'value': 16.13, 
            'environment': "staging", 
            'tech_family': 2
        },
        {
            'value': 16.13, 
            'environment': "development", 
            'tech_family': 2
        },
        
        {
            'value': 10.64, 
            'environment': "production", 
            'tech_family': 3
        },
        {
            'value': 26.88, 
            'environment': "staging", 
            'tech_family': 3
        },
        {
            'value': 26.88, 
            'environment': "development", 
            'tech_family': 3
        },
    ]
    
    tasks = []
    date = start_date
    while date <= current_date:
        for i in range(0, len(data)):
            create_model_entry(data[i], date)
            # tasks.append(create_model_entry(data[i]))
        date += delta

    # await asyncio.gather(*tasks)

    return HttpResponse({"success": "ses."})
class BigQueryViews(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        
        if not date :
            return Response({"error": "Date parameter is required."}, status=400)
        
        validateFormat(date)
        
        data = BigQuery.get_project(date)
        
        return Response(data, status=status.HTTP_200_OK)
    
    @api_view(["GET"])
    def get_tf(self):
        tf_mdi = TechFamily.get_tf_mdi()
        tf_mfi = TechFamily.get_tf_mfi()

        serializer = TFSerializer(list(chain(tf_mdi, tf_mfi)), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def get_index_weight(from_date, to_date):
        data = IndexWeight.get_index_weight(from_date, to_date)
        serializer = IndexWeightSerializer(data, many=True)
        return serializer
    
    @api_view(["POST"])
    @view_permission_classes([IsAuthenticated])
    def post_index_weight(request, *args, **kwargs):

        data = {
            'value': request.data.get('value'), 
            'environment': request.data.get('environment'), 
            'tech_family': request.data.get('tech_family_id')
        }

        serializer = IndexWeightSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
