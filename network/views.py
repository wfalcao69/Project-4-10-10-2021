from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Comment, Follower, Like


#def index(request):
#    return render(request, "network/index.html")


def index(request):
    # If no user is signed in, return to login page:
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "network/index.html")


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

@csrf_exempt
@login_required
def plus_like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #content = data.get("content")
        w_post = data.get("w_post")
        post = Post.objects.get(pk=w_post)
        user = request.user

        like = Like(
            user=user,
            post=post
        )
        like.save()
        counter = Like.objects.filter(post=post).count()
        return JsonResponse({
            "Success": "like added",
            "likecount":str(counter)
        }, status=200)
    return JsonResponse({
        "Error": "get methode"
    }, status=400)

    ###############################

@csrf_exempt
@login_required
def cancel_like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #content = data.get("content")
        w_post = data.get("w_post")
        post = Post.objects.get(pk=w_post)
        user = request.user

        like = Like(
            user=user,
            post=post
        )
        like.delete()
        counter = Like.objects.filter(post=post).count()
        return JsonResponse({
            "Success": "like canceled",
            "likecount":str(counter)
        }, status=200)
    return JsonResponse({
        "Error": "get methode"
    }, status=400)

    ###############################

@csrf_exempt
@login_required
def likecounter(request,id):
    post = Post.objects.get(pk=id)
    counter = Like.objects.filter(post=post).count()
    return JsonResponse({
        "likecount":str(counter)
    }, status=200)

@csrf_exempt
@login_required
def like_button(request,id):
    #post = Post.objects.get(pk=id)
    post = Post.objects.get(pk=id)
    #counter = Like.objects.filter(post=post).count()
    like_button = Like.objects.filter(post=post).filter(user=request.user.username.count()
    return JsonResponse({
        "like_button":str(like_button)
    }, status=200)

@csrf_exempt
@login_required
def compose(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)

    content = data.get("content")

    if content == "":
        return JsonResponse({
            "error": "Empty post is not permitted."
        }, status=400)


    creator = User.objects.get(username=request.user.username)
    post = Post(
        creator=creator,
        content=content
    )

    post.save()

    return JsonResponse({"message": "Post sent successfully."}, status=201)

 ######################################################################

def all_posts(request):
    post_list = Post.objects.all()
    post_list = post_list.order_by("-time_of_creation").all()
    paginator = Paginator(post_list, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/all_posts.html', {'page_obj': page_obj})

#########################################################################3

def comment(request, post_id):
    post = Post.objects.get(id=post_id)
    #comments_0 = Comment.objects.all()
    comments = Comment.objects.all().filter(item_id=post.id)
    return render(request, "network/comment.html", {
        "post": post,
        "comments": comments
    })

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, "network/edit.html", {
        "post": post
    })

@csrf_exempt
@login_required
def edit_2(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        print(post.content)
        post.content = data["content"]
        post.save()
        return JsonResponse({
            "Success": "Update"
        }, status=200)

        # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def comment_add(request, post_id):
    username = request.user.username
    user = User.objects.get(username=username)
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        comment = request.POST["comment"]
        comments = Comment.objects.create(user=user, post=post, comment=comment, item_id=post.id)
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse("Invalid Input")


def profile(request, creator_id):
    username = request.user.username
    user = User.objects.get(username=username)
    user2 = User.objects.get(id=creator_id)
    #Airport.objects.filter(city="New York")
    post_list = Post.objects.filter(creator=user2)
    post_list = post_list.order_by("-time_of_creation").all()
    paginator = Paginator(post_list, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page',)
    page_obj = paginator.get_page(page_number)
    wells = Follower.objects.all().filter(user=user)
    y_cont = Follower.objects.all().filter(user=user).count()
    w_cont = Follower.objects.all().filter(user=user2).count()
    cont = 0
    for well in wells:
        if well.following == user2:
            cont = cont + 1

    x_cont = user.followed.all().count()
    z_cont = user2.followed.all().count()
    #for well in wells:
    #    if well.following == user2:
    #        w_cont = W_cont + 1
    return render(request, 'network/profile.html', {'page_obj': page_obj, 'user': user, 'user2': user2, "w_cont": int(w_cont), "x_cont": int(x_cont), "z_cont": int(z_cont), 'y_cont': int(y_cont), 'cont': int(cont)})


def follower_add(request, following_id):
    following = User.objects.get(id=following_id)
    username = request.user.username
    user = User.objects.get(username=username)
    #follower_items = Follower.objects.all()
    item_count = Follower.objects.all().filter(user=user, following=following).count()
    if item_count == 1:
        return HttpResponse("Following")
    follower_item = Follower.objects.create(user=user, following=following)
    #my_follower = Follower.objects.all().get(user=user)
    return HttpResponseRedirect(reverse("index"))
    #return render(request, "network/follower_add.html", {
    #    "message": "from now on, following this user, as long as you don't decide to stop following it"
    #    "my_follower": my_follower
    #})


def follower_index(request):
    username = request.user.username
    user = User.objects.get(username=username)
    wells = Follower.objects.all().filter(user=user)
    post_list = Post.objects.all()
    w_list = []
    for well in wells:
        follower = well.following
        w_list.append(follower)
    post_list = Post.objects.filter(creator__in=w_list)
    #post_list = Post.objects.filter(creator=user2)
    #Blog.objects.filter(pk__in=[1, 4, 7])
    post_list = post_list.order_by("-time_of_creation").all()
    paginator = Paginator(post_list, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page',)
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/follower_index.html', {'page_obj': page_obj, 'user': user})



def follower_del(request, following_id):
    following = User.objects.get(id=following_id)
    username = request.user.username
    user = User.objects.get(username=username)
    well = Follower.objects.get(user=user, following=following)
    well.delete()
    return HttpResponseRedirect(reverse("index"))
