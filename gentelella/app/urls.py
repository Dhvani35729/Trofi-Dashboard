from django.urls import path, re_path
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    # re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path('', views.lost, name='lost'),
    path('incoming/', views.incoming, name='incoming'),    
    re_path(r'api/hours/$', views.api_hours, name='apiHours'),
    re_path(r'api/hours/(?P<hour_id>\w+)/$', views.api_hours, name='apiHours'),
    re_path(r'api/orders/$', views.api_orders, name='apiOrders'),
    re_path(r'api/orders/(?P<order_id>\w+)/$', views.api_orders, name='apiOrders'),     
    path('login/', views.signIn, name='signIn'),
    path('signup/', views.signUp, name='signUp'),    
    path('logout/', views.logout, name='logout'),
    path('manage/', views.manage, name='manage'),
    path('history/', views.history, name='history'),


]
