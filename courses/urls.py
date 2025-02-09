from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses import views

router = DefaultRouter()
router.register('courses', views.CourseViewSet, basename='course')
router.register('modules', views.ModuleViewSet, basename='module')
router.register('classes', views.ClassViewSet, basename='class')
router.register('students', views.StudentViewSet, basename='student')
router.register('students_classes', views.StudentClassViewSet, basename='student-class')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterUserApiView.as_view(), name='register'),
    path('update/<int:pk>/', views.UpdateUserApiView.as_view(), name='update-user'),
    path('login/', views.LoginApiView.as_view(), name='login'),
    path('buy/', views.BuyApiView.as_view(), name='buy'),

    path('home/', views.home, name='home'),
    path('course/<int:course_id>/', views.course, name='course'),

    # urls cart
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:course_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove_item_cart/<int:item_id>/', views.remove_item_cart, name='remove-item-cart'),
    
    # urls login render
    path('login_user/', views.login_view, name='login-user'),
    path('logout_user/', views.logout_view, name='logout-user'),
    path('register_user/', views.register_view, name='register-user')
]