"""
URL configuration for clipboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from board import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', views.create_board, name='create_board'),
    path('access/', views.access_board, name='access_board'),
    path('b/<str:identifier>/', views.board_detail, name='board_detail'),
    path('b/<str:identifier>/verify/', views.board_detail, name='verify_board'),
    path('b/<str:identifier>/add/', views.add_item, name='add_item'),
    path('b/<str:identifier>/delete/<int:item_id>/', views.delete_item, name='delete_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
