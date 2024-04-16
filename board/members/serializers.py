from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Member         # member 모델 사용
        fields = '__all__'     # 모든 필드 포함