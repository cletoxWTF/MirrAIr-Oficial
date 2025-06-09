from rest_framework import serializers
from .models import Traduction

class TraductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traduction
        fields = ('name', 'description', 'score', 'votes', 'finalScore')
