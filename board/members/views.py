from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Member
from rest_framework.views import APIView
from .serializers import MemberSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import bcrypt
import re

class SignUpAPI(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']
        
        if not re.search("[@]", email) or not re.search("[.]", email):
            return Response({"message": "이메일 오류"}, status=400)
        
        if len(password) < 8 or not re.search("[0-9]", password) or not re.search("[a-zA-Z]", password) or not re.search("[*~!#$^%?]", password):
            return Response({"message": "비밀번호 오류"}, status=400)
        
        try:
            Member.objects.get(email=email)
        except Member.DoesNotExist:
            member = Member.objects.create(
                name = data['name'],
                email = email,
                password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            )
            token = TokenObtainPairSerializer.get_token(member)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = {
                "message": "회원가입 성공",
                "member": {
                    "name": data['name'],
                    "email": email,
                },
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                }
            }
            return Response(res, status=200)
        
        return Response({"message": "회원가입 실패"}, status=400)
    
class SignInAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data['email']
            password = data['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), bytes(Member.objects.get(email=email).password, "utf-8")):
                token = TokenObtainPairSerializer.get_token(Member.objects.get(email=email))
                refresh_token = str(token)
                access_token = str(token.access_token)
                res = {
                    "message": "로그인 성공",
                    "member": {
                        "name": Member.objects.get(email=email).name,
                        "email": email,
                    },
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    }
                }
                return Response(res, status=200)
            
            return Response({"message": "로그인 실패"}, status=400)
        except KeyError:
            return Response({"message": "로그인 데이터 오류"}, status=400)
        except Member.DoesNotExist:
            return Response({"message": "로그인 정보 없음"}, status=400)