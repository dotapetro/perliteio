from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base import views

router = DefaultRouter()
router.register(r'tasks', views.TasksViewSet)
router.register(r'solutions', views.SolutionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
