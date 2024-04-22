from django.shortcuts import render, redirect
from .form import BoardForm
from .models import Board
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib import messages
from .serializers import BoardSerializer

# 게시글 목록
def list(request, order_type='earliest'):
    if request.method == "GET":
        if order_type == 'hitsd':       # 조회수 내림차순
            board = Board.objects.all().order_by('-view_count')
        elif order_type == 'hitsa':     # 조회수 오름차순
            board = Board.objects.all().order_by('view_count')
        elif order_type == 'latest':    # 작성일자 내림차순
            board = Board.objects.all().order_by('-idx')
        elif order_type == 'earliest':  # 작성일자 오름차순
            board = Board.objects.all().order_by('idx')
        else:
            return redirect('/')
        context = {
            'board': board
        }  
        return render(request, 'board/list.html', context)

# 게시글 상세
def detail(request, idx):
    if request.method == "GET":
        update_view(idx)
        board = Board.objects.get(idx=idx)
        context = {
            'board': board
        }
        return render(request, 'board/detail.html', context)

# 게시글 등록
def create(request):
    if request.method == "POST":
        data = request.POST
        title = data['title']
        contents = data['contents']
        
        # 빈칸 확인
        create_data = BoardSerializer(data=data)
        if create_data.is_valid():
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
        messages.error(request, '빈칸은 등록할 수 없습니다.')
        return render(request, 'board/create.html')
    return render(request, 'board/create.html')

# 게시글 수정
def update(request, idx):
    if request.method == "POST":
        data = request.POST
        title = data['title']
        contents = data['contents']
        
        # 빈칸 확인
        update_data = BoardSerializer(data=data)
        if update_data.is_valid():
            try:
                board = Board.objects.filter(idx=idx).update(
                    title = title,
                    contents = contents,
                    updated_at = timezone.now()
                )
                return redirect(request, 'board/detail', idx)
            except Exception as e:
                return redirect('/')
        messages.error(request, '빈칸은 등록할 수 없습니다.')
    board = Board.objects.get(idx=idx)
    context = {
        'board': board
    }
    return render(request, 'board/update.html', context)

# 게시글 삭제
def delete(request, idx):
    board = Board.objects.get(idx=idx)
    if request.method == "GET":
        try:
            board.delete()
            messages.success(request, '삭제되었습니다.')
            return redirect('/')
        except Exception as e:
            messages.error(request, '삭제 오류')
            return redirect('/')
    return render(request, 'board/detail.html', {'board': board})

# 게시글 조회수 업데이트
def update_view(idx):
    board = Board.objects.get(idx=idx)
    if board:
        Board.objects.filter(idx=idx).update(
            view_count = board.view_count + 1
        )