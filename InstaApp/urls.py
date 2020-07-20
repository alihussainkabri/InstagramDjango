from InstaApp import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('fetchPosts/', views.fetchPosts, name='fetchPosts'),
    path('addPost/', views.addPost, name='addPost'),
    path('addComment/', views.addComment, name='addComment'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('deletePost/<str:id>/', views.deletePost, name='deletePost'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
