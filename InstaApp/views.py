from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core import serializers
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    return HttpResponse('hy')


@api_view(['POST'])
def signup(request):
    data = request.data
    print(data)
    username = data['username']
    email = data['email']
    password = data['password']
    user = User.objects.create_user(
        username=username, email=email, password=password)
    user.save()
    if user:
        auth = authenticate(request, username=user.username, password=password)

        if auth:
            login(request, auth)
            data = {
                'user_id': auth.id,
                'username': auth.username,
                'email': auth.email
            }
            return HttpResponse(json.dumps(data))


@api_view(['POST'])
def signin(request):
    data = request.data
    email = data['email']
    password = data['password']

    if (len(email) > 0 and len(password) > 0):
        get_user = User.objects.filter(email=email)
        if get_user:
            auth = authenticate(
                request, username=get_user[0].username, password=password)

            if auth:
                login(request, auth)
                print(auth.id)
                print(auth.username)
                data = {
                    'user_id': auth.id,
                    'username': auth.username,
                    'email': auth.email
                }
                return HttpResponse(json.dumps(data))


def signout(request):
    logout(request)
    return HttpResponse('done')


def fetchPosts(request):
    allPost = Post.objects.all().order_by('-id')
    comments = Comment.objects.all().order_by('-id')
    data = {
        'allPosts': serializers.serialize('json', allPost),
        'comments': serializers.serialize('json', comments)
    }

    return HttpResponse(json.dumps(data))


def deletePost(request, id):
    post_id = int(id)
    currentPost = Post.objects.filter(id=post_id)[0]
    currentPost.delete()
    allPost = Post.objects.all().order_by('-id')
    comments = Comment.objects.all().order_by('-id')
    data = {
        'allPosts': serializers.serialize('json', allPost),
        'comments': serializers.serialize('json', comments)
    }
    return HttpResponse(json.dumps(data))


@api_view(['POST'])
def addPost(request):
    data = request.data
    user = int(data['user'])
    user = User.objects.filter(id=user)[0]
    caption = data['caption']
    image = data['image']
    new_post = Post.objects.create(
        user=user, image=image, caption=caption, username=user.username)
    new_post.save()
    allPost = Post.objects.all().order_by('-id')
    comments = Comment.objects.all().order_by('-id')
    data = {
        'allPosts': serializers.serialize('json', allPost),
        'comments': serializers.serialize('json', comments)
    }

    return HttpResponse(json.dumps(data))


@api_view(['POST'])
def addComment(request):
    data = request.data
    user_id = int(data['user_id'])
    username = data['username']
    post_id = data['post_id']
    print(post_id)
    comment = data['comment']
    user = User.objects.filter(id=user_id, username=username)[0]
    post = Post.objects.filter(id=post_id)[0]
    newComment = Comment.objects.create(
        post=post, user=user, username=username, comment=comment)
    newComment.save()
    comments = Comment.objects.all().order_by('-id')
    data = {
        'comments': serializers.serialize('json', comments)
    }

    return HttpResponse(json.dumps(data))
