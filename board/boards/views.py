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
        form = BoardForm(request.POST)
        if form.is_valid():
            board = Board.objects.create(
                name = "테스트 이름",
                email = "테스트 이메일",
                title = form['title'],
                contents = form['contents'],
            )
            return redirect('detail', idx=board.idx)
        else:
            return render(request, 'board/create.html', {'form': form})
    else:
        form = BoardForm()
    return render(request, 'board/create.html', {'form': form})