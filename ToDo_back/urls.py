from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/registration/', views.registration, name='registration'),
    path('api/login/', views.login, name='login'),
    path('api/logout/', views.logout, name='logout'),

    path('api/todo/get/', views.get_list_todo, name='todos-list'),
    path('api/todo/post/', views.post_todo, name='todo-post'),
    path('api/todo/delete/<int:id>/', views.delete_todo, name='todo-delete'),
    path('api/todo/put/status/<int:id>/', views.put_status_todo, name='todo-put-status'),
    path('api/todo/put/text/<int:id>/', views.put_text_todo, name='todo-put-text'),

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]