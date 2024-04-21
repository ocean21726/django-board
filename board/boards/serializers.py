from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Board         # member 모델 사용
        fields = ['title', 'contents']