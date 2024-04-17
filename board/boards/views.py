from django.shortcuts import render, redirect
from .form import BoardForm
from .models import Board
from rest_framework.views import APIView

# Create your views here.

def list(request):
    if request.method == "GET":
        boardForm = BoardForm
        board = Board.objects.all()
        context = {
            'boardForm': boardForm,
            'board': board
        }
        return render(request, 'board/list.html', context)

def detail(request, idx):
    if request.method == "GET":
        board = Board.objects.get(idx=idx)
        context = {
            'board': board
        }
        return render(request, 'board/detail.html', context)

def create(request):
    if request.method == "POST":
        data = request.POST
        title = data['title']
        contents = data['contents']
        
        try:
            board = Board.objects.create(
                name = '임시 테스트',
                email = 'test@test.com',
                title = title,
                contents = contents,
            )
            return render(request, 'board/detail.html', {'board': board})
        except Exception as e:
            return redirect('/')
    return render(request, 'board/create.html')