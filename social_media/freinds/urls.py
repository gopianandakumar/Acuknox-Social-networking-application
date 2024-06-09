from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FriendRequestViewSet, UserViewset, SearchUsersView

# Create a router and register the VendorViewSet with it
router = DefaultRouter()
router.register(r'user', UserViewset)
router.register(r'search', SearchUsersView, basename='search')
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-requests')


urlpatterns = router.urls