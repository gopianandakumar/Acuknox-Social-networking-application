# friends/views.py

from rest_framework import viewsets, status,request
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .throttling import FriendRequestRateThrottle
from .serializers import UserSerializer
import datetime
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination

from . import serializers


class UserViewset(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user, password = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'detail': 'Created User Successfully', 'password': password, 'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def login(self, request):
	    try:
	        email = request.data['email'].lower()
	        user = self.get_queryset().get(email=email)
	        if user.check_password(request.data['password']):
	            token, _ = Token.objects.get_or_create(user=user)
	            return Response({'AuthToken': token.key})
	        else:
	            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
	    except User.DoesNotExist:
        	return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)


    from rest_framework.permissions import IsAuthenticated

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            print("dd")
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        


class SearchUsersPagination(PageNumberPagination):
    page_size = 10  # Default records per page

class SearchUsersView(viewsets.ModelViewSet):
    pagination_class = SearchUsersPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        search_keyword = request.GET.get('search_keyword')
        page_number = int(request.GET.get('page', 1))

        if not search_keyword:
            return Response({'error': 'Search keyword is required'}, status=400)

        users = User.objects.all()  # Query all users (optimize based on your use case)
        filtered_users = []

        # Exact email match
        for user in users:
            if user.email.lower() == search_keyword.lower():
                filtered_users.append(user)
                break  # Exact email match takes precedence

        # Partial name match (case-insensitive)
        if not filtered_users:
            name_pattern = re.compile(rf"^{search_keyword.lower()}.*|.*{search_keyword.lower()}$", re.IGNORECASE)
            for user in users:
                if name_pattern.match(user.name.lower()):
                    filtered_users.append(user)

        page = self.paginate_queryset(filtered_users)
        serializer = UserSerializer(page, many=True)  # Replace with your user serializer

        return Response({
            'search_keyword': search_keyword,
            'users': serializer.data,
            'page_number': page.number,
            'total_pages': page.paginator.num_pages,
            'has_previous': page.has_previous(),
            'has_next': page.has_next(),
            'total_count': page.paginator.count,
        })

# friends/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer, UserSerializer

class FriendRequestViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @ratelimit(key='user', rate='3/m', method='post', block=True)
    @action(detail=False, methods=['post'])
    def send_request(self, request):
        to_user_id = request.data.get('to_user_id')
        if not to_user_id:
            return Response({'detail': 'to_user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'detail': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def accept_request(self, request, pk=None):
        try:
            friend_request = FriendRequest.objects.get(id=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.delete()
        return Response({'detail': 'Friend request accepted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject_request(self, request, pk=None):
        try:
            friend_request = FriendRequest.objects.get(id=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.delete()
        return Response({'detail': 'Friend request rejected'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_friends(self, request):
        friendships = Friendship.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        friends = [friendship.user1 if friendship.user2 == request.user else friendship.user2 for friendship in friendships]
        return Response(UserSerializer(friends, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_pending_requests(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user)
        return Response(FriendRequestSerializer(pending_requests, many=True).data, status=status.HTTP_200_OK)
