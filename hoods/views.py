from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from .forms import SignUpForm,NeighbourhoodsForm,ProfileForm,ChangeNeighbourhood,MessageForm,BusinessForm,CommentForm
from .models import Profile,Neighbourhoods,Message,Businesses
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username,email=email,password=raw_password)
            profile = Profile(user=user)
            profile.save()
            login(request,user)
            return redirect('index')
    return render(request,'registration/signup.html',{"form":form})

@login_required(login_url='/auth/login/')
def index(request):
    businesses = BusinessForm()
    print(businesses)
    comment = CommentForm()
    new_neighbourhood = NeighbourhoodsForm()
    message_form = MessageForm()
    if request.method == 'POST':
        form = NeighbourhoodsForm(request.POST)
        message_form = MessageForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            return redirect('/')
        if message_form.is_valid():
            messaging = message_form.save(commit=False)
            print('x')
            messaging.user = request.user
            messaging.neighbourhood = request.user.profile.neighbourhood
            messaging.save()
            return redirect('/')
    messages = MessageForm
    if request.user.neighbourhood == None:
        message = 'PLEASE CLICK ON THE PROFILES OPTION AND CHOOSE A NEIGHBOURHOOD'
        return render(request,'index.html',{"comment":comment,"new_neighbourhood":new_neighbourhood,'businesses':businesses,"habari":message,'message_form':message_form,"messages":messages})
    return render(request,'index.html',{"comment":comment,"new_neighbourhood":new_neighbourhood,'businesses':businesses,'message_form':message_form,"messages":messages})

@login_required(login_url='/auth/login/')
def profile(request):
        form = ProfileForm()
        current_user=request.user
        neighbourhood = ChangeNeighbourhood()
        profile = Profile.objects.get(user=current_user)
        if request.method == 'POST':
                form = ProfileForm(request.POST,request.FILES,instance=profile)
                neighbourhood = ChangeNeighbourhood(request.POST,instance=profile)
                if form.is_valid():
                    form.save()
                    return redirect('profile')
                if neighbourhood.is_valid():
                    neighbourhood.save()
                    return redirect('profile')
                else:
                    message = 'Fill in the form appropriately'
                    return render(request,'profile/profile.html',{"neighbourhood":neighbourhood, "profile":profile,"form":form,"message":message})
        return render(request,'profile/profile.html',{"form":form,"neighbourhood":neighbourhood, "profile":profile})

@login_required(login_url='/auth/login/')
def profiles(request,id):
    prof = Profile.objects.get(id=id)
    business = Businesses.objects.filter(user=prof.user)
    return render(request,'profile/profiles.html',{"profile":prof})


@login_required(login_url='/auth/login/')
def search_results(request):

    if 'user' in request.GET or request.GET['user']:
        search_item = request.GET.get('user')
        searched_users = User.objects.filter(username=search_item)
        print(searched_users)
        message = f"{search_item}"
        return render(request, 'search.html',{"message":message,"users": searched_users})
    else:
        message = "You haven't searched for any user"
        return render(request, 'search.html',{"message":message})

@login_required(login_url='/auth/login/')
def create_business(request):
    bizform = BusinessForm()
    if request.method == 'POST':
        bizform = BusinessForm(request.POST,request.FILES)
        if bizform.is_valid():
            bizna = bizform.save(commit=False)
            bizna.user = request.user
            bizna.neighbourhood = request.user.profile.neighbourhood
            bizna.save()
            return redirect('/')
    else:
        bizform = BusinessForm()
        return render(request,"biz.html",{"bizform":bizform})

@login_required(login_url='/auth/login/')
def create_neighbourhood(request):
    if request.method == 'POST':
        new_neighbourhood = NeighbourhoodsForm(request.POST)
        if new_neighbourhood.is_valid():
            neighbourhood = new_neighbourhood.save(commit=False)
            neighbourhood.user = request.user
            neighbourhood.admin = request.user
            neighbourhood.save()
            return redirect('index')

def comment(request,id):
    comment = Message.objects.get(id=id)
    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            comm = comment.save(commit=False)
            comm.user = request.user
            comm.message = commentt
            comm.save()
            return redirect('index')
