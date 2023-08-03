from rest_framework import serializers
from .model import Todo
from home.models.tech_family import TechFamily

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user"]

class TFSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechFamily
        fields = ["name", "pic", "pic_email", "slug", "project", "created_at", "updated_at"]
