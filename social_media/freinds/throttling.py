# friends/throttling.py

from rest_framework.throttling import UserRateThrottle

class FriendRequestRateThrottle(UserRateThrottle):
    rate = '3/minute'  # Allow 3 requests per minute per user

