from django.contrib.auth.models import User
from rest_framework import serializers

from foodapp.models import Restaurant, Menu, Vote


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registering employees into the system"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class RestaurantCreateSerializer(serializers.ModelSerializer):
    """Serializer used for creating a new restaurant"""
    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer used for nested use in Menu serializers"""
    class Meta:
        model = Restaurant
        fields = ['name', 'description']


class TodaysVoteSerializer(serializers.ModelSerializer):
    """Serializer for displaying menus for today, including votes count"""
    owner = RestaurantSerializer()

    class Meta:
        model = Menu
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['vote_count'] = instance.get_count()

        return representation


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for detailed view of Menu"""
    owner = RestaurantSerializer(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        restaurant = user.restaurant.get()
        print(type(restaurant))
        validated_data['owner'] = restaurant
        menu = Menu.objects.create(**validated_data)
        return menu


class VoteCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new Votes"""
    class Meta:
        model = Vote
        fields = ['menu']

    def create(self, validated_data):
        user = self.context['request'].user
        menu = validated_data['menu']
        vote = Vote.objects.create(user=user, menu=menu)
        return vote
