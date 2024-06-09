from rest_framework.permissions import IsAuthenticated

class IsFriendRequestOwner(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ('PUT', 'DELETE'):
            # Check if user owns the friend request
            obj = view.get_object()
            return (obj.from_user == request.user or obj.to_user == request.user)
        return super().has_permission(request, view)
