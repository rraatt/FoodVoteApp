from django.contrib.auth.models import User
from rest_framework import serializers

from foodapp.models import Restaurant, Menu, Vote

"""Same serializers, but lets imagine that they somehow add support for legacy frontend"""


class UserRegistrationSerializerLegacy(serializers.ModelSerializer):
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
        print('doing legacy stuff')
        return user


class RestaurantCreateSerializerLegacy(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print('still legacy')
        return representation

    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'description']


class TodaysVoteSerializerLegacy(serializers.ModelSerializer):
    """Serializer for displaying menus for today, including votes count"""
    owner = RestaurantSerializer()

    class Meta:
        model = Menu
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['vote_count'] = instance.get_count()
        print('its some old app you use')
        return representation


class MenuSerializerLegacy(serializers.ModelSerializer):
    """Serializer for detailed view of Menu"""
    owner = RestaurantSerializer(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'

    def create(self, validated_data):
        print('legacy')
        user = self.context['request'].user
        restaurant = user.restaurant.get()
        validated_data['owner'] = restaurant
        menu = Menu.objects.create(**validated_data)
        return menu


class VoteCreateSerializerLegacy(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['menu']

    def create(self, validated_data):
        print('yeah, legacy')
        user = self.context['request'].user
        menu = validated_data['menu']
        vote = Vote.objects.create(user=user, menu=menu)
        return vote
