from django.conf.urls import include
from django.urls import path
from strugglebusapi.views import register_user, login_user, TasksViewSet
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'tasks', TasksViewSet, 'task')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
