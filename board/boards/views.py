from django.shortcuts import render, redirect
from .form import BoardForm
from .models import Board
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib import messages

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
        updateView(idx)
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

def update(request, idx):
    if request.method == "POST":
        data = request.POST
        title = data['title']
        contents = data['contents']
        
        try:
            board = Board.objects.filter(idx=idx).update(
                title = title,
                contents = contents,
                updated_at = timezone.now()
            )
            return redirect(request, 'board/detail', idx)
        except Exception as e:
            return redirect('/')
    else:
        board = Board.objects.get(idx=idx)
        context = {
            'board': board
        }
        return render(request, 'board/update.html', context)
    
def delete(request, idx):
    board = Board.objects.get(idx=idx)
    if request.method == "GET":
        try:
            board.delete()
            messages.success(request, '삭제되었습니다.')
            return redirect(request, 'board/list')
        except Exception as e:
                messages.error(request, '삭제 오류')
                return redirect('/')
    return render(request, 'board/detail.html', {'board': board})

def updateView(idx):
    board = Board.objects.get(idx=idx)
    if board:
        Board.objects.filter(idx=idx).update(
            view_count = board.view_count + 1
        )