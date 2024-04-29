from rest_framework import serializers
from rest_framework.validators import UniqueValidator # 이메일 중복 방지 검증 도구
from django.contrib.auth.password_validation import validate_password # django 기본 pw 검증 도구
from .models import Member

import re
import bcrypt

class RegisterSerializer(serializers.ModelSerializer) :
    name = serializers.CharField(
        required = True,
    ),
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=Member.objects.all())],
    )
    password = serializers.CharField(
        required = True,
        validators = [validate_password],
    )
    class Meta :
        model = Member         # member 모델 사용
        fields = '__all__'     # 모든 필드 포함
        
    def validate_password(self, password):
        if not re.search("[0-9]", password) or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[*~!#$^%?]", password):
            raise serializers.ValidationError('대/소문자, 숫자, 특수문자를 포함한 8자 이상의 비밀번호를 입력하세요.')
        return password
    
    def create(self, validated_data):
        member = Member.objects.create(
            name = validated_data['name'],
            email = validated_data['email'],
            password = bcrypt.hashpw(validated_data['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
        )
        return member
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        try:
            member = Member.objects.get(email=data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), bytes(member.password, "utf-8")):
                return member
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        except Member.DoesNotExist:
            raise serializers.ValidationError('일치하는 회원 정보가 없습니다.')
    