from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/todo/get/', views.get_list_todo, name='todos-list'),
    path('api/todo/post/', views.post_todo, name='todo-post'),
    path('api/todo/delete/<int:id>/', views.delete_todo, name='todo-delete'),
    path('api/todo/put/status/<int:id>/', views.put_status_todo, name='todo-put-status'),
    path('api/todo/put/text/<int:id>/', views.put_text_todo, name='todo-put-text'),
]
