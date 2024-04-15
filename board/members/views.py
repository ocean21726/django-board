from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import Member
from rest_framework.views import APIView
from .serializers import MemberSerializer

import bcrypt
import re

class SignUpAPI(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']
        
        if not re.search("[@]", email) or not re.search("[.]", email):
            return Response({"result: 이메일 오류"}, status=400)
        
        if len(password) < 8 or not re.search("[0-9]", password) or not re.search("[a-zA-Z]", password) or not re.search("[*~!#$^%?]", password):
            return Response({"result: 비밀번호 오류"}, status=400)
        
        try:
            Member.objects.get(email=email)
        except Member.DoesNotExist:
            Member.objects.create(
                name = data['name'],
                email = email,
                password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            )
            return Response({"result: 회원가입 성공"}, status=200)
        
        return Response({"result: 회원가입 실패"}, status=400)