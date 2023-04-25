from django.urls import path

from foodapp.views import RestaurantRegistrationView, TodaysVoteView, MenuDetailedView, MenuCreateView, VoteCreateView, \
    UserRegistrationView

urlpatterns = [
    path('newrestaurant/', RestaurantRegistrationView.as_view(), name='new_restaurant'),
    path('todaysmenus/', TodaysVoteView.as_view(), name='todays_vote'),
    path('menu/<int:pk>/', MenuDetailedView.as_view(), name='menu_details'),
    path('menu/create/', MenuCreateView.as_view(), name='menu_create'),
    path('vote/<int:menu_id>/', VoteCreateView.as_view(), name='vote-create'),
    path('register/', UserRegistrationView.as_view(), name='registration')
]
