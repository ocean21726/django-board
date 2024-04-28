from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Member
from rest_framework.views import APIView
from .serializers import MemberSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib import messages

import bcrypt
import re

# 회원가입 API
class SignUpAPI(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']
        
        # 이메일 유효성 검사
        if not re.search("[@]", email) or not re.search("[.]", email):
            return Response({"message": "이메일 오류"}, status=400)
        
        # 비밀번호 유효성 검사
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
            # jwt 생성
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

class NewSignUpAPI(generics.CreateAPIView):
    # queryset = Member.objects.all()
    serializer_class = MemberSerializer
    
    def post(self, request):
        serializer = MemberSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인 API
class SignInAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data['email']
            password = data['password']
            member = Member.objects.get(email=email)
            
            # 비밀번호 일치 여부 확인
            if bcrypt.checkpw(password.encode('utf-8'), bytes(member.password, "utf-8")):
                token = TokenObtainPairSerializer.get_token(member)
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
                return Response(res, status=200, headers={"Authorization": access_token})
            
            return Response({"message": "로그인 실패"}, status=400)
        except KeyError:
            return Response({"message": "로그인 데이터 오류"}, status=400)
        except Member.DoesNotExist:
            return Response({"message": "로그인 정보 없음"}, status=400)

# 회원가입        
def register(request):
    if request.method == 'POST':
        data = request.POST
        email = data['email']
        password = data['password']
        
        # 이메일 유효성 검사
        if not re.search("[@]", email) or not re.search("[.]", email):
            messages.error(request, '이메일 오류')
            return render(request, 'members/register.html')
        
        # 비밀번호 유효성 검사
        if len(password) < 8 or not re.search("[0-9]", password) or not re.search("[a-zA-Z]", password) or not re.search("[*~!#$^%?]", password):
            messages.error(request, '비밀번호 오류')
            return render(request, 'members/register.html')
        
        try:
            Member.objects.get(email=email)
        except Member.DoesNotExist:
            member = Member.objects.create(
                name = data['name'],
                email = email,
                password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            )
            # jwt 생성
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

            return redirect('/', res)
        messages.error(request, '회원가입 실패')
        return render(request, 'members/register.html')
    return render(request, 'members/register.html')

# 로그인
def login(request):
    if request.method == "POST":
        try:
            data = request.POST
            email = data['email']
            password = data['password']
            member = Member.objects.get(email=email)
            
            # 비밀번호 일치 여부 확인
            if bcrypt.checkpw(password.encode('utf-8'), bytes(member.password, "utf-8")):
                token = TokenObtainPairSerializer.get_token(member)
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
                return redirect('/', res)
            messages.error(request, "로그인 실패")
            return render(request, 'members/login.html')
        except KeyError:
            messages.error(request, "로그인 데이터 오류")
            return render(request, 'members/login.html')
        except Member.DoesNotExist:
            messages.error(request, "로그인 정보 없음")
            return render(request, 'members/login.html')
    return render(request, 'members/login.html')