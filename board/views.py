from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib import messages
from .models import Board, BoardItem
import mimetypes
import json

def home(request):
    return render(request, 'board/home.html')

def create_board(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        
        if Board.objects.filter(identifier=identifier).exists():
            return JsonResponse({'error': '此标识符已被使用'}, status=400)
        
        board = Board.objects.create(
            identifier=identifier,
            password=password
        )
        return redirect('board_detail', identifier=identifier)
    
    return render(request, 'board/create.html')

def access_board(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')
        
        try:
            board = Board.objects.get(identifier=identifier)
            
            if board.password:
                if not password or password != board.password:
                    return JsonResponse({'error': '密码错误'}, status=403)
                request.session[f'board_access_{board.identifier}'] = True
            
            return redirect('board_detail', identifier=identifier)
        except Board.DoesNotExist:
            return JsonResponse({'error': '剪贴板不存在'}, status=404)
    
    return render(request, 'board/access.html')

def verify_board_access(request, board):
    if board.password:
        session_key = f'board_access_{board.identifier}'
        if not request.session.get(session_key):
            return False
        return True
    return True

def board_detail(request, identifier):
    board = get_object_or_404(Board, identifier=identifier)
    
    if request.method == 'POST' and 'password' in request.POST:
        password = request.POST.get('password')
        if board.password and password == board.password:
            request.session[f'board_access_{board.identifier}'] = True
            return JsonResponse({'success': True})
        return JsonResponse({'error': '密码错误'}, status=403)
    
    if board.password and not verify_board_access(request, board):
        return render(request, 'board/password.html', {'board': board})
    
    items = board.items.all()
    return render(request, 'board/detail.html', {'board': board, 'items': items})

@csrf_exempt
def add_item(request, identifier):
    board = get_object_or_404(Board, identifier=identifier)
    
    if not verify_board_access(request, board):
        return HttpResponseForbidden('需要密码验证')
    
    if request.method == 'POST':
        item_type = request.POST.get('type')
        item = BoardItem(board=board, item_type=item_type)
        
        if item_type == 'text':
            item.text_content = request.POST.get('content')
        elif item_type == 'file' and request.FILES.get('file'):
            file = request.FILES['file']
            item.file_name = file.name
            item.mime_type = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
            item.file.save(file.name, file)
        print("aaaaaaaaaaa")
        item.save()
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': '不支持的请求方法'}, status=405)

@csrf_exempt
def delete_item(request, identifier, item_id):
    board = get_object_or_404(Board, identifier=identifier)
    
    if not verify_board_access(request, board):
        return HttpResponseForbidden('需要密码验证')
    
    item = get_object_or_404(BoardItem, id=item_id, board=board)
    
    if request.method == 'POST':
        if item.file:
            item.file.delete()
        item.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': '不支持的请求方法'}, status=405)
