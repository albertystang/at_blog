from django.shortcuts import render, redirect
from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm, LoginForm, PasswordChangingForm, EditUserProfileForm
from django.contrib.auth.decorators import login_required
from main.models import Blog


""" def signup_user(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are signed up successfully...')
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])            
            login(request, new_user)
            return redirect('home')
        else:
            messages.error(request, 'An error in signing up...')
    context = {'form': form}
    return render(request, 'authors/signup.html', context) """


class signup_user(SuccessMessageMixin, generic.CreateView):
    form_class = SignupForm
    template_name = 'authors/signup.html'
    success_url = reverse_lazy('home')
    success_message = 'You are signed up successfully, please log in...'

    def form_invalid(self):
        messages.add_message(self.request, messages.ERROR, "An error in signing up, please try again...")
        return redirect('home')


""" def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are successfully logged in as {username}...")
                return redirect('home')
            else:
                messages.error(request, 'Error')
        else:
            messages.error(request, 'Username or password incorrect...')
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'authors/login.html', context) """


class login_user(generic.View):
    form_class = LoginForm
    template_name = 'authors/login.html'
    success_url = reverse_lazy('home')

    def get(self, request):
        if self.request.user.is_authenticated:
            messages.success(request, 'You have logged in already...')
            return redirect('home')
        else:
            form = self.form_class        
            return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)                    
                    messages.success(request, f"You are successfully logged in...")
                    return redirect('home')
                else:
                    messages.error(request, 'Error')
            else:
                messages.error(request, 'An error in loggin in, please try again...')
        else:
            form = LoginForm()
        context = {'form': form}
        return render(request, 'authors/login.html', context)


""" def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out...')
    return redirect('home') """


class logout_user(LoginRequiredMixin, generic.View): 
    login_url = 'login'
       
    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out...')
        return redirect('home')


@login_required(login_url='login')
def profile(request, user_name):
    blogs = Blog.objects.filter(author__username=user_name)
    context = {'blogs': blogs}
    return render(request, 'authors/profile.html', context)


""" class profile(LoginRequiredMixin, generic.View):
    model = Blog
    login_url = 'login'
    template_name = 'authors/profile.html'

    def get(self, request, user_name):
        blogs = Blog.objects.filter(author__username=user_name)
        context = {'blogs': blogs}
        return render(request, self.template_name, context)  """


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_change_success')


def password_change_success(request):    
    return render(request, 'authors/password_change_success.html')


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = EditUserProfileForm
    template_name = 'authors/edit_user_profile.html'
    success_url = reverse_lazy('home')
    success_message = 'User profile has been updated...'
    login_url = 'login'

    def get_object(self):
        return self.request.user
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "An error in signing up, please try again...")
        return redirect('home')
    

class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = User
    login_url = 'login'
    template_name = 'authors/delete_user_confirm.html'
    success_message = 'User has been deleted...'
    success_url = reverse_lazy('home')