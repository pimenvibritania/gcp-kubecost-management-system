from rest_framework import serializers
from .model import Todo
from home.models.tech_family import TechFamily
from home.models.index_weight import IndexWeight

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]

class TFSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechFamily
        fields = ["name", "pic", "pic_email", "slug", "project", "created_at", "updated_at"]

class IndexWeightSerializer(serializers.ModelSerializer):
    tech_family = serializers.PrimaryKeyRelatedField(
        queryset=TechFamily.objects.all(), 
        many=False
        )

    class Meta:
        model = IndexWeight
        fields = ["value", "environment", "created_at", "tech_family"]
    