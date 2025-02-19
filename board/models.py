from django.db import models
from django.utils import timezone

class Board(models.Model):
    identifier = models.CharField(max_length=100, unique=True, help_text='唯一标识符')
    password = models.CharField(max_length=128, blank=True, null=True, help_text='可选密码')
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    is_admin_created = models.BooleanField(default=False, help_text='是否由管理员创建')
    admin_notes = models.TextField(blank=True, null=True, help_text='管理员备注')

    def __str__(self):
        return self.identifier

class BoardItem(models.Model):
    ITEM_TYPES = [
        ('text', '文本'),
        ('file', '文件'),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    text_content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='board_files/%Y/%m/%d/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.board.identifier} - {self.get_item_type_display()}'
