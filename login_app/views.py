from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, "index.html")

def register(request):
    if request.method =="GET":
        return redirect("/")

    if request.method == "POST":
        errors = User.objects.vablator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            # new_user = User.objects.register(request.POST)
            # request.session['user_id'] = new_user.id
            # messages.success(request, "You have successfully registered!")

            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            new_user = User.objects.create(
                first_name = request.POST["first_name"], 
                last_name = request.POST["last_name"], 
                email = request.POST["email"], 
                password = pw_hash
            )
            request.session['user'] = new_user.first_name
            request.session['user_id'] = new_user.id
            messages.success(request, "You have successfully registered!")
            return redirect("/success")
    return redirect("/")
    

def login(request):
    if request.method == "GET":
        return redirect("/")
    # if not User.objects.authenticate(request.POST['email'], request.POST['password']):
    #     messages.error(request, 'invalid Email/Password')
    #     return redirect("/")
    # user = User.objects.get(email = request.POST['email'])
    # request.session['user_id'] = user.id
    # messages.success(request, "You have successfully logged in!")
    # return redirect("/success")

    user = User.objects.filter(email = request.POST['email'])
    if len(user) > 0:
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user'] = user.first_name
            request.session['user_id'] = user.id
            messages.success(request, "You have successfully logged in!")
            return redirect("/success")
    messages.error(request, "Email or password is incorrect.")
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect("/")

    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'messages': Wall_Message.objects.all()
    }
    return render(request, "success.html", context)

def post_message(request):
    poster = User.objects.get(id = request.session['user_id'])
    Wall_Message.objects.create(message = request.POST['message'], user = poster)
    print(poster)
    return redirect("/success")

def post_comment(request,post_id):
    poster = User.objects.get(id = request.session['user_id'])
    post_message = Wall_Message.objects.get(id = post_id)
    print(post_id)
    Comment.objects.create(comment = request.POST['comment'], user = poster, wall_message = post_message)
    return redirect("/success")

def profile(request, user_id):
    context = {
        'user': User.objects.get(id = user_id)
    }
    return render(request, "profile.html", context)

def delete(request, post_id):
    poster = User.objects.get(id = request.session['user_id'])
    to_delete_message = poster.user_messages.get(id = post_id)
    to_delete_message.delete()
    return redirect("/success")

def add_like(request, post_id):
    liked_message = Wall_Message.objects.get(id = post_id)
    user_liking = User.objects.get(id = request.session['user_id'])
    liked_message.likes.add(user_liking)
    return redirect("/success")

    