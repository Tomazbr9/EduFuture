from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, ClassViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('modules', ModuleViewSet, basename='module')
router.register('classes', ClassViewSet, basename='class')

urlpatterns = router.urls