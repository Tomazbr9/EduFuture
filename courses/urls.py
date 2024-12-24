from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, ModuleViewSet, 
    ClassViewSet, RegisterUserApiView,
    LoginApiView)

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('modules', ModuleViewSet, basename='module')
router.register('classes', ClassViewSet, basename='class')

urlpatterns = [
    path('api/', include(router.urls)),
    path('register/', RegisterUserApiView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login')
]