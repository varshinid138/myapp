from django.urls import path
from .views import admin_dashboard, index, login_request, signup, logout_view, create_adm, superuser_dashboard, user_dashboard,next1,next2,plans

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_request, name='login'),
    path('signup/', signup, name='signup'),
    path('create_adm/', create_adm, name='create_adm'),
    path('logout/', logout_view, name='logout'),
    path('superuser_dashboard/', superuser_dashboard, name='superuser_dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('next1/', next1, name='next1'),
    path('next2/', next2, name='next2'),
    path('plans/', plans, name='plans'),
]
