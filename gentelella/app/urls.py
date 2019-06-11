from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    # re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path('', views.index, name='index'),
    path('incoming/', views.incoming, name='incoming'),
    re_path(r'api/hours/$', views.api_hours, name='apiHours'),
    re_path(r'api/hours/(?P<hour_id>[0-9][0-3]{0,1}?)/$',
            views.api_hours, name='apiHours'),
    re_path(r'api/restaurants/hours/$',
            views.api_restaurants_hour, name='apiRestaurantsHour'),
    re_path(r'api/restaurants/hours/(?P<hour_id>[0-9][0-3]{0,1}?)/$',
            views.api_restaurants_hour, name='apiRestaurantsHour'),
    re_path(r'api/restaurant/(?P<restaurant_id>[\w,-]+)/hours/$',
            views.api_restaurant_hour, name='apiRestaurantHour'),
    re_path(r'api/restaurant/(?P<restaurant_id>[\w,-]+)/hours/(?P<hour_id>[0-9][0-3]{0,1}?)/$',
            views.api_restaurant_hour, name='apiRestaurantHour'),
    re_path(r'api/restaurant/(?P<restaurant_id>[\w,-]+)/menu/$',
            views.api_restaurant_menu, name='apiRestaurantMenu'),
    re_path(r'api/restaurant/(?P<restaurant_id>[\w,-]+)/hours/(?P<hour_id>[0-9][0-3]{0,1}?)/menu/$',
            views.api_restaurant_menu, name='apiRestaurantMenu'),
    re_path(r'api/users/(?P<user_public_id>[\w,-]+)/private/(?P<user_private_id>\w+)/current_order/$',
            views.api_user_current_order, name='apiUserCurrentOrder'),
    re_path(r'api/orders/$', views.api_orders, name='apiOrders'),
    re_path(r'api/orders/(?P<order_id>\w+)/$',
            views.api_orders, name='apiOrders'),
    re_path(r'api/foods/$', views.api_foods, name='apiFoods'),
    re_path(r'api/foods/(?P<food_id>\w+)/$', views.api_foods, name='apiFoods'),
    re_path(r'api/other/$', views.api_others, name='apiFoods'),
    path('login/', views.sign_in, name='signIn'),
    path('signup/', views.sign_up, name='signUp'),
    path('logout/', views.logout, name='logout'),
    path('manage/', views.manage, name='manage'),
    path('history/', views.history, name='history'),

]
