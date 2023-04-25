from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.utils import timezone
from rest_framework import generics, versioning
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .legacy_serializers import UserRegistrationSerializerLegacy, TodaysVoteSerializerLegacy, MenuSerializerLegacy, \
    RestaurantCreateSerializerLegacy, VoteCreateSerializerLegacy
from .models import Menu
from .permissions import IsOwnerOrReadOnly, IsRestaurantOwner
from .serializers import UserRegistrationSerializer, RestaurantCreateSerializer, TodaysVoteSerializer, MenuSerializer, \
    VoteCreateSerializer
from .services import get_menu_by_id


class UserRegistrationView(generics.CreateAPIView):
    """Registering employees into the system"""
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User account created successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

    def get_serializer_class(self):
        if float(self.request.version) < 1.0:
            return UserRegistrationSerializerLegacy
        return UserRegistrationSerializer


class RestaurantRegistrationView(generics.CreateAPIView):
    """View for registering a new restaurant, action can be performed only by user
    with admin rights. Creation process similar to regular registration, but
    restaurant name and description need to be specified"""
    queryset = User.objects.all()
    permission_classes = [IsAdminUser, ]

    def create(self, request, *args, **kwargs):
        """Creating a user account for restaurant manager and creating a restaurant instance, tied to new account"""
        if float(request.version) < 1.0:
            serializer = UserRegistrationSerializerLegacy
            restaurant_serializer = RestaurantCreateSerializerLegacy
        else:
            serializer = UserRegistrationSerializer
            restaurant_serializer = RestaurantCreateSerializer
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        restaurant_data = {
            'name': request.data['restaurant_name'],
            'description': request.data['restaurant_description'],
            'owner': user.id
        }
        restaurant_serializer = restaurant_serializer(data=restaurant_data)
        restaurant_serializer.is_valid(raise_exception=True)
        restaurant = restaurant_serializer.save()
        return Response({
            'message': 'User account and restaurant entry created successfully',
            'user_id': user.id,
            'restaurant_id': restaurant.id
        })


class TodaysVoteView(generics.ListAPIView):
    """View to display today's available menus and current voting results"""
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(day=timezone.now().date())
        return queryset

    def get_serializer_class(self):
        if float(self.request.version) < 1.0:
            return TodaysVoteSerializerLegacy
        return TodaysVoteSerializer


class MenuDetailedView(generics.RetrieveUpdateDestroyAPIView):
    """View for watching one menu, menu owner has rights to edit and delete menu"""
    queryset = Menu.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]

    def get_serializer_class(self):
        if float(self.request.version) < 1.0:
            return MenuSerializerLegacy
        return MenuSerializer


class MenuCreateView(generics.CreateAPIView):
    """Allows users, who are listed as a restaurant owner to create a menu"""
    queryset = Menu.objects.all()
    permission_classes = [IsRestaurantOwner, ]

    def get_serializer_class(self):
        if float(self.request.version) < 1.0:
            return MenuSerializerLegacy
        return MenuSerializer


class VoteCreateView(generics.CreateAPIView):
    """Model for creating votes, only one vote for user per day"""
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        menu_id = kwargs.get('menu_id')
        menu = get_menu_by_id(menu_id)
        data = {'user': request.user.id, 'menu': menu.id}
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            vote = serializer.save()
        except IntegrityError:
            return HttpResponseForbidden('You can vote only once a day')
        return Response({'message': 'Vote created successfully', 'vote_id': vote.id})

    def get_serializer_class(self):
        if float(self.request.version) < 1.0:
            return VoteCreateSerializerLegacy
        return VoteCreateSerializer
