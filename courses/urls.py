from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, ModuleViewSet, 
    ClassViewSet, RegisterUserApiView,
    LoginApiView, InstructorViewSet, StudentViewSet, BuyApiView)

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('modules', ModuleViewSet, basename='module')
router.register('classes', ClassViewSet, basename='class')
router.register('instructors', InstructorViewSet, basename='instructor')
router.register('students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserApiView.as_view(), name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('buy/', BuyApiView.as_view(), name='buy')
]