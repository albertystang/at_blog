from django.urls import path
from . import views


urlpatterns = [    
    path('signup/', views.signup_user.as_view(), name='signup'),
    # path('user-profile/<str:user_name>/', views.profile.as_view(), name='profile'),       
    path('user-profile/<str:user_name>/', views.profile, name='profile'),       
    path('login/', views.login_user.as_view(), name='login'),    
    path('logout/', views.logout_user.as_view(), name='logout'),    
    path('change_password/', views.PasswordChangeView.as_view(template_name='authors/password_change.html'), name='change_password'),    
    path('password_change_success/', views.password_change_success, name='password_change_success'),
    path('edit_profile/', views.UpdateUserView.as_view(), name='edit_profile'),
    path('delete_user/<int:pk>/', views.DeleteUser.as_view(), name='delete_user'),    
]