from django.urls import path
from todolist.views import delete_task, login_user
from todolist.views import logout_user
from todolist.views import register
from todolist.views import show_todolist
from todolist.views import create_task
from todolist.views import delete_task
from todolist.views import update_task

app_name='todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-task/', create_task, name='create-task'),
    path('delete_task/<str:task_id>/', delete_task, name="delete_task"),
    path('update_task/<str:task_id>/', update_task, name="update_task"),

]