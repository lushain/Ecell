from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Blog


# Create your views here.

def home(request):
    blogs = Blog.objects.all()
    
    return render(request, 'index.html', {"blogs":blogs[:7]})

def contact(request):
    return render(request, 'contact.html')

def blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs.html', {'blogs':blogs[::-1]})


def remove(request, id):
    if request.user.is_authenticated:
        user = request.user
        try:
            item = Blog.objects.get(id = id)
        except:
            #404
            print("404")
            return redirect('/')

        else:
            if item.author == user:
                item.delete()
                return redirect('/account')
            else:
                #user does not own the item, hence we get an error
                print("Does not own")
                return redirect('/')

    else:
        return redirect('/accounts/login')


def account(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.all()
        username = request.user.username
        none = False
        user_blogs = []

        for i in blogs:
            if str(i.author) == str(request.user.username):
                user_blogs.append(i)

        if user_blogs == []:
            none = True

        return render(request, 'account.html', {"username":username, "blogs": user_blogs, "none": none})

    else:
        #CUSTOM ERROR PAGE
        return redirect('/accounts/login')

def login(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid credentials.", extra_tags="login")
            return redirect('/accounts/login')

    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def change_pass(request):
    if request.method == "POST":
        p1 = request.POST['password1']
        p2 = request.POST['password2']

        user= request.user

        n_user = auth.authenticate(username=request.user.username, password=p1)

        if n_user is not None:
            user.set_password(p2)
            user.save()

            auth.login(request, user)
            return redirect('/account')

        else:
            messages.info(request, "Invalid 'Old Password'.", extra_tags="change_pass")
            return redirect('/account/change-password')
    else:
        return render(request, 'pass.html')


def edit(request):
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            n_user = User.objects.get(username = username)
            if n_user.id == request.user.id:
                pass

            else:
                messages.info(request, "Username already exists, pick a new one.", extra_tags = "username")
                return redirect("/account/edit")

        elif User.objects.filter(email = email).exists():
            n_user = User.objects.get(email= email)
            if n_user.id == request.user.id:
                pass

            else:
                messages.success(request, "This email already exists, try another one.", extra_tags = "email")
                return redirect("/account/edit")

        else:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
            return redirect('/account')

    else:
        return render(request, 'edit.html')

def register(request):
    if request.method == "POST":

        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']


        if password == password2:

            if User.objects.filter(username=username).exists():

                messages.info(request, "Username already exists, pick a new one.", extra_tags = "username")
                return redirect("/accounts/register")

            elif User.objects.filter(email = email).exists():

                messages.success(request, "This email already exists, try another one.", extra_tags = "email")
                return redirect("/accounts/register")

            else:
                user = User.objects.create_user(email=email, username= username, password= password, last_name= last_name, first_name=first_name)
                user.save()
                auth.login(request, user)
                return redirect('/')

        else:
            messages.warning(request, "These passwords do not match", extra_tags = "password")
            return redirect("/accounts/register")

    else:
        return render(request, 'register.html')
    
def create(request):
    if request.method == "POST":
        if request.user.is_authenticated:

            user = request.user

            title = request.POST['title']
            content = request.POST['textarea']
            image = request.FILES.get('image')

            blog = Blog.objects.create(author= user, title=title,content=content,img=image)
            blog.save()

            # return redirect("/account")
            return redirect(f"/blogs/showcase/{blog.id}")

        else:
            return redirect("/accounts/login")

    else:
        if request.user.is_authenticated:
            return render(request, 'create.html')
        else:
            return redirect('/accounts/login')
    
def showcase(request, id):
    try:
        item = Blog.objects.get(id = id)
    except:
        #404
        print("404")
        return redirect('/')

    else:
        if request.user.is_authenticated:
            return render(request, "showcase.html", {"blog":item, "user":request.user})
        return render(request, "showcase.html", {"blog":item})
    
def edit_blog(request, id):
    if request.method == "POST":
        user = request.user
        id = request.POST['id']
        title = request.POST['title']
        content = request.POST['textarea']
        image = request.FILES.get('image')
        rem = request.POST.get('remove-img')

        try:
            blog = Blog.objects.get(id = int(id))
        except:
            return redirect('/blogs')
        else:
            blog.content = content

            if image:
                blog.img = image
            elif str(rem) == "true":
                blog.img = ""
            if title:
                blog.title = title
        

            blog.save()

        return redirect(f"/blogs/showcase/{blog.id}")

    else:
        if request.user.is_authenticated:
            user = request.user
            try:
                item = Blog.objects.get(id = id)
            except:
                #404
                print("404")
                return redirect('/blogs')

            else:
                if user == item.author:
                    return render(request, "editblog.html", {"blog":item})
                else:
                    return redirect('/blogs')

        else:
            return redirect('/accounts/login')

    
        