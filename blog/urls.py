from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ChildViewSet, BlogViewSet, VlogViewSet, HomeFeedView, LogoutView, RegisterView, DetailVlogBlogView

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'children', ChildViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'vlogs', VlogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home-feed/', HomeFeedView.as_view(), name='home_feed'),
    path('detail/', DetailVlogBlogView.as_view(), name='detail'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
