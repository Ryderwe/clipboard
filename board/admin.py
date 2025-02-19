from django.contrib import admin
from .models import Board, BoardItem

class BoardAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'created_at', 'last_modified', 'is_admin_created']
    list_filter = ['is_admin_created', 'created_at']
    search_fields = ['identifier', 'admin_notes']
    readonly_fields = ['created_at', 'last_modified']
    fieldsets = [
        (None, {'fields': ['identifier', 'password']}),
        ('管理员信息', {'fields': ['is_admin_created', 'admin_notes']}),
        ('时间信息', {'fields': ['created_at', 'last_modified']}),
    ]
    list_display_links = ['identifier']
    list_per_page = 20

    def identifier(self, obj):
        return obj.identifier
    identifier.short_description = '标识符'
    identifier.admin_order_field = 'identifier'

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = '创建时间'
    created_at.admin_order_field = 'created_at'

    def last_modified(self, obj):
        return obj.last_modified
    last_modified.short_description = '最后修改'
    last_modified.admin_order_field = 'last_modified'

    def is_admin_created(self, obj):
        return obj.is_admin_created
    is_admin_created.short_description = '管理员创建'
    is_admin_created.admin_order_field = 'is_admin_created'

class BoardItemAdmin(admin.ModelAdmin):
    list_display = ['board', 'item_type', 'file_name', 'created_at']
    list_filter = ['item_type', 'created_at']
    search_fields = ['board__identifier', 'file_name', 'text_content']
    readonly_fields = ['created_at', 'last_modified']
    fieldsets = [
        (None, {'fields': ['board', 'item_type']}),
        ('内容', {'fields': ['text_content', 'file', 'file_name', 'mime_type']}),
        ('时间信息', {'fields': ['created_at', 'last_modified']}),
    ]
    list_display_links = ['board']
    list_per_page = 20

    def get_list_display(self, request):
        return ['board', 'item_type', 'file_name', 'created_at']

    def board(self, obj):
        return obj.board
    board.short_description = '剪贴板'
    board.admin_order_field = 'board'

    def item_type(self, obj):
        return obj.get_item_type_display()
    item_type.short_description = '类型'
    item_type.admin_order_field = 'item_type'

    def file_name(self, obj):
        return obj.file_name
    file_name.short_description = '文件名'
    file_name.admin_order_field = 'file_name'

    def created_at(self, obj):
        return obj.created_at
    created_at.short_description = '创建时间'
    created_at.admin_order_field = 'created_at'

admin.site.register(Board, BoardAdmin)
admin.site.register(BoardItem, BoardItemAdmin)
