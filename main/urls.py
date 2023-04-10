from django.urls import path
from . import views


urlpatterns = [    
    path('', views.blog_home.as_view(), name='home'),
    path('blog_detail/<str:slug>/', views.blog_detail, name='blog_detail'),    
    path('contact_us/', views.contact_us.as_view(), name='contact_us'),
    # path('create_blog/', views.CreateBlog.as_view(), name='create_blog'),
    path('create_blog/', views.CreateBlog, name='create_blog'),
    path('update_blog/<int:pk>/', views.update_blog, name='update_blog'),
    path('delete_blog/<int:pk>/', views.DeleteBlogView.as_view(), name='delete_blog'),
]