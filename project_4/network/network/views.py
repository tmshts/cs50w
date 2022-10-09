from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts, Follow

import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django import forms
from django.core.paginator import Paginator


class PostForm(forms.Form):
    content_post = forms.CharField(error_messages={'required': "Please enter your name"}, required=True, label="", widget=forms.Textarea(attrs={'placeholder': 'What are you thinking?', 'rows': 4, 'cols': 60, 'radius': 60}))


def index(request):

    posts = Posts.objects.all()
    posts = posts.order_by("-timestamp").all()
    current_user = request.user

    # Show 10 posts per page
    paginator = Paginator(posts, 10)

    # http://127.0.0.1:8000/?page=2
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    return render(request, "network/index.html", {
        "form": PostForm(),
        #"posts": posts,
        "current_user": current_user,
        "page_obj": page_obj
    })
    

@csrf_exempt
def likes(request, id):

    if request.method == "GET":
        return JsonResponse({"error": "POST request required."}, status=400)

    else:
    # if request.method == "POST":
        data = json.loads(request.body)

        current_user = data["current_user"]
        # Get Post object
        post_object = Posts.objects.get(pk=id)
        # Get User object
        user_object = User.objects.get(username=current_user)

        likes_users = post_object.number_of_likes.all()

        # Check if current_user already liked the post or not
        if user_object in likes_users:
            # Remove username like from post
            post_object.number_of_likes.remove(user_object)
        else:
            # Add username like to post
            post_object.number_of_likes.add(user_object)

        # Update number of likes in Javascript
        numero_of_likes = Posts.objects.get(pk=id).number_of_likes.count()      

        return JsonResponse({"numero_of_likes": numero_of_likes})


@csrf_exempt
def post(request, id):

    if request.method == "GET":
        return JsonResponse({"error": "POST request required."}, status=400)

    # POST
    else:
    # if request.method == "POST":
        data = json.loads(request.body)

        edited_text = data["edited_text"] # request.user

        # Update post
        Posts.objects.filter(pk=id).update(content_post=edited_text)

        # Get updated post
        content_post = Posts.objects.get(pk=id).content_post

        return JsonResponse({"content_post": content_post})



def following(request):

    if request.user.is_authenticated:

        current_user = request.user
        # Get users ids (FK) which current_user follows = list with users ids
        selected_users = Follow.objects.filter(want_follow=current_user).values('is_followed')

        # Get all the posts where user_post is equal to the users in that list
        selected_posts = Posts.objects.filter(user_post__in=selected_users) 
        posts = selected_posts.order_by("-timestamp").all()

        # Show 5 posts per page
        paginator = Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/following.html", {
            #"selected_users": selected_users,
            #"posts": posts,
            "current_user": current_user,
            "page_obj": page_obj
        })
    else:
        return JsonResponse({"error": "You have to be logged in in order to see the posts of people you follow."}, status=404)

def follower_handler(request_user, username_object_id):

    # Check follow or not follow button
    follow_value = ''
    if Follow.objects.filter(want_follow=request_user, is_followed=username_object_id).exists():
        follow_value = "Unfollow"
    else:
        follow_value = "Follow"

    return follow_value

@csrf_exempt
def profil(request, username):

    # the roles between username and request_user swapped compared to the GET method
    # POST
    if request.method == "POST":
        data = json.loads(request.body)

        wants_follow_user = data["wants_follow"] # request.user
        is_followed_user = data["is_followed"]

        # Get objects
        wants_follow_user_object = User.objects.get(username=wants_follow_user)
        is_followed_user_object = User.objects.get(username=is_followed_user)

        if Follow.objects.filter(want_follow=wants_follow_user_object.id, is_followed=is_followed_user_object.id).exists():
            # Delete connection
            follow_object = Follow.objects.filter(want_follow=wants_follow_user_object.id, is_followed=is_followed_user_object.id)
            follow_object.delete()
        else:
            # Create follow connection
            Follow.objects.create(want_follow=wants_follow_user_object, is_followed=is_followed_user_object)

        # Check followers count - swapped compared to GET method
        user_follow = Follow.objects.filter(want_follow=is_followed_user_object).count()
        user_is_followed = Follow.objects.filter(is_followed=is_followed_user_object).count()

        follow_value = follower_handler(wants_follow_user_object.id, is_followed_user_object.id)
     
        return JsonResponse({"user_follow_counts": user_follow, "user_is_followed_counts": user_is_followed, "follow": follow_value})

    # interested in username
    else: # request.method == "GET":
    # Check whether user exist - NOT logged in people can still check it.
        try:
            username_object = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "This user does not exist."}, status=404)

        # You have to be logged in in order to see the user´s profile
        if request.user.is_authenticated:
            # Get instance of username
            username_object = User.objects.get(username=username)

            # Get posts based on the username
            posts = Posts.objects.filter(user_post = username_object)

            posts = posts.order_by("-timestamp").all()

            # Determine current user
            current_user = ''
            if username == request.user:
                current_user = request.user
            else:
                current_user = username

            request_user = request.user
            username_object_id = username_object.id

            # Check followers count # different to POST method where username is different
            user_follow = Follow.objects.filter(want_follow=username_object).count()
            user_is_followed = Follow.objects.filter(is_followed=username_object).count()

            # Check follow or not follow button -> I make function see below
            """
            follow_value = ''
            if Follow.objects.filter(want_follow=request_user, is_followed=username_object.id).exists():
                follow_value = "Unfollow"
            else:
                follow_value = "Follow"
            """
            # Check follow or not follow button
            follow_value = follower_handler(request_user, username_object_id)
            # Show 5 posts per page
            paginator = Paginator(posts, 10)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

        else:
            return JsonResponse({"error": "You have to be logged in in order to see the profil."}, status=404)


        return render(request, "network/profil.html", {
            #"posts": posts,
            "current_user": current_user,
            "request_user": request_user,
            "user_follow": user_follow,
            "user_is_followed": user_is_followed,
            "follow_value": follow_value,
            "page_obj": page_obj
        })

@csrf_exempt
@login_required
def create_post(request):

    # Creating a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # GET
    # Takes form from POST request
    form = PostForm(request.POST)

    # Checks if form is valid
    if form.is_valid():
        # get content
        content_post = form.cleaned_data["content_post"]
        # get username instance
        username_instance = User.objects.get(pk=request.user.id)
        # username_id = request.user.id

        # Create new object of class Posts
        Posts.objects.create(user_post=username_instance, content_post=content_post)

        # return JsonResponse({"message": "Post was saved in database."}, status=201)
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")
        

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
